from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView
from .forms import ContactForm,NotificationForm
from .models import Person, Building,Apartment, DistrictNode, NeighborhoodNode, BuildingNode, ApartmentNode, PersonNode
from neomodel import db
import random

# Create your views here.
def index(request):
    return render(request,'base.html')

def get_persons(request):
    return render(request, 'persons.html')
    
def get_person(request,person_id):
    try:
        person_id = int(person_id)
    except ValueError:
        raise Http404()
    return render(request, 'person.html', {"person_id":person_id})

class PersonsView(View):
    def get(self,request,*args,**kwargs):
        persons = PersonNode.nodes.all()
        context = {"persons":persons}
        return render(request,'persons.html',context)

def get_buildingsgraph(request):
    buildingnodes = BuildingNode.nodes.all()
    return render(request, 'buildingsgraph.html', {"buildingnodes":buildingnodes})

class BuildingsView(TemplateView):
    template_name = 'buildingsgraph.html'

    def get_context_data(self,*args,**kwargs):
        context = super(BuildingsView,self).get_context_data(*args, **kwargs)
        buildingnodes = BuildingNode.nodes.all()
        print(str(len(buildingnodes)))
        context = {"buildingnodes":buildingnodes}
        return context
    #def get(self,request,*args,**kwargs):
    #    buildingnodes = BuildingNode.nodes.all()
    #    context = {"buildingnodes":buildingnodes}
    #    return render(request,'buildingsgraph.html',context)

def meta(request):
    return render(request, 'meta.html', {"meta":request.META})

def search(request):
    return render(request, 'search.html')

def search_results(request):
    errors = []
    q = None
    if 'q' in request.GET:
        q = request.GET['q']
    if not q:
        errors.append('Enter a search term')
    elif len(q) > 20:
        errors.append('Please enter at most 20 characters.')
    else:
        persons = Person.objects.filter(name__icontains=q)
        return render(request, 'search_results.html',{"query":request.GET['q'],"persons":persons})
    return render(request,'search.html',{'errors':errors})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(initial={'subject':'I love your site!'})
    return render(request,'contact_form.html',{'form':form})

def contactthanks(request):
    form = ContactForm()
    messages = []
    messages.append('Thank you')
    return render(request,'contact_form.html',{'form':form,'messages':messages})

def notification(request):
    messages = []
    results = []
    errors = []
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            messages.append("Searching for " + cd['district'])
            graphresults = db.cypher_query("MATCH (p:PersonNode)-[r:LIVES_IN]-(a:ApartmentNode)-[r1:PART_OF]-"
                                     "(b:BuildingNode)-[r2:PART_OF]->(n:NeighborhoodNode)-[r3:PART_OF]->"
                                     "(d:DistrictNode {name:'" + cd['district'] + "'})"
                                     " RETURN p,a,b,n,d")
            for graphresult in graphresults[0]:
                results.append({"personname":graphresult[0].properties['name'],"personmobile":graphresult[0].properties['mobile'],
                                "apartmentnumber":graphresult[1].properties['number'],"apartmentfloor":graphresult[1].properties['floor'],
                                "buildingaddress":graphresult[2].properties['address'],"neighborhoodname":graphresult[3].properties['name'],
                                "districtname":graphresult[4].properties['name']})
    else:
        form = NotificationForm()
    return render(request,'notification.html',{'form':form,'messages':messages,'results':results,'errors':errors})

def setupgraph(request):
    messages = []
    districts = ["Kungsholmen","Norrmalm","Södermalm","Östermalm","Enskede-Årsta-Vantör","Farsta","Hägersten-Liljeholmen"
                 ,"Skarpnäck","Skärholmen","Bromma","Hässelby-Vällingby","Rinkeby-Kista","Spånga-Tensta"]
    messages.append("Checking for existing populated database")
    if len(DistrictNode.nodes.all()) > 0:
        messages.append("District Nodes found so skipping creation")
    else:
        messages.append("Creating District Nodes")
        for district in districts:
            d = DistrictNode(name=district)
            d.save()
            messages.append("Added District Node : " + district)
    if len(NeighborhoodNode.nodes.all()) > 0:
        messages.append("NeighborhoodNodes found so skipping creation")
    else:
        messages.append("Creating Neighborhood Nodes")
        districts = DistrictNode.nodes.all()
        counter = 0
        for i in range (0,13,1):
            for j in range (0,3,1):
                n = NeighborhoodNode(name="NB" + str(counter))
                districtindex = int(i)
                n.save()
                counter += 1
                messages.append("Added Neighborhood Node : " + "NB" + str(counter))
                n.community.connect(districts[districtindex])
                messages.append("Connected Neighborhood Node : " + "NB" + str(counter) + " to district : " + districts[districtindex].name )
    if len(BuildingNode.nodes.all()) > 0:
        messages.append("BuildingNodes found so skipping creation")
    else:
        messages.append("Creating Building Nodes")
        neighborhoods = NeighborhoodNode.nodes.all()
        counter = 0
        for i in range (0,39,1):
            for j in range (0,4,1):
                b = BuildingNode(address="BD" + str(counter))
                neighborhoodindex = int(i)
                b.save()
                counter += 1
                messages.append("Added Building Node : " + "BD" + str(counter))
                b.neighborhood.connect(neighborhoods[neighborhoodindex])
                messages.append("Connected Building Node : " + "BD" + str(counter) + " to neighborhood : " + neighborhoods[neighborhoodindex].name)
    if len(ApartmentNode.nodes.all()) > 0:
        messages.append("ApartmentNodes found so skipping creation")
    else:
        messages.append("Creating Apartment Nodes")
        buildings = BuildingNode.nodes.all()
        counter = 0
        for i in range (0,156,1):
            for j in range (0,5,1):
                a = ApartmentNode(number="AP" + str(counter),floor=random.randint(0,7))
                buildingindex = int(i)
                a.save()
                counter += 1
                messages.append("Added Apartment Node : " + "AP" + str(counter))
                a.building.connect(buildings[buildingindex])
                messages.append("Connected Apartment Node : " + "AP" + str(counter) + " to building : " + buildings[buildingindex].address)
    if len(PersonNode.nodes.all()) > 0:
        messages.append("PersonNodes found so skipping creation")
    else:
        messages.append("Creating Person Nodes")
        apartments = ApartmentNode.nodes.all()
        first_name = ["John","Nick","Lars","Eric","William","Lucas","Oscar","Hugo","Elias","Alice","Maja","Elsa","Julia","Liam","Ella"]
        last_name = ["Johansson","Andersson","Karlsson","Nilsson","Eriksson","Larsson","Olsson","Persson","Svensson","Gustafsson"]
        counter = 0
        for i in range (0,500):
            name = first_name[random.randint(0,len(first_name)-1)] + "," + last_name[random.randint(0,len(last_name)-1)]
            mobile = random.randint(1000000,9999999)
            p = PersonNode(name=name,mobile=mobile)
            apartmentindex = random.randint(0,780)
            p.save()
            messages.append("Added Person Node : " + name)
            p.apartment.connect(apartments[apartmentindex])
            messages.append("Connected Person Node : " + name + " to apartment : " + apartments[apartmentindex].number)
    return render(request,'setupgraph.html',{'messages':messages})
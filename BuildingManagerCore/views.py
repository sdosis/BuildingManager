from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .forms import ContactForm
from .models import Person, Building,Apartment, BuildingNode

# Create your views here.
def index(request):
    return HttpResponse("Welcome")

def get_persons(request):
    return render(request, 'persons.html')
    #return render('BuildingManagerCore/persons.html', request, {'persons': Person.nodes.all()})

def get_person(request,person_id):
    try:
        person_id = int(person_id)
    except ValueError:
        raise Http404()
    return render(request, 'person.html', {"person_id":person_id})

def get_buildingsgraph(request):
    buildingnodes = BuildingNode.nodes.all()
    return render(request, 'buildingsgraph.html', {"buildingnodes":buildingnodes})

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
from django.db import models
from django_neomodel import DjangoNode
from neomodel import StructuredNode, StringProperty,RelationshipTo,RelationshipFrom

# Create your models here.
class Building(models.Model):
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.address

class Apartment(models.Model):
    number = models.CharField(max_length=10)
    floor = models.IntegerField()
    building = models.ForeignKey(Building,on_delete=models.DO_NOTHING,default='0')

    def __str__(self):
        return str(self.building.id) + " " + self.number

class Person(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15)
    apartment = models.ManyToManyField(Apartment)

    def __str__(self):
        return self.name

class BuildingNode(StructuredNode):
    address = StringProperty(unique_index=True)
    apartment = RelationshipFrom('ApartmentNode','PART_OF')

class ApartmentNode(StructuredNode):
    number = StringProperty()
    floor = StringProperty()
    building = RelationshipTo(BuildingNode,'PART_OF')
    person = RelationshipFrom('PersonNode','LIVES_IN')

class PersonNode(StructuredNode):
    name = StringProperty()
    mobile = StringProperty()
    apartment = RelationshipTo(ApartmentNode,'LIVES_IN')

from django.contrib import admin
from .models import Building, Apartment, Person, BuildingNode

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name','mobile')
    search_fields = ('name','mobile')
    list_filter = ('name',)
    ordering = ('name',)
    filter_horizontal = ('apartment',)

class ApartmentAdmin(admin.ModelAdmin):
    raw_id_fields = ('building',)

# Register your models here.
admin.site.register(Building)
admin.site.register(Apartment,ApartmentAdmin)
admin.site.register(Person,PersonAdmin)
#admin.site.register(BuildingNode)
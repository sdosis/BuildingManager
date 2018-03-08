from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('persons/',views.get_persons),
    path('persons/<int:person_id>', views.get_person),
    path('graph/',views.get_buildingsgraph),
    path('graph/buildings',views.get_buildingsgraph),
    path('meta/',views.meta),
    path('search/',views.search),
    path('search/results/',views.search_results),
    path('notification/',views.notification),
    path('contact/',views.contact),
    path('contact/thanks/',views.contactthanks),
    path('setup/graph/',views.setupgraph)
]
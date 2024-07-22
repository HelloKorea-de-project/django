from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='airline_index'),
    path('search-flights/', views.search_flights, name='search_flights'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='tour_index'),
    path('district/<str:district_name>/', views.district_detail, name='district_detail'),
    path('get-district-info/', views.get_district_info, name='get_district_info'),
    path('district/<str:district_name>/all/', views.get_district_detail, name='get_district_detail'),
    path('district/<str:district_name>/tour-info/', views.get_tour_info, name='get_tour_info'),
    path('district/<str:district_name>/events/', views.get_events, name='get_events'),
    path('district/<str:district_name>/lodgings/', views.get_lodgings, name='get_lodgings'),
]
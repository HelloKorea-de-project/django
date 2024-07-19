from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='tour_index'),
    path('district/<str:district_name>/', views.district_detail, name='district_detail'),
]

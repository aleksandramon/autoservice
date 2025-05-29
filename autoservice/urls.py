from django.urls import path
from . import views

app_name = 'autoservice'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.service_list, name='service_list'),
    path('service/<int:id>/', views.service_detail, name='service_detail'),
    path('search/', views.search_services, name='search_services'),
]
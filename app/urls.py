from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('experience/', views.experience, name='experience'),
    path('skills/', views.skills, name='skills'),
    path('contact/', views.contact, name='contact'),
    path('personal_projects/', views.personal_projects, name='personal_projects'),
    path('servicios/', views.services, name='services'),
    # Agendamiento
    path('agendar/', views.agendar, name='agendar'),
    path('agendar/horarios/', views.get_available_slots, name='get_available_slots'),
    path('agendar/confirmar/<uuid:token>/', views.confirm_appointment, name='confirm_appointment'),
    path('agendar/cancelar/<uuid:token>/', views.cancel_appointment, name='cancel_appointment'),
]

from django.urls import path
from django_distill import distill_path
from . import views

urlpatterns = [
    # Páginas de contenido estático: se congelan con `distill_path` para
    # que `python manage.py distill generate` las escriba en docs/.
    # Las vistas dinámicas (agendamiento, contacto, endpoints AJAX) se
    # dejan con `path` normal: django-distill las ignora y siguen siendo
    # servidas por el backend Django en producción.
    distill_path('robots.txt', views.robots_txt, name='robots_txt'),
    distill_path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    distill_path('', views.index, name='index'),
    distill_path('about/', views.about, name='about'),
    distill_path('experience/', views.experience, name='experience'),
    distill_path('skills/', views.skills, name='skills'),
    path('contact/', views.contact, name='contact'),
    distill_path('personal_projects/', views.personal_projects, name='personal_projects'),
    distill_path('servicios/', views.services, name='services'),
    # Agendamiento
    path('agendar/', views.agendar, name='agendar'),
    path('agendar/configuracion-calendario/', views.get_calendar_config, name='get_calendar_config'),
    path('agendar/horarios/', views.get_available_slots, name='get_available_slots'),
    path('agendar/confirmar/<uuid:token>/', views.confirm_appointment, name='confirm_appointment'),
    path('agendar/cancelar/<uuid:token>/', views.cancel_appointment, name='cancel_appointment'),
]

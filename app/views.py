from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def index(request):
    return render(request, 'index.html', {'title': 'Inicio'})

def about(request):
    return render(request, 'about.html', {'title': 'Quién Soy'})

def experience(request):
    return render(request, 'experience.html', {'title': 'Experiencia'})

def skills(request):
    return render(request, 'skills.html', {'title': 'Habilidades'})

def personal_projects(request):
    return render(request, 'personal_projects.html', {'title': 'Proyectos personales'})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'Consulta desde el sitio web')
        message = request.POST.get('message')
        
        # Enviar email
        email_message = f"""
        Nombre: {name}
        Email: {email}
        
        Mensaje:
        {message}
        """
        
        try:
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, '¡Tu mensaje ha sido enviado con éxito!')
        except Exception as e:
            messages.error(request, 'Hubo un error al enviar tu mensaje. Por favor intenta nuevamente.')
        
        return render(request, 'contact.html', {'title': 'Contáctame'})
    
    return render(request, 'contact.html', {'title': 'Contáctame'})
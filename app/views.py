from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .forms import ContactForm
import logging

# Configurar logger
logger = logging.getLogger(__name__)

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
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject'] or 'Consulta desde el sitio web'
            message = form.cleaned_data['message']
            
            # Enviar email
            email_message = f"""
            Nuevo mensaje de contacto desde acortesv.cl:
            
            Nombre: {name}
            Email: {email}
            Asunto: {subject}
            
            Mensaje:
            {message}
            
            ---
            Enviado desde: {request.META.get('HTTP_HOST', 'Sitio web')}
            IP: {request.META.get('REMOTE_ADDR', 'No disponible')}
            """
            
            try:
                # Verificar configuración de email
                if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                    raise Exception("Configuración de email incompleta - verifica EMAIL_HOST_USER y EMAIL_HOST_PASSWORD")
                
                if not settings.DEFAULT_FROM_EMAIL or not settings.CONTACT_EMAIL:
                    raise Exception("Configuración de email incompleta - verifica DEFAULT_FROM_EMAIL y CONTACT_EMAIL")
                
                # Log de intento de envío
                logger.info(f"Intentando enviar email desde {email} a {settings.CONTACT_EMAIL}")
                



                # Enviar email
                result = send_mail(
                    subject=f"Nuevo mensaje de contacto: {subject}",
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                
                if result:
                    # Log del envío exitoso
                    logger.info(f"Email enviado exitosamente desde {email} a {settings.CONTACT_EMAIL}")
                    messages.success(request, '¡Tu mensaje ha sido enviado con éxito! Te responderé pronto.')
                else:
                    raise Exception("El email no se pudo enviar - resultado fue False")
                
            except Exception as e:
                # Log del error con más detalles
                error_msg = f"Error enviando email desde {email}: {str(e)}"
                logger.error(error_msg)
                
                # Mensaje de error más específico
                if "Authentication" in str(e):
                    user_msg = "Error de autenticación. Verifica las credenciales de Gmail."
                elif "SMTP" in str(e):
                    user_msg = "Error de conexión SMTP. Verifica la configuración del servidor."
                elif "TLS" in str(e):
                    user_msg = "Error de conexión TLS. Verifica la configuración de seguridad."
                else:
                    user_msg = f"Error al enviar el mensaje: {str(e)}"
                
                messages.error(request, f'{user_msg} Por favor intenta nuevamente más tarde o contáctame directamente por email.')
            
            return render(request, 'contact.html', {'title': 'Contáctame', 'form': ContactForm()})
        else:
            # Si el formulario no es válido, mostrar errores
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'title': 'Contáctame', 'form': form})




from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_GET
from datetime import date as date_type, datetime, timedelta
from .forms import ContactForm
from .models import Appointment, AvailableSlot, BlockedDate
import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuración de ventana de agendamiento (días hábiles)
# ---------------------------------------------------------------------------
MIN_BOOKING_DAYS_AHEAD = 1   # Mínimo de días de anticipación
MAX_BOOKING_DAYS_AHEAD = 30  # Máximo de días hacia adelante

DAYS_ES = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
MONTHS_ES = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
]


def _format_date_es(d):
    return f"{DAYS_ES[d.weekday()]}, {d.day} de {MONTHS_ES[d.month - 1]} de {d.year}"


def _send_booking_confirmation(appointment):
    """Correo al prospecto confirmando que quedó agendado (no confirmado aún)."""
    date_str = _format_date_es(appointment.date).capitalize()
    subject = f"Reunión agendada con Alejandro Cortés – {appointment.date.strftime('%d/%m/%Y')}"
    context = {'appointment': appointment, 'date_formatted': date_str}
    plain = (
        f"Hola {appointment.name},\n\n"
        f"Tu reunión ha sido registrada correctamente.\n"
        f"Fecha: {date_str}\n"
        f"Hora:  {appointment.time.strftime('%H:%M')} hrs\n\n"
        f"Recibirás un correo 24 horas antes con enlace para confirmar tu asistencia.\n\n"
        f"Alejandro Cortés V. | contacto@acortesv.cl"
    )
    try:
        html = render_to_string('emails/booking_confirmation.html', context)
        send_mail(
            subject=subject,
            message=plain,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.email],
            html_message=html,
            fail_silently=True,
        )
    except Exception as exc:
        logger.error(f"Error sending booking confirmation to {appointment.email}: {exc}")


def _send_host_notification(appointment):
    """Notifica a Alejandro de una nueva reserva."""
    date_str = _format_date_es(appointment.date).capitalize()
    subject = (
        f"Nueva reunión agendada: {appointment.name} – "
        f"{appointment.date.strftime('%d/%m/%Y')} {appointment.time.strftime('%H:%M')}"
    )
    context = {'appointment': appointment, 'date_formatted': date_str}
    plain = (
        f"Nueva reunión: {appointment.name} | {appointment.email} | {appointment.phone}\n"
        f"Fecha: {date_str} | Hora: {appointment.time.strftime('%H:%M')} hrs\n"
        f"Notas: {appointment.notes or 'Sin notas'}"
    )
    try:
        html = render_to_string('emails/host_notification.html', context)
        send_mail(
            subject=subject,
            message=plain,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            html_message=html,
            fail_silently=True,
        )
    except Exception as exc:
        logger.error(f"Error sending host notification: {exc}")


# ---------------------------------------------------------------------------
# Vistas principales
# ---------------------------------------------------------------------------

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


def services(request):
    return render(request, 'services.html', {'title': 'Servicios'})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject'] or 'Consulta desde el sitio web'
            message = form.cleaned_data['message']

            email_message = (
                f"Nuevo mensaje de contacto desde acortesv.cl:\n\n"
                f"Nombre: {name}\n"
                f"Email: {email}\n"
                f"Asunto: {subject}\n\n"
                f"Mensaje:\n{message}\n\n"
                f"---\n"
                f"IP: {request.META.get('REMOTE_ADDR', 'No disponible')}"
            )

            try:
                if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                    raise Exception("Configuración de email incompleta")
                if not settings.DEFAULT_FROM_EMAIL or not settings.CONTACT_EMAIL:
                    raise Exception("Configuración de email incompleta")

                logger.info(f"Intentando enviar email desde {email} a {settings.CONTACT_EMAIL}")
                result = send_mail(
                    subject=f"Nuevo mensaje de contacto: {subject}",
                    message=email_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                if result:
                    logger.info(f"Email enviado exitosamente desde {email}")
                    messages.success(request, '¡Tu mensaje ha sido enviado con éxito! Te responderé pronto.')
                else:
                    raise Exception("El email no se pudo enviar")

            except Exception as e:
                error_msg = f"Error enviando email desde {email}: {str(e)}"
                logger.error(error_msg)
                if "Authentication" in str(e):
                    user_msg = "Error de autenticación con el servidor de correo."
                elif "SMTP" in str(e):
                    user_msg = "Error de conexión SMTP."
                else:
                    user_msg = f"Error al enviar el mensaje: {str(e)}"
                messages.error(request, f'{user_msg} Intenta nuevamente o contáctame directamente.')

            return render(request, 'contact.html', {'title': 'Contáctame', 'form': ContactForm()})
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'title': 'Contáctame', 'form': form})


# ---------------------------------------------------------------------------
# Agendamiento
# ---------------------------------------------------------------------------

def agendar(request):
    if request.method == 'POST':
        date_str = request.POST.get('date', '').strip()
        time_str = request.POST.get('time', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        notes = request.POST.get('notes', '').strip()

        errors = []

        if not all([date_str, time_str, name, email, phone]):
            errors.append('Todos los campos obligatorios deben completarse.')

        booking_date = None
        booking_time = None

        try:
            booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            booking_time = datetime.strptime(time_str, '%H:%M').time()
        except (ValueError, TypeError):
            errors.append('Fecha u hora inválida. Por favor vuelve al paso anterior.')

        if booking_date:
            today = date_type.today()
            min_date = today + timedelta(days=MIN_BOOKING_DAYS_AHEAD)
            max_date = today + timedelta(days=MAX_BOOKING_DAYS_AHEAD)

            if booking_date < min_date or booking_date > max_date:
                errors.append('La fecha seleccionada no está disponible.')
            elif BlockedDate.objects.filter(date=booking_date).exists():
                errors.append('La fecha seleccionada no está disponible.')
            elif not AvailableSlot.objects.filter(
                weekday=booking_date.weekday(),
                time=booking_time,
                is_active=True,
            ).exists():
                errors.append('El horario seleccionado no está disponible.')
            elif Appointment.objects.filter(
                date=booking_date,
                time=booking_time,
                status__in=[Appointment.STATUS_PENDING, Appointment.STATUS_CONFIRMED],
            ).exists():
                errors.append(
                    'Este horario acaba de ser reservado por otra persona. '
                    'Por favor selecciona otro.'
                )

        if errors:
            for err in errors:
                messages.error(request, err)
            return render(request, 'agendar.html', {'title': 'Agéndame'})

        appointment = Appointment.objects.create(
            date=booking_date,
            time=booking_time,
            name=name,
            email=email,
            phone=phone,
            notes=notes,
        )

        _send_booking_confirmation(appointment)
        _send_host_notification(appointment)

        return render(request, 'agendar_success.html', {
            'title': 'Reunión agendada',
            'appointment': appointment,
            'date_formatted': _format_date_es(appointment.date).capitalize(),
        })

    return render(request, 'agendar.html', {'title': 'Agéndame'})


@require_GET
def get_calendar_config(request):
    """Devuelve al JS los días activos, fechas bloqueadas y ventana de reserva."""
    today = date_type.today()
    max_date = today + timedelta(days=MAX_BOOKING_DAYS_AHEAD)

    active_weekdays = list(
        AvailableSlot.objects.filter(is_active=True)
        .values_list('weekday', flat=True)
        .distinct()
        .order_by('weekday')
    )

    blocked = list(
        BlockedDate.objects.filter(date__gte=today, date__lte=max_date)
        .values_list('date', flat=True)
    )
    blocked_dates = [d.strftime('%Y-%m-%d') for d in blocked]

    return JsonResponse({
        'available_weekdays': active_weekdays,
        'blocked_dates': blocked_dates,
        'min_days_ahead': MIN_BOOKING_DAYS_AHEAD,
        'max_days_ahead': MAX_BOOKING_DAYS_AHEAD,
    })


@require_GET
def get_available_slots(request):
    date_str = request.GET.get('date', '')
    try:
        requested_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return JsonResponse({'slots': []})

    today = date_type.today()
    min_date = today + timedelta(days=MIN_BOOKING_DAYS_AHEAD)
    max_date = today + timedelta(days=MAX_BOOKING_DAYS_AHEAD)

    if requested_date < min_date or requested_date > max_date:
        return JsonResponse({'slots': []})

    if BlockedDate.objects.filter(date=requested_date).exists():
        return JsonResponse({'slots': []})

    # Horarios activos para este día de la semana desde la BD
    db_slots = (
        AvailableSlot.objects.filter(weekday=requested_date.weekday(), is_active=True)
        .values_list('time', flat=True)
        .order_by('time')
    )
    if not db_slots:
        return JsonResponse({'slots': []})

    booked = Appointment.objects.filter(
        date=requested_date,
        status__in=[Appointment.STATUS_PENDING, Appointment.STATUS_CONFIRMED],
    ).values_list('time', flat=True)

    booked_times = {t.strftime('%H:%M') for t in booked}
    available = [t.strftime('%H:%M') for t in db_slots if t.strftime('%H:%M') not in booked_times]

    return JsonResponse({'slots': available})


def confirm_appointment(request, token):
    try:
        appt = Appointment.objects.get(
            confirmation_token=token,
            status=Appointment.STATUS_PENDING,
        )
        appt.status = Appointment.STATUS_CONFIRMED
        appt.save(update_fields=['status'])

        date_str = _format_date_es(appt.date).capitalize()
        subject = "Asistencia confirmada – Reunión con Alejandro Cortés"
        plain = (
            f"Hola {appt.name},\n\n"
            f"¡Perfecto! Tu asistencia ha sido confirmada.\n"
            f"Fecha: {date_str} | Hora: {appt.time.strftime('%H:%M')} hrs\n\n"
            f"Nos vemos entonces.\nAlejandro Cortés V."
        )
        try:
            html = render_to_string('emails/booking_confirmed.html', {
                'appointment': appt,
                'date_formatted': date_str,
            })
            send_mail(subject, plain, settings.DEFAULT_FROM_EMAIL, [appt.email],
                      html_message=html, fail_silently=True)
        except Exception:
            pass

        return render(request, 'agendar_confirm.html', {
            'title': 'Asistencia confirmada',
            'appointment': appt,
            'date_formatted': date_str,
        })
    except Appointment.DoesNotExist:
        messages.error(request, 'El enlace no es válido o la reunión ya fue confirmada.')
        return redirect('agendar')


def cancel_appointment(request, token):
    try:
        appt = Appointment.objects.get(
            confirmation_token=token,
            status__in=[Appointment.STATUS_PENDING, Appointment.STATUS_CONFIRMED],
        )
        appt.status = Appointment.STATUS_CANCELLED
        appt.save(update_fields=['status'])

        return render(request, 'agendar_cancelled.html', {
            'title': 'Reunión cancelada',
            'appointment': appt,
            'date_formatted': _format_date_es(appt.date).capitalize(),
        })
    except Appointment.DoesNotExist:
        messages.error(request, 'El enlace no es válido o la reunión ya fue cancelada.')
        return redirect('agendar')

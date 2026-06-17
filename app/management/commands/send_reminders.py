"""
Comando: python manage.py send_reminders

Envía recordatorios por correo a todas las reuniones pendientes o confirmadas
que ocurren en las próximas 23–25 horas.

Configurar cron (en el servidor) para ejecutar cada hora:
    0 * * * * /ruta/venv/bin/python /ruta/proyecto/manage.py send_reminders >> /ruta/proyecto/logs/reminders.log 2>&1
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
import pytz
import logging

from app.models import Appointment

logger = logging.getLogger(__name__)

DAYS_ES = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
MONTHS_ES = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
]


def _format_date_es(d):
    return f"{DAYS_ES[d.weekday()]}, {d.day} de {MONTHS_ES[d.month - 1]} de {d.year}"


class Command(BaseCommand):
    help = 'Envía recordatorios de confirmación a reuniones en las próximas 24 horas'

    def handle(self, *args, **options):
        tz = pytz.timezone(settings.TIME_ZONE)
        now = datetime.now(tz)
        window_start = now + timedelta(hours=23)
        window_end = now + timedelta(hours=25)

        pending = Appointment.objects.filter(
            status__in=[Appointment.STATUS_PENDING, Appointment.STATUS_CONFIRMED],
            reminder_sent=False,
        )

        sent = 0
        site_url = getattr(settings, 'SITE_URL', 'https://acortesv.cl')

        for appt in pending:
            appt_dt = tz.localize(datetime.combine(appt.date, appt.time))
            if not (window_start <= appt_dt <= window_end):
                continue

            confirm_url = f"{site_url}/agendar/confirmar/{appt.confirmation_token}/"
            cancel_url = f"{site_url}/agendar/cancelar/{appt.confirmation_token}/"
            date_str = _format_date_es(appt.date).capitalize()

            subject = "Recordatorio: Tu reunión con Alejandro Cortés es mañana"
            message = (
                f"Hola {appt.name},\n\n"
                f"Este es un recordatorio de tu reunión programada para mañana.\n\n"
                f"Detalles:\n"
                f"  Fecha: {date_str}\n"
                f"  Hora:  {appt.time.strftime('%H:%M')} hrs\n\n"
                f"Por favor confirma tu asistencia haciendo clic aquí:\n"
                f"{confirm_url}\n\n"
                f"Si no puedes asistir, cancela aquí:\n"
                f"{cancel_url}\n\n"
                f"Si ya confirmaste anteriormente, ignora este mensaje.\n\n"
                f"---\n"
                f"Alejandro Cortés V.\n"
                f"Consultor en Tecnología y Procesos de Negocio\n"
                f"contacto@acortesv.cl  |  +56 9 4482 3643\n"
                f"www.acortesv.cl"
            )

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[appt.email],
                    fail_silently=False,
                )
                appt.reminder_sent = True
                appt.save(update_fields=['reminder_sent'])
                sent += 1
                logger.info(f"Reminder sent → {appt.email} ({appt.date} {appt.time})")
                self.stdout.write(self.style.SUCCESS(
                    f"  ✓ {appt.name} <{appt.email}> — {appt.date} {appt.time.strftime('%H:%M')}"
                ))
            except Exception as exc:
                logger.error(f"Error sending reminder to {appt.email}: {exc}")
                self.stdout.write(self.style.ERROR(
                    f"  ✗ {appt.email}: {exc}"
                ))

        self.stdout.write(self.style.SUCCESS(f"\nRecordatorios enviados: {sent}"))

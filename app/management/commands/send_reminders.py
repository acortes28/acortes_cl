"""
Comando: python manage.py send_reminders

Envía recordatorios por correo a todas las reuniones pendientes o confirmadas
que ocurren en las próximas 23–25 horas.

Para pruebas, usa --force para ignorar la ventana de tiempo:
    python manage.py send_reminders --force

Configurar cron (en el servidor) para ejecutar cada hora:
    0 * * * * /home/acortes/repositorio/acortes_cl/venv/bin/python /home/acortes/repositorio/acortes_cl/manage.py send_reminders >> /home/acortes/repositorio/acortes_cl/logs/reminders.log 2>&1
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
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

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Enviar recordatorio ignorando la ventana de tiempo (para pruebas)',
        )

    def handle(self, *args, **options):
        force = options['force']
        tz = pytz.timezone(settings.TIME_ZONE)
        now = datetime.now(tz)
        window_start = now + timedelta(hours=23)
        window_end   = now + timedelta(hours=25)

        self.stdout.write(f"Ahora:   {now.strftime('%Y-%m-%d %H:%M %Z')}")
        self.stdout.write(
            f"Ventana: {window_start.strftime('%Y-%m-%d %H:%M')} → "
            f"{window_end.strftime('%Y-%m-%d %H:%M')}"
        )
        if force:
            self.stdout.write(self.style.WARNING("  [--force] Ventana de tiempo ignorada"))

        pending = Appointment.objects.filter(
            status__in=[Appointment.STATUS_PENDING, Appointment.STATUS_CONFIRMED],
            reminder_sent=False,
        )

        self.stdout.write(f"Reuniones pendientes sin recordatorio: {pending.count()}")

        if not pending.exists():
            self.stdout.write("  (ninguna encontrada)")
            return

        sent = 0
        site_url = getattr(settings, 'SITE_URL', 'https://acortesv.cl')

        for appt in pending:
            appt_dt = tz.localize(datetime.combine(appt.date, appt.time))
            in_window = window_start <= appt_dt <= window_end

            if not force and not in_window:
                self.stdout.write(
                    f"  — {appt.name} ({appt.date} {appt.time.strftime('%H:%M')}) "
                    f"fuera de ventana [{appt_dt.strftime('%Y-%m-%d %H:%M')}] → ignorada"
                )
                continue

            confirm_url = f"{site_url}/agendar/confirmar/{appt.confirmation_token}/"
            cancel_url  = f"{site_url}/agendar/cancelar/{appt.confirmation_token}/"
            date_str    = _format_date_es(appt.date).capitalize()

            subject = "Recordatorio: Tu reunión con Alejandro Cortés es mañana"

            plain = (
                f"Hola {appt.name},\n\n"
                f"Recordatorio: tu reunión es mañana.\n"
                f"Fecha: {date_str}\n"
                f"Hora:  {appt.time.strftime('%H:%M')} hrs\n\n"
                f"Confirmar asistencia: {confirm_url}\n"
                f"Cancelar: {cancel_url}\n\n"
                f"Alejandro Cortés V. | contacto@acortesv.cl"
            )

            context = {
                'appointment': appt,
                'date_formatted': date_str,
                'confirm_url': confirm_url,
                'cancel_url': cancel_url,
            }

            try:
                html = render_to_string('emails/booking_reminder.html', context)
                send_mail(
                    subject=subject,
                    message=plain,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[appt.email],
                    html_message=html,
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

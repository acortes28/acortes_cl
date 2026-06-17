import uuid
from django.db import models


class AvailableSlot(models.Model):
    WEEKDAY_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    weekday = models.IntegerField('Día de la semana', choices=WEEKDAY_CHOICES)
    time = models.TimeField('Hora')
    is_active = models.BooleanField('Activo', default=True)

    class Meta:
        unique_together = [['weekday', 'time']]
        ordering = ['weekday', 'time']
        verbose_name = 'Horario disponible'
        verbose_name_plural = 'Horarios disponibles'

    def __str__(self):
        return f"{self.get_weekday_display()} {self.time.strftime('%H:%M')}"


class BlockedDate(models.Model):
    date = models.DateField('Fecha', unique=True)
    reason = models.CharField('Motivo (opcional)', max_length=200, blank=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Fecha bloqueada'
        verbose_name_plural = 'Fechas bloqueadas'

    def __str__(self):
        label = self.reason or 'Bloqueado'
        return f"{self.date.strftime('%d/%m/%Y')} – {label}"


class Appointment(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente de confirmación'),
        (STATUS_CONFIRMED, 'Confirmada'),
        (STATUS_CANCELLED, 'Cancelada'),
    ]

    name = models.CharField('Nombre', max_length=100)
    email = models.EmailField('Correo electrónico')
    phone = models.CharField('Teléfono', max_length=20)
    date = models.DateField('Fecha')
    time = models.TimeField('Hora')
    notes = models.TextField('Notas', blank=True)
    status = models.CharField(
        'Estado', max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    confirmation_token = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    reminder_sent = models.BooleanField('Recordatorio enviado', default=False)
    created_at = models.DateTimeField('Creado el', auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']
        verbose_name = 'Reunión'
        verbose_name_plural = 'Reuniones'

    def __str__(self):
        return f"{self.name} – {self.date} {self.time.strftime('%H:%M')} ({self.get_status_display()})"

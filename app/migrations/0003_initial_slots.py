"""
Migración de datos: carga los horarios disponibles por defecto.
Lunes a viernes, 09:00 – 17:00 (con pausa de almuerzo 12:00-14:00).
Puedes modificarlos libremente desde el panel de administración Django.
"""
from django.db import migrations
from datetime import time


DEFAULT_SLOTS = [
    # (weekday, hour, minute)
    (0, 9, 0), (0, 10, 0), (0, 11, 0), (0, 14, 0), (0, 15, 0), (0, 16, 0), (0, 17, 0),
    (1, 9, 0), (1, 10, 0), (1, 11, 0), (1, 14, 0), (1, 15, 0), (1, 16, 0), (1, 17, 0),
    (2, 9, 0), (2, 10, 0), (2, 11, 0), (2, 14, 0), (2, 15, 0), (2, 16, 0), (2, 17, 0),
    (3, 9, 0), (3, 10, 0), (3, 11, 0), (3, 14, 0), (3, 15, 0), (3, 16, 0), (3, 17, 0),
    (4, 9, 0), (4, 10, 0), (4, 11, 0), (4, 14, 0), (4, 15, 0), (4, 16, 0), (4, 17, 0),
]


def create_default_slots(apps, schema_editor):
    AvailableSlot = apps.get_model('app', 'AvailableSlot')
    for weekday, hour, minute in DEFAULT_SLOTS:
        AvailableSlot.objects.get_or_create(
            weekday=weekday,
            time=time(hour, minute),
            defaults={'is_active': True},
        )


def remove_default_slots(apps, schema_editor):
    AvailableSlot = apps.get_model('app', 'AvailableSlot')
    AvailableSlot.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_blockeddate_availableslot'),
    ]

    operations = [
        migrations.RunPython(create_default_slots, remove_default_slots),
    ]

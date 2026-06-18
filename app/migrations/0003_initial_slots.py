"""
Migración de datos: carga los horarios disponibles por defecto.
Lunes a viernes, 09:00 – 17:00 (con pausa de almuerzo 12:00-14:00).
Puedes modificarlos libremente desde el panel de administración Django.
"""
from django.db import migrations
from datetime import time


DEFAULT_SLOTS = [
    # (weekday, hour, minute)
    (0, 13, 0), (0, 18, 0), (0, 19, 0),
    (1, 13, 0), (1, 18, 0), (1, 19, 0),
    (2, 13, 0), (2, 18, 0), (2, 19, 0),
    (3, 13, 0), (3, 18, 0), (3, 19, 0),
    (4, 13, 0), (4, 16, 0), (4, 17, 0), (4, 18, 0), (4, 19, 0),
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

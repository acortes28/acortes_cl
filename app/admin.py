from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'date', 'time', 'status', 'reminder_sent', 'created_at']
    list_filter = ['status', 'date', 'reminder_sent']
    search_fields = ['name', 'email', 'phone']
    ordering = ['date', 'time']
    readonly_fields = ['confirmation_token', 'created_at']
    date_hierarchy = 'date'
    list_per_page = 25
    list_editable = ['status']

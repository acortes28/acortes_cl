from django.contrib import admin
from django.utils.html import format_html
from .models import Appointment, AvailableSlot, BlockedDate


# ---------------------------------------------------------------------------
# Acciones reutilizables
# ---------------------------------------------------------------------------

@admin.action(description='Activar horarios seleccionados')
def activate_slots(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='Desactivar horarios seleccionados')
def deactivate_slots(modeladmin, request, queryset):
    queryset.update(is_active=False)


# ---------------------------------------------------------------------------
# Horarios disponibles
# ---------------------------------------------------------------------------

@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ['weekday_label', 'hora', 'estado_badge']
    list_filter = ['weekday', 'is_active']
    list_editable = ['is_active'] if False else []   # se maneja con actions
    ordering = ['weekday', 'time']
    list_per_page = 50
    actions = [activate_slots, deactivate_slots]

    # Columna "Día" con nombre del día
    @admin.display(description='Día', ordering='weekday')
    def weekday_label(self, obj):
        return obj.get_weekday_display()

    # Columna "Hora" formateada
    @admin.display(description='Hora', ordering='time')
    def hora(self, obj):
        return obj.time.strftime('%H:%M') + ' hrs'

    # Columna "Estado" con badge de color
    @admin.display(description='Estado', ordering='is_active', boolean=False)
    def estado_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#dcfce7;color:#16a34a;padding:3px 10px;'
                'border-radius:20px;font-size:12px;font-weight:600;">Activo</span>'
            )
        return format_html(
            '<span style="background:#fee2e2;color:#dc2626;padding:3px 10px;'
            'border-radius:20px;font-size:12px;font-weight:600;">Inactivo</span>'
        )

    def get_list_editable(self, request):
        return ['is_active']

    # Permite editar is_active directamente en la lista
    def get_list_display(self, request):
        return ['weekday_label', 'hora', 'is_active', 'estado_badge']


# ---------------------------------------------------------------------------
# Fechas bloqueadas
# ---------------------------------------------------------------------------

@admin.register(BlockedDate)
class BlockedDateAdmin(admin.ModelAdmin):
    list_display = ['date', 'dia_semana', 'reason']
    search_fields = ['reason']
    ordering = ['date']
    date_hierarchy = 'date'
    list_per_page = 30

    @admin.display(description='Día de la semana')
    def dia_semana(self, obj):
        DAYS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return DAYS[obj.date.weekday()]


# ---------------------------------------------------------------------------
# Reuniones agendadas
# ---------------------------------------------------------------------------

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'date', 'hora_fmt', 'estado_badge', 'status', 'reminder_sent', 'created_at']
    list_filter = ['status', 'date', 'reminder_sent']
    search_fields = ['name', 'email', 'phone']
    ordering = ['date', 'time']
    readonly_fields = ['confirmation_token', 'created_at']
    date_hierarchy = 'date'
    list_per_page = 25
    list_editable = ['status']

    @admin.display(description='Hora', ordering='time')
    def hora_fmt(self, obj):
        return obj.time.strftime('%H:%M') + ' hrs'

    @admin.display(description='Estado', ordering='status', boolean=False)
    def estado_badge(self, obj):
        colors = {
            'pending':   ('#fef9c3', '#92400e'),
            'confirmed': ('#dcfce7', '#16a34a'),
            'cancelled': ('#fee2e2', '#dc2626'),
        }
        bg, fg = colors.get(obj.status, ('#f1f5f9', '#64748b'))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;'
            'border-radius:20px;font-size:12px;font-weight:600;">{}</span>',
            bg, fg, obj.get_status_display()
        )

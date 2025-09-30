from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['provider_name', 'appointment_time', 'client_email', 'payment_status', 'amount', 'created_at']
    list_filter = ['payment_status', 'appointment_time', 'created_at']
    search_fields = ['provider_name', 'client_email']
    readonly_fields = ['stripe_payment_intent_id', 'stripe_checkout_session_id', 'created_at', 'updated_at']
    date_hierarchy = 'appointment_time'

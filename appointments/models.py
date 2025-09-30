from django.db import models
from django.core.validators import EmailValidator

class Appointment(models.Model):
    provider_name = models.CharField(max_length=100)
    appointment_time = models.DateTimeField()
    client_email = models.EmailField(validators=[EmailValidator()])
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_checkout_session_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment with {self.provider_name} on {self.appointment_time}"

    class Meta:
        ordering = ['-appointment_time']

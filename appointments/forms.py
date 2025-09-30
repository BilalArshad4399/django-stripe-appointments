from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['provider_name', 'appointment_time', 'client_email']
        widgets = {
            'provider_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter provider name'
            }),
            'appointment_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
        }
        labels = {
            'provider_name': 'Healthcare Provider Name',
            'appointment_time': 'Appointment Date & Time',
            'client_email': 'Your Email Address',
        }
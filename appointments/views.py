from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from .models import Appointment
from .forms import AppointmentForm

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    appointments = Appointment.objects.all()[:5]
    return render(request, 'appointments/home.html', {
        'appointments': appointments
    })

def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            request.session['appointment_id'] = appointment.id
            return redirect('appointments:payment', appointment_id=appointment.id)
    else:
        form = AppointmentForm()

    return render(request, 'appointments/create_appointment.html', {
        'form': form,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

def payment_page(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Appointment with {appointment.provider_name}',
                            'description': f'Scheduled for {appointment.appointment_time}',
                        },
                        'unit_amount': int(appointment.amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('appointments:payment_success', kwargs={'appointment_id': appointment.id})
                ) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(
                    reverse('appointments:payment_cancel', kwargs={'appointment_id': appointment.id})
                ),
                customer_email=appointment.client_email,
            )

            appointment.stripe_checkout_session_id = checkout_session.id
            appointment.save()

            return redirect(checkout_session.url, code=303)

        except stripe.error.StripeError as e:
            messages.error(request, f'Payment error: {str(e)}')
            return redirect('appointments:payment', appointment_id=appointment.id)

    return render(request, 'appointments/payment.html', {
        'appointment': appointment,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'amount': appointment.amount
    })

def payment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    session_id = request.GET.get('session_id')

    if session_id and appointment.stripe_checkout_session_id == session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                appointment.payment_status = 'paid'
                appointment.save()
                messages.success(request, 'Payment successful! Your appointment is confirmed.')
        except stripe.error.StripeError as e:
            messages.error(request, f'Error verifying payment: {str(e)}')

    return render(request, 'appointments/payment_success.html', {
        'appointment': appointment
    })

def payment_cancel(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.payment_status = 'cancelled'
    appointment.save()
    messages.warning(request, 'Payment was cancelled.')

    return render(request, 'appointments/payment_cancel.html', {
        'appointment': appointment
    })

def appointment_list(request):
    appointments = Appointment.objects.all()

    # Calculate counts for each status
    paid_count = appointments.filter(payment_status='paid').count()
    pending_count = appointments.filter(payment_status='pending').count()
    cancelled_count = appointments.filter(payment_status='cancelled').count()

    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments,
        'paid_count': paid_count,
        'pending_count': pending_count,
        'cancelled_count': cancelled_count,
    })

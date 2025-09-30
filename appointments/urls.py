from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_appointment, name='create'),
    path('payment/<int:appointment_id>/', views.payment_page, name='payment'),
    path('payment/success/<int:appointment_id>/', views.payment_success, name='payment_success'),
    path('payment/cancel/<int:appointment_id>/', views.payment_cancel, name='payment_cancel'),
    path('list/', views.appointment_list, name='list'),
]
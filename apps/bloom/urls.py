from django.urls import path
from . import views

app_name = "bloom"

urlpatterns = [
    path('payment/new/', views.payment_new, name='payment_new'),
    path('payment/<int:pk>/pay/', views.payment_pay, name='payment_pay'),
]

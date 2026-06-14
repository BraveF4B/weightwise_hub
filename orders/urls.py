from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('verify/<str:reference>/', views.verify_payment, name='verify_payment'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
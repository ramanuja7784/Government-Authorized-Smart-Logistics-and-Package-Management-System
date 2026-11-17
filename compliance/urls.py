from django.urls import path
from . import views

app_name = 'compliance'

urlpatterns = [
    path('pending/', views.pending_approvals, name='pending'),
    path('approve/<str:tracking_number>/', views.approve_shipment, name='approve'),
    path('reject/<str:tracking_number>/', views.reject_shipment, name='reject'),
]

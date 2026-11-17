from django.urls import path
from . import views

app_name = "shipments"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/", views.create_shipment, name="create"),
    path("track/", views.public_track, name="public_track"),
    path("<str:tracking_number>/", views.shipment_detail, name="detail"),
    path("<str:tracking_number>/update-status/", views.update_status, name="update_status"),
    path(
    "delete/<str:tracking_number>/",
    views.delete_shipment,
    name="delete"
),

    


]

from django.urls import path
from . import views

app_name = "delivery"

urlpatterns = [
    path("dashboard/", views.delivery_dashboard, name="dashboard"),
    path(
        "update/<str:tracking_number>/",
        views.update_delivery_status,
        name="update_status"
    ),
    path(
        "accept/<str:tracking_number>/",
        views.accept_delivery,
        name="accept_delivery"
    ),
]

from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("delivery-boys/", views.delivery_boy_list, name="delivery_boy_list"),
    path("delivery-boys/create/", views.create_delivery_boy, name="create_delivery_boy"),
    path("notifications/read/", views.mark_notifications_read, name="mark_notifications_read"),
]

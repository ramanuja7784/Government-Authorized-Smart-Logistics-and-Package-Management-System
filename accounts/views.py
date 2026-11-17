from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, DeliveryBoyCreateForm
from django.contrib.auth import get_user_model
from shipments.models import DeliveryAssignment

User = get_user_model()

@login_required
def delivery_boy_list(request):
    if not request.user.is_admin():
        return redirect("shipments:dashboard")

    delivery_boys = User.objects.filter(role="DELIVERY_BOY")

    delivery_boys_data = []
    for boy in delivery_boys:
        is_busy = DeliveryAssignment.objects.filter(
            delivery_boy=boy,
            completed=False
        ).exists()
        delivery_boys_data.append({
            'boy': boy,
            'is_busy': is_busy
        })

    return render(request, "accounts/delivery_boy_list.html", {
        "delivery_boys_data": delivery_boys_data
    })

@login_required
def create_delivery_boy(request):
    if not request.user.is_admin():
        return redirect("shipments:dashboard")

    if request.method == "POST":
        form = DeliveryBoyCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Delivery boy account created successfully.")
            return redirect("accounts:delivery_boy_list")
    else:
        form = DeliveryBoyCreateForm()

    return render(request, "accounts/create_delivery_boy.html", {"form": form})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")

def user_logout(request):
    logout(request)
    return redirect("accounts:login")

@login_required
def mark_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

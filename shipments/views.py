from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from reports.models import AuditLog
from shipments.models import Shipment  # ✅ Use relative import
from shipments.forms import ShipmentForm
from ml.fraud_detector import calculate_risk_score


@login_required
def dashboard(request):
    if request.user.is_govt_auth():
        return redirect("compliance:pending")

    if request.user.is_superuser or request.user.is_staff:
        shipments = Shipment.objects.all().order_by('-id')
    elif request.user.is_courier():
        shipments = Shipment.objects.filter(courier=request.user).order_by('-id')
    else:
        # Others see nothing here
        shipments = Shipment.objects.none()

    return render(request, "shipments/dashboard.html", {"shipments": shipments})


@login_required
def create_shipment(request):


    if not (request.user.is_courier() or request.user.is_staff):
        messages.error(request, "You are not authorized to create shipments.")
        return redirect("shipments:dashboard")
    
    if request.method == "POST":
        form = ShipmentForm(request.POST, request.FILES)
        if form.is_valid():
            shipment = form.save(commit=False)

            # Assign courier
            shipment.courier = request.user if request.user.is_courier() else None

            # Reconstruct addresses for AI risk detection
            sender_full_addr = f"{shipment.sender_house_no} {shipment.sender_street} {shipment.sender_city} {shipment.sender_state} {shipment.sender_pincode}"
            receiver_full_addr = f"{shipment.receiver_house_no} {shipment.receiver_street} {shipment.receiver_city} {shipment.receiver_state} {shipment.receiver_pincode}"

            # AI fraud detection
            risk, details = calculate_risk_score(
                shipment.weight_kg,
                shipment.declared_value,
                shipment.sender_city,
                shipment.receiver_city,
            )

            shipment.risk_score = risk
            shipment.risk_details = details
            shipment.status = "PENDING_APPROVAL"
            shipment.save()
            AuditLog.objects.create(
                user=request.user,
                shipment=shipment,
                action="CREATED",
                details="Shipment created by courier"
            )

            # --- Notification Trigger ---
            from accounts.models import Notification
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            for gu in User.objects.filter(role="govt_auth"):
                Notification.objects.create(
                    user=gu,
                    message=f"NEW SHIPMENT: Shipment {shipment.tracking_number} created and awaits your approval (Risk: {risk}).",
                    link="/compliance/pending/"
                )

            messages.success(request, "Shipment created successfully.")
            return redirect("shipments:dashboard")
    else:
        form = ShipmentForm()


    return render(request, "shipments/create_shipment.html", {"form": form})


from reports.models import AuditLog

def shipment_detail(request, tracking_number):
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)

    audit_logs = shipment.audit_logs.select_related("user").order_by("-timestamp")

    return render(request, "shipments/shipment_detail.html", {
        "shipment": shipment,
        "audit_logs": audit_logs
    })


def public_track(request):
    tracking_number = request.GET.get("tracking_number")
    shipment = None
    if tracking_number:
        shipment = Shipment.objects.filter(tracking_number=tracking_number).first()

    return render(request, "shipments/public_track.html", {"shipment": shipment})


@login_required
def update_status(request, tracking_number):
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)

    if not (request.user.is_staff or request.user == shipment.courier):
        messages.error(request, "Unauthorized access.")
        return redirect("shipments:dashboard")
    
    if request.method == "POST":
        new_status = request.POST.get("status")
        
        # Enforce strict sequential state transitions
        transition_map = {
            "IN_TRANSIT": "OUT_FOR_DELIVERY",
            "OUT_FOR_DELIVERY": "DELIVERED",
        }
        
        current_status = shipment.status
        
        if current_status in transition_map and new_status == transition_map[current_status]:
            shipment.status = new_status
            shipment.save()

            AuditLog.objects.create(
                user=request.user,
                shipment=shipment,
                action="STATUS_UPDATE",
                details=f"Status changed to {new_status}"
            )

            messages.success(request, f"Status updated to {new_status}")
        else:
            messages.error(request, f"Invalid status transition from {current_status} to {new_status}.")
        return redirect("shipments:dashboard")

    return render(request, "shipments/update_status.html", {"shipment": shipment})

@login_required
def delete_shipment(request, tracking_number):
    shipment = get_object_or_404(
        Shipment,
        tracking_number=tracking_number,
        courier=request.user
    )

    # ❌ Safety check
    if shipment.status != "REJECTED":
        messages.error(request, "Only rejected shipments can be deleted.")
        return redirect("shipments:dashboard")

    # 🧾 Audit log
    AuditLog.objects.create(
        user=request.user,
        shipment=shipment,
        action="DELETED",
        details="Courier deleted rejected shipment"
    )

    shipment.delete()
    messages.success(request, "Rejected shipment deleted successfully.")
    return redirect("shipments:dashboard")

@login_required
def home(request):
    if request.user.is_delivery_boy():
        return redirect("delivery:dashboard")
    elif request.user.is_courier():
        return redirect("shipments:dashboard")
    elif request.user.is_govt_auth():
        return redirect("compliance:pending")
    elif request.user.is_superuser or request.user.is_staff or request.user.is_admin():
        return redirect("reports:dashboard")
    
    return render(request, "home.html")

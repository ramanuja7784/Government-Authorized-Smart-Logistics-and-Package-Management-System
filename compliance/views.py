from urllib import request
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from shipments.models import DeliveryAssignment
from shipments.utils import get_free_delivery_boy
from shipments.models import Shipment
from .models import ComplianceCheck
from reports.models import AuditLog




@login_required
def pending_approvals(request):
    if not request.user.is_govt_auth():
        return redirect('shipments:dashboard')

    # ✅ CORRECT STATUS
    pending_shipments = Shipment.objects.filter(status='PENDING_APPROVAL')
    high_risk_pending = pending_shipments.filter(risk_score='HIGH')

    # Fetch shipments approved by this logged-in government user
    my_approved = ComplianceCheck.objects.filter(approved_by=request.user).select_related('shipment').order_by('-id')

    return render(request, 'compliance/pending_approvals.html', {
        'pending_shipments': pending_shipments,
        'high_risk_pending': high_risk_pending,
        'my_approved': my_approved
    })


@login_required
def approve_shipment(request, tracking_number):
    if not request.user.is_govt_auth():
        return redirect("shipments:dashboard")

    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)

    if shipment.status != "PENDING_APPROVAL":
        messages.warning(request, "Shipment already processed.")
        return redirect("compliance:pending")

    check, _ = ComplianceCheck.objects.get_or_create(shipment=shipment)
    check.approved_by = request.user
    check.has_valid_invoice = True
    check.has_complete_address = True
    check.contains_restricted_items = False
    check.save()

    shipment.status = "APPROVED"
    shipment.save()

    AuditLog.objects.create(
        user=request.user,
        shipment=shipment,
        action="APPROVED",
        details="Approved after compliance verification"
    )
    from accounts.models import Notification, User
    # 1. Notify the Courier who created it
    if shipment.courier:
        Notification.objects.create(
            user=shipment.courier,
            message=f"Shipment {shipment.tracking_number} was APPROVED and is ready for delivery.",
            link="/shipments/dashboard/"
        )
    # 2. Notify all active Delivery Boys
    delivery_boys = User.objects.filter(role="DELIVERY_BOY", is_active=True)
    for boy in delivery_boys:
        Notification.objects.create(
            user=boy,
            message=f"NEW SHIPMENT AVAILABLE: Shipment {shipment.tracking_number} is ready for delivery.",
            link="/delivery/dashboard/"
        )

    messages.success(request, "Shipment approved successfully.")
    return redirect("compliance:pending")


@login_required
def reject_shipment(request, tracking_number):
    if not request.user.is_govt_auth():
        return redirect("shipments:dashboard")

    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)

    if shipment.status != "PENDING_APPROVAL":
        messages.warning(request, "Shipment already processed.")
        return redirect("compliance:pending")

    shipment.status = "REJECTED"
    shipment.save()

    AuditLog.objects.create(
        user=request.user,
        shipment=shipment,
        action="REJECTED",
        details="Rejected after compliance verification"
    )

    from accounts.models import Notification
    if shipment.courier:
        Notification.objects.create(
            user=shipment.courier,
            message=f"ALERT: Shipment {shipment.tracking_number} was REJECTED by Government Auth.",
            link="/shipments/dashboard/"
        )

    messages.error(request, "Shipment rejected.")
    return redirect("compliance:pending")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from shipments.models import Shipment, DeliveryAssignment
from reports.models import AuditLog


@login_required
def delivery_dashboard(request):
    if not request.user.is_delivery_boy():
        return redirect("shipments:dashboard")

    # Fetch all unassigned approved shipments that any delivery boy can claim
    available_shipments = Shipment.objects.filter(status="APPROVED").order_by("-id")

    assignments = DeliveryAssignment.objects.filter(
        delivery_boy=request.user,
        completed=False,
        shipment__status__in=["IN_TRANSIT", "OUT_FOR_DELIVERY"]
    ).select_related("shipment")

    completed_count = DeliveryAssignment.objects.filter(
        delivery_boy=request.user,
        completed=True
    ).count()

    return render(request, "delivery/dashboard.html", {
        "assignments": assignments,
        "completed_count": completed_count,
        "available_shipments": available_shipments
    })


@login_required
def accept_delivery(request, tracking_number):
    if not request.user.is_delivery_boy():
        return redirect("shipments:dashboard")

    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)

    if shipment.status != "APPROVED":
        messages.error(request, "This shipment is not available for claiming.")
        return redirect("delivery:dashboard")

    # Ensure no existing delivery assignment exists
    if DeliveryAssignment.objects.filter(shipment=shipment).exists():
        messages.error(request, "This shipment has already been assigned.")
        return redirect("delivery:dashboard")

    # Create the assignment
    DeliveryAssignment.objects.create(
        delivery_boy=request.user,
        shipment=shipment
    )
    shipment.status = "IN_TRANSIT"
    shipment.save()

    # Log the action
    AuditLog.objects.create(
        user=request.user,
        shipment=shipment,
        action="STATUS_UPDATE",
        details=f"Accepted and claimed by delivery boy {request.user.username}"
    )

    messages.success(request, f"Shipment {tracking_number} accepted successfully. It is now in transit.")
    return redirect("delivery:dashboard")
@login_required
def update_delivery_status(request, tracking_number):
    assignment = get_object_or_404(
        DeliveryAssignment,
        shipment__tracking_number=tracking_number,
        delivery_boy=request.user,
        completed=False
    )

    shipment = assignment.shipment

    if request.method == "POST":
        new_status = request.POST.get("status")

        allowed = {
            "IN_TRANSIT": "OUT_FOR_DELIVERY",
            "OUT_FOR_DELIVERY": "DELIVERED",
        }

        if shipment.status in allowed and new_status == allowed[shipment.status]:
            shipment.status = new_status
            shipment.save()

            AuditLog.objects.create(
                user=request.user,
                shipment=shipment,
                action="STATUS_UPDATE",
                details=f"Delivery boy updated status to {new_status}"
            )

            from accounts.models import Notification
            if shipment.courier:
                Notification.objects.create(
                    user=shipment.courier,
                    message=f"Update: Shipment {shipment.tracking_number} is now {new_status} by Delivery Boy {request.user.username}.",
                    link="/shipments/dashboard/"
                )

            if new_status == "DELIVERED":
                assignment.completed = True
                assignment.save()
                
                # Add commission to vault
                from decimal import Decimal
                commission_amount = Decimal('50.00')
                request.user.vault_balance += commission_amount
                request.user.save(update_fields=['vault_balance'])

                messages.success(request, f"Shipment delivered successfully 🎉 ₹{commission_amount} added to your vault!")
            else:
                messages.success(request, f"Shipment updated to {new_status} successfully!")
                
            return redirect("delivery:dashboard")

        messages.error(request, "Invalid status update.")

    return render(request, "delivery/update_status.html", {
        "shipment": shipment
    })

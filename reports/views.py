from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from shipments.models import Shipment
from billing.models import Invoice

from reports.models import AuditLog

from django.db.models import Sum 


@login_required
def reports(request):
    if not (request.user.is_superuser or request.user.is_staff or request.user.is_courier()):
        return redirect("shipments:dashboard")

    if request.user.is_courier():
        shipments = Shipment.objects.filter(courier=request.user)
        delivered_shipments = shipments.filter(status="DELIVERED")


        courier_revenue = Invoice.objects.filter(
        shipment__courier=request.user,
            shipment__status="DELIVERED"
        ).aggregate(
            total=Sum("total_amount")
        )["total"] or 0
        context = {
            "total_shipments": shipments.count(),
            "pending_count": shipments.filter(status="PENDING_APPROVAL").count(),
            "approved_count": shipments.filter(status="APPROVED").count(),
            "delivered_count": shipments.filter(status="DELIVERED").count(),
            "high_risk_shipments": shipments.filter(risk_score="HIGH").count(),
            "shipments": shipments.order_by("-updated_at")[:10],
            "courier_revenue": courier_revenue,   # ✅ IMPORTANT
        }

    else:
        total_revenue = Invoice.objects.filter(
        shipment__status="DELIVERED"
        ).aggregate(
            total=Sum("total_amount")
        )["total"] or 0
        context = {
            "total_shipments": Shipment.objects.count(),
            "pending_count": Shipment.objects.filter(status="PENDING_APPROVAL").count(),
            "approved_count": Shipment.objects.filter(status="APPROVED").count(),
            "delivered_count": Shipment.objects.filter(status="DELIVERED").count(),
            "total_revenue": total_revenue,
        }

    return render(request, "reports/dashboard.html", context)

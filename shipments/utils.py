from django.contrib.auth import get_user_model
from shipments.models import DeliveryAssignment

User = get_user_model()

def get_free_delivery_boy():
    delivery_boys = User.objects.filter(
        role="DELIVERY_BOY",
        is_active=True
    )

    if not delivery_boys.exists():
        return None

    # Find the delivery boy with the fewest active (incomplete) assignments
    from django.db.models import Count, Q
    boy_with_least_jobs = delivery_boys.annotate(
        active_jobs=Count('assigned_deliveries', filter=Q(assigned_deliveries__completed=False))
    ).order_by('active_jobs').first()

    return boy_with_least_jobs

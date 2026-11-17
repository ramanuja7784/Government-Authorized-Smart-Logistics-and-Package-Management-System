from django.contrib import admin
from django.urls import path, include
from shipments.views import home 

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("shipments/", include("shipments.urls")),
    path("billing/", include("billing.urls")),
    path("compliance/", include("compliance.urls")),
    path("reports/", include("reports.urls")),
    path("delivery/", include("delivery.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

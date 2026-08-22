from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("apps.core.api.urls")),
    path("api/v1/admin/lab/", include("apps.demo_lab.api.urls")),
    path("api/v1/auth/", include("apps.identity.api.urls")),
    path("api/v1/", include("apps.referrals.api.urls")),
]

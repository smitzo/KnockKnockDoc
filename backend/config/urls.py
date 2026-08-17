from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("apps.core.api.urls")),
    path("api/v1/", include("apps.referrals.api.urls")),
]

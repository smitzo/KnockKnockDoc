from django.urls import path

from .views import PartnerApplicationCreateView


urlpatterns = [
    path("applications/", PartnerApplicationCreateView.as_view(), name="partner-application"),
]

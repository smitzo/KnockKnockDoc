from django.urls import path

from .views import HealthView, ProductModeView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("product-mode/", ProductModeView.as_view(), name="product-mode"),
]

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import DemoWorkspaceView, ReferralCaseViewSet

router = SimpleRouter()
router.register("cases", ReferralCaseViewSet, basename="case")

urlpatterns = [
    path("", include(router.urls)),
    path("demo/workspace/", DemoWorkspaceView.as_view(), name="demo-workspace"),
]

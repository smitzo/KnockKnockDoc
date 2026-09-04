from django.urls import path

from .views import (
    ApplicationReviewActionView,
    ApplicationReviewDetailView,
    ApplicationReviewListView,
    PartnerApplicationCreateView,
)


urlpatterns = [
    path("applications/", PartnerApplicationCreateView.as_view(), name="partner-application"),
    path(
        "review/applications/",
        ApplicationReviewListView.as_view(),
        name="application-review-list",
    ),
    path(
        "review/applications/<uuid:application_id>/",
        ApplicationReviewDetailView.as_view(),
        name="application-review-detail",
    ),
    path(
        "review/applications/<uuid:application_id>/<str:action>/",
        ApplicationReviewActionView.as_view(),
        name="application-review-action",
    ),
]

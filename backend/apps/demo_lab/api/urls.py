from django.urls import path

from .views import AdminLabSummaryView, SyntheticDoctorListView, SyntheticPatientListView

urlpatterns = [
    path("summary/", AdminLabSummaryView.as_view(), name="admin-lab-summary"),
    path("doctors/", SyntheticDoctorListView.as_view(), name="admin-lab-doctors"),
    path("patients/", SyntheticPatientListView.as_view(), name="admin-lab-patients"),
]

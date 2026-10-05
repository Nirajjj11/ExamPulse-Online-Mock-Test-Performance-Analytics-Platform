from django.urls import path

from .views import CandidateDashboardView


app_name = "dashboard"


urlpatterns = [
      path("",CandidateDashboardView.as_view(),name="candidate",),
]
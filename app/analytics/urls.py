from django.urls import path

from .views import CandidateAnalyticsView


app_name = "analytics"

urlpatterns = [
      path("",CandidateAnalyticsView.as_view(),name="dashboard",),
]
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class CandidateDashboardView(LoginRequiredMixin,TemplateView,):      

      template_name = "dashboard/candidate_dashboard.html"
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .services.performance import PerformanceAnalytics


class CandidateAnalyticsView(LoginRequiredMixin, TemplateView):
      template_name = "analytics/dashboard.html"

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            analytics = PerformanceAnalytics(
                  self.request.user
            )

            context["overall"] = (
                  analytics.overall_performance()
            )

            context["subjects"] = (
                  analytics.subject_performance()
            )

            context["difficulties"] = (
                  analytics.difficulty_performance()
            )

            context["trend"] = (
                  analytics.score_trend()
            )

            strong_weak = (
                  analytics.strong_and_weak_subjects()
            )

            context["strong_subjects"] = (
                  strong_weak["strong"]
            )

            context["weak_subjects"] = (
                  strong_weak["weak"]
            )

            return context
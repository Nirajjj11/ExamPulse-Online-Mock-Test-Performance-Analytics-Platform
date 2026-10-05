from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from attempts.models import TestAttempt
from exam_tests.models import Test

class CandidateDashboardView(
      LoginRequiredMixin,
      TemplateView,
      ):
      template_name = "dashboard/candidate_dashboard.html"


      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            today = timezone.localdate()
            now = timezone.localtime()

            published_tests = (
                  Test.objects
                  .filter(
                        status=Test.Status.PUBLISHED,
                        is_active=True,
                  )
                  .select_related("series")
                  .order_by(
                        "test_date",
                        "start_time",
                  )
            )

            available_tests = []
            upcoming_tests = []

            for test in published_tests:

                  # No scheduled date means the test is immediately available.
                  if test.test_date is None:
                        available_tests.append(test)
                        continue

                  # Future date = forthcoming.
                  if test.test_date > today:
                        upcoming_tests.append(test)
                        continue

                  # Today's test with a future start time = forthcoming.
                  if (
                        test.test_date == today
                        and test.start_time
                        and now.time() < test.start_time
                  ):
                        upcoming_tests.append(test)
                        continue

                  # Past test or today's test whose start time has arrived.
                  available_tests.append(test)

            previous_attempts = (
                  TestAttempt.objects
                  .filter(
                        candidate=self.request.user,
                        status__in=[
                        TestAttempt.Status.SUBMITTED,
                        TestAttempt.Status.TIMED_OUT,
                        ],
                  )
                  .select_related(
                        "test",
                        "test__series",
                  )
                  .order_by("-submitted_at")
            )

            context["available_tests"] = available_tests
            context["upcoming_tests"] = upcoming_tests
            context["previous_attempts"] = previous_attempts

            return context
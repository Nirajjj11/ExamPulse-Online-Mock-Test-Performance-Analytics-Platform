from django.db import transaction
from django.utils import timezone

from attempts.models import AttemptAnswer, TestAttempt


def is_test_forthcoming(test):
      """
      Returns True when the test has not reached its scheduled
      date/time yet.
      """

      now = timezone.localtime()
      today = now.date()

      # Future date
      if test.test_date and test.test_date > today:
            return True

      # Today's test but start time has not arrived
      if (
            test.test_date == today
            and test.start_time
            and now.time() < test.start_time
      ):
            return True

      return False


def can_start_test(test):
      """
      Returns:
            (True, None)
            OR
            (False, reason)
      """

      if test.status != test.Status.PUBLISHED:
            return False, "This test is not currently published."

      if not test.is_active:
            return False, "This test is currently inactive."

      if is_test_forthcoming(test):
            return False, "This test has not started yet."

      if not test.questions.exists():
            return False, "This test does not contain any questions yet."

      return True, None


@transaction.atomic
def create_or_resume_attempt(candidate, test):
      """
      Resume an existing in-progress attempt.

      If no active attempt exists, create a new attempt and
      initialize answers for all questions.
      """

      existing_attempt = (
            TestAttempt.objects
            .filter(
                  candidate=candidate,
                  test=test,
                  status=TestAttempt.Status.IN_PROGRESS,
            )
            .first()
      )

      if existing_attempt:
            return existing_attempt, False

      completed_attempt = (
            TestAttempt.objects
            .filter(
                  candidate=candidate,
                  test=test,
                  status__in=[
                  TestAttempt.Status.SUBMITTED,
                  TestAttempt.Status.TIMED_OUT,
                  ],
            )
            .exists()
      )

      if completed_attempt:
            return None, False

      questions = test.questions.all().order_by(
            "question_number",
            "id",
      )

      attempt = TestAttempt.objects.create(
            candidate=candidate,
            test=test,
            total_questions=questions.count(),
      )

      AttemptAnswer.objects.bulk_create(
            [
                  AttemptAnswer(
                  attempt=attempt,
                  question=question,
                  )
                  for question in questions
            ]
      )

      return attempt, True


def is_attempt_expired(attempt):
      """
      Determines whether the server-side exam deadline
      has been reached.
      """

      deadline = (
            attempt.started_at
            + timezone.timedelta(
                  minutes=attempt.test.duration_minutes
            )
      )

      return timezone.now() >= deadline
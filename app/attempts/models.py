from django.conf import settings
from django.db import models


class TestAttempt(models.Model):
      class Status(models.TextChoices):
            IN_PROGRESS = "IN_PROGRESS", "In Progress"
            SUBMITTED = "SUBMITTED", "Submitted"
            TIMED_OUT = "TIMED_OUT", "Timed Out"

      candidate = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="test_attempts",
      )

      test = models.ForeignKey(
            "exam_tests.Test",
            on_delete=models.CASCADE,
            related_name="attempts",
      )

      started_at = models.DateTimeField(
            auto_now_add=True,
      )

      submitted_at = models.DateTimeField(
            null=True,
            blank=True,
      )

      status = models.CharField(
            max_length=20,
            choices=Status.choices,
            default=Status.IN_PROGRESS,
      )

      score = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            default=0.00,
      )

      correct_answers = models.PositiveIntegerField(
            default=0,
      )

      incorrect_answers = models.PositiveIntegerField(
            default=0,
      )

      unattempted_answers = models.PositiveIntegerField(
            default=0,
      )

      total_questions = models.PositiveIntegerField(
            default=0,
      )

      percentage = models.DecimalField(
            max_digits=6,
            decimal_places=2,
            default=0.00,
      )

      accuracy = models.DecimalField(
            max_digits=6,
            decimal_places=2,
            default=0.00,
      )

      time_taken_seconds = models.PositiveIntegerField(
            default=0,
      )

      created_at = models.DateTimeField(
            auto_now_add=True,
      )

      updated_at = models.DateTimeField(
            auto_now=True,
      )

      class Meta:
            ordering = ["-started_at"]

            indexes = [
                  models.Index(
                  fields=["candidate", "status"],
                  ),
                  models.Index(
                  fields=["test", "status"],
                  ),
                  models.Index(
                  fields=["started_at"],
                  ),
            ]

      def __str__(self):
            return (
                  f"{self.candidate.username} - "
                  f"{self.test.title}"
            )


class AttemptAnswer(models.Model):
      class SelectedOption(models.TextChoices):
            A = "A", "Option A"
            B = "B", "Option B"
            C = "C", "Option C"
            D = "D", "Option D"

      attempt = models.ForeignKey(
            TestAttempt,
            on_delete=models.CASCADE,
            related_name="answers",
      )

      question = models.ForeignKey(
            "questions.Question",
            on_delete=models.CASCADE,
            related_name="attempt_answers",
      )

      selected_option = models.CharField(
            max_length=1,
            choices=SelectedOption.choices,
            null=True,
            blank=True,
      )

      is_correct = models.BooleanField(
            null=True,
            blank=True,
      )

      marks_obtained = models.DecimalField(
            max_digits=8,
            decimal_places=2,
            default=0.00,
      )

      answered_at = models.DateTimeField(
            null=True,
            blank=True,
      )

      marked_for_review = models.BooleanField(
            default=False,
      )

      class Meta:
            ordering = ["question__question_number"]

            constraints = [
                  models.UniqueConstraint(
                  fields=["attempt", "question"],
                  name="unique_question_per_attempt",
                  ),
            ]

            indexes = [
                  models.Index(
                  fields=["attempt", "question"],
                  ),
                  models.Index(
                  fields=["attempt", "selected_option"],
                  ),
            ]

      def __str__(self):
            return (
                  f"{self.attempt} - "
                  f"Question {self.question.question_number}"
            )
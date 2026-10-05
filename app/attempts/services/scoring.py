from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from attempts.models import TestAttempt


@transaction.atomic
def evaluate_attempt(attempt):
      answers = (
            attempt.answers
            .select_related("question")
            .all()
      )

      correct_count = 0
      incorrect_count = 0
      unattempted_count = 0

      total_score = Decimal("0.00")

      for answer in answers:

            question = answer.question

            if not answer.selected_option:
                  answer.is_correct = None
                  answer.marks_obtained = Decimal("0.00")

                  unattempted_count += 1

            elif answer.selected_option == question.correct_option:
                  answer.is_correct = True
                  answer.marks_obtained = question.marks

                  correct_count += 1
                  total_score += question.marks

            else:
                  answer.is_correct = False
                  answer.marks_obtained = -question.negative_marks

                  incorrect_count += 1
                  total_score -= question.negative_marks

            answer.save(
                  update_fields=[
                  "is_correct",
                  "marks_obtained",
                  ]
            )

      total_questions = answers.count()

      submitted_at = timezone.now()

      time_taken_seconds = max(
            0,
            int(
                  (
                  submitted_at - attempt.started_at
                  ).total_seconds()
            ),
      )

      maximum_marks = sum(
            (
                  answer.question.marks
                  for answer in answers
            ),
            Decimal("0.00"),
      )

      if maximum_marks > 0:
            percentage = (
                  total_score / maximum_marks
            ) * Decimal("100")
      else:
            percentage = Decimal("0.00")

      answered_count = (
            correct_count + incorrect_count
      )

      if answered_count > 0:
            accuracy = (
                  Decimal(correct_count)
                  / Decimal(answered_count)
            ) * Decimal("100")
      else:
            accuracy = Decimal("0.00")

      attempt.score = total_score
      attempt.correct_answers = correct_count
      attempt.incorrect_answers = incorrect_count
      attempt.unattempted_answers = unattempted_count
      attempt.total_questions = total_questions
      attempt.percentage = percentage
      attempt.accuracy = accuracy
      attempt.submitted_at = submitted_at
      attempt.time_taken_seconds = time_taken_seconds
      attempt.status = TestAttempt.Status.SUBMITTED

      attempt.save(
            update_fields=[
                  "score",
                  "correct_answers",
                  "incorrect_answers",
                  "unattempted_answers",
                  "total_questions",
                  "percentage",
                  "accuracy",
                  "submitted_at",
                  "time_taken_seconds",
                  "status",
                  "updated_at",
            ]
      )

      return attempt
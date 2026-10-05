from collections import defaultdict

from django.db.models import Avg

from attempts.models import TestAttempt


class PerformanceAnalytics:

      def __init__(self, candidate):
            self.candidate = candidate

      def get_completed_attempts(self):
            return (
                  TestAttempt.objects
                  .filter(
                  candidate=self.candidate,
                  status__in=[
                        TestAttempt.Status.SUBMITTED,
                        TestAttempt.Status.TIMED_OUT,
                  ],
                  )
                  .select_related(
                  "test",
                  "test__series",
                  )
                  .prefetch_related(
                  "answers__question",
                  )
                  .order_by("submitted_at")
            )

      def overall_performance(self):
            attempts = self.get_completed_attempts()

            if not attempts.exists():
                  return {
                  "total_tests": 0,
                  "average_score": 0,
                  "average_percentage": 0,
                  "average_accuracy": 0,
                  "total_correct": 0,
                  "total_incorrect": 0,
                  "total_unattempted": 0,
                  }

            average_score = (
                  attempts.aggregate(
                  value=Avg("score")
                  )["value"] or 0
            )

            average_percentage = (
                  attempts.aggregate(
                  value=Avg("percentage")
                  )["value"] or 0
            )

            average_accuracy = (
                  attempts.aggregate(
                  value=Avg("accuracy")
                  )["value"] or 0
            )

            return {
                  "total_tests": attempts.count(),
                  "average_score": round(float(average_score), 2),
                  "average_percentage": round(
                  float(average_percentage), 2
                  ),
                  "average_accuracy": round(
                  float(average_accuracy), 2
                  ),
                  "total_correct": sum(
                  attempt.correct_answers
                  for attempt in attempts
                  ),
                  "total_incorrect": sum(
                  attempt.incorrect_answers
                  for attempt in attempts
                  ),
                  "total_unattempted": sum(
                  attempt.unattempted_answers
                  for attempt in attempts
                  ),
            }

      def subject_performance(self):
            attempts = self.get_completed_attempts()

            subjects = defaultdict(
                  lambda: {
                  "total": 0,
                  "correct": 0,
                  "incorrect": 0,
                  "unattempted": 0,
                  "marks": 0,
                  }
            )

            for attempt in attempts:
                  for answer in attempt.answers.all():

                        subject = (
                              answer.question.subject
                              or "General"
                        )

                        data = subjects[subject]

                        data["total"] += 1

                        if answer.selected_option is None:
                              data["unattempted"] += 1

                        elif answer.is_correct:
                              data["correct"] += 1

                        else:
                              data["incorrect"] += 1

                        data["marks"] += float(
                              answer.marks_obtained or 0
                        )

            result = []

            for subject, data in subjects.items():

                  attempted = (
                  data["correct"]
                  + data["incorrect"]
                  )

                  accuracy = (
                  data["correct"] / attempted * 100
                  if attempted
                  else 0
                  )

                  result.append({
                  "subject": subject,
                  "total": data["total"],
                  "correct": data["correct"],
                  "incorrect": data["incorrect"],
                  "unattempted": data["unattempted"],
                  "marks": round(data["marks"], 2),
                  "accuracy": round(accuracy, 2),
                  })

            return sorted(
                  result,
                  key=lambda item: item["accuracy"],
                  reverse=True,
            )

      def difficulty_performance(self):
            attempts = self.get_completed_attempts()

            difficulties = defaultdict(
                  lambda: {
                  "total": 0,
                  "correct": 0,
                  "incorrect": 0,
                  "unattempted": 0,
                  }
            )

            for attempt in attempts:
                  for answer in attempt.answers.all():

                        difficulty = (
                              answer.question.difficulty
                              or "Unknown"
                        )

                        data = difficulties[difficulty]

                        data["total"] += 1

                        if answer.selected_option is None:
                              data["unattempted"] += 1

                        elif answer.is_correct:
                              data["correct"] += 1

                        else:
                              data["incorrect"] += 1

            result = []

            for difficulty, data in difficulties.items():

                  attempted = (
                  data["correct"]
                  + data["incorrect"]
                  )

                  accuracy = (
                  data["correct"] / attempted * 100
                  if attempted
                  else 0
                  )

                  result.append({
                  "difficulty": difficulty,
                  "total": data["total"],
                  "correct": data["correct"],
                  "incorrect": data["incorrect"],
                  "unattempted": data["unattempted"],
                  "accuracy": round(accuracy, 2),
                  })

            return result

      def score_trend(self):
            attempts = self.get_completed_attempts()

            return [
                  {
                  "test": attempt.test.title,
                  "date": attempt.submitted_at,
                  "score": float(attempt.score),
                  "percentage": float(
                        attempt.percentage or 0
                  ),
                  "accuracy": float(
                        attempt.accuracy or 0
                  ),
                  }
                  for attempt in attempts
            ]

      def strong_and_weak_subjects(self):
            subjects = self.subject_performance()

            if not subjects:
                  return {
                  "strong": [],
                  "weak": [],
                  }

            ordered = sorted(
                  subjects,
                  key=lambda item: item["accuracy"],
            )

            return {
                  "strong": list(reversed(ordered[-3:])),
                  "weak": ordered[:3],
            }
from django.contrib import admin

from .models import AttemptAnswer, TestAttempt


class AttemptAnswerInline(admin.TabularInline):
      model = AttemptAnswer
      extra = 0

      readonly_fields = (
            "is_correct",
            "marks_obtained",
            "answered_at",
      )

      autocomplete_fields = (
            "question",
      )


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
      list_display = (
            "candidate",
            "test",
            "status",
            "score",
            "correct_answers",
            "incorrect_answers",
            "unattempted_answers",
            "percentage",
            "accuracy",
            "started_at",
            "submitted_at",
      )

      list_filter = (
            "status",
            "test",
            "started_at",
      )

      search_fields = (
            "candidate__username",
            "candidate__email",
            "test__title",
      )

      readonly_fields = (
            "started_at",
            "submitted_at",
            "score",
            "correct_answers",
            "incorrect_answers",
            "unattempted_answers",
            "total_questions",
            "percentage",
            "accuracy",
            "time_taken_seconds",
            "created_at",
            "updated_at",
      )

      autocomplete_fields = (
            "candidate",
            "test",
      )

      inlines = [
            AttemptAnswerInline,
      ]

      ordering = (
            "-started_at",
      )


@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
      list_display = (
            "attempt",
            "question",
            "selected_option",
            "is_correct",
            "marks_obtained",
            "marked_for_review",
            "answered_at",
      )

      list_filter = (
            "is_correct",
            "marked_for_review",
            "selected_option",
      )

      search_fields = (
            "attempt__candidate__username",
            "question__question",
      )

      autocomplete_fields = (
            "attempt",
            "question",
      )
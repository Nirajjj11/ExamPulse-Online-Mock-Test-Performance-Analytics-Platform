from django.contrib import admin

from .models import Option, Question


class OptionInline(admin.TabularInline):
      model = Option
      extra = 4
      max_num = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
      list_display = (
            "question_number",
            "test",
            "subject",
            "topic",
            "difficulty",
            "correct_option",
            "marks",
            "negative_marks",
      )

      list_filter = (
            "difficulty",
            "subject",
            "topic",
            "test",
      )

      search_fields = (
            "question",
            "subject",
            "topic",
            "test__title",
      )

      ordering = (
            "test",
            "question_number",
      )

      autocomplete_fields = (
            "test",
      )

      inlines = [
            OptionInline,
      ]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
      list_display = (
            "question",
            "label",
            "text",
      )

      list_filter = (
            "label",
      )

      search_fields = (
            "text",
            "question__question",
      )

      autocomplete_fields = (
            "question",
      )
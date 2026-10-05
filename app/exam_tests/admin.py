from django.contrib import admin

from .models import Test, TestSeries


@admin.register(TestSeries)
class TestSeriesAdmin(admin.ModelAdmin):
      list_display = (
            "name",
            "category",
            "is_active",
            "created_at",
      )

      list_filter = (
            "category",
            "is_active",
      )

      search_fields = (
            "name",
            "description",
      )

      prepopulated_fields = {
            "slug": ("name",),
      }

      ordering = (
            "name",
      )

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
      list_display = (
            "title",
            "series",
            "test_date",
            "start_time",
            "duration_minutes",
            "difficulty",
            "status",
            "is_active",
      )

      list_filter = (
            "status",
            "difficulty",
            "is_active",
            "test_date",
            "series",
      )

      search_fields = (
            "title",
            "subject",
            "topic",
            "series__name",
      )

      prepopulated_fields = {
            "slug": ("title",),
      }

      autocomplete_fields = (
            "series",
      )

      ordering = (
            "-test_date",
            "-start_time",
      )
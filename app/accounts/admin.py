from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
      readonly_fields = ("created_at", "updated_at")
      fieldsets = UserAdmin.fieldsets + (
            (
                  "ExamPulse Information",
                  {
                  "fields": (
                        "role",
                        "created_at",
                        "updated_at",
                  )
                  },
            ),
      )

      add_fieldsets = UserAdmin.add_fieldsets + (
            (
                  "ExamPulse Information",
                  {
                  "fields": (
                        "email",
                        "role",
                  )
                  },
            ),
      )

      list_display = (
            "username",
            "email",
            "role",
            "is_staff",
            "is_active",
            "date_joined",
      )

      list_filter = (
            "role",
            "is_staff",
            "is_active",
      )

      search_fields = (
            "username",
            "email",
            "first_name",
            "last_name",
      )
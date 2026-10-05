from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class AdminRequiredMixin(AccessMixin):
      def dispatch(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                  return self.handle_no_permission()

            if not (
                  request.user.is_staff
                  or request.user.role == "ADMIN"
            ):
                  messages.error(
                  request,
                  "You do not have permission to access this page.",
                  )

                  return redirect("dashboard:candidate")

            return super().dispatch(
                  request,
                  *args,
                  **kwargs,
            )
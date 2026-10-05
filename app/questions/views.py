from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from core.mixins import AdminRequiredMixin
from exam_tests.models import Test

from .forms import QuestionCSVUploadForm
from .services.csv_importer import (
    CSVImportError,
    import_questions_from_csv,
)


class QuestionCSVImportView(
      AdminRequiredMixin,
      FormView,
      ):
      template_name = "questions/csv_import.html"
      form_class = QuestionCSVUploadForm

      def dispatch(self, request, *args, **kwargs):
            self.test = Test.objects.get(
                  pk=kwargs["test_id"]
            )

            return super().dispatch(
                  request,
                  *args,
                  **kwargs,
            )

      def form_valid(self, form):
            csv_file = form.cleaned_data["csv_file"]

            try:
                  questions = import_questions_from_csv(
                  test=self.test,
                  uploaded_file=csv_file,
                  )

            except CSVImportError as exc:
                  form.add_error(
                  "csv_file",
                  str(exc),
                  )

                  return self.form_invalid(form)

            messages.success(
                  self.request,
                  (
                        f"{len(questions)} questions imported "
                        f"successfully into '{self.test.title}'."
                  ),
            )

            return redirect(
                  reverse(
                        "questions:csv-import",
                        kwargs={
                              "test_id": self.test.pk,
                        },
                  )
            )
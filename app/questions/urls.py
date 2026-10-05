from django.urls import path

from .views import QuestionCSVImportView


app_name = "questions"


urlpatterns = [
      path("tests/<int:test_id>/import/",QuestionCSVImportView.as_view(),name="csv-import",),
]
from django.urls import path

from .views import (
    AttemptResultView,
    ExamView,
    SaveAnswerView,
    StartTestView,
    SubmitAttemptView,
)

app_name = "attempts"

urlpatterns = [
      path("tests/<int:test_id>/start/",StartTestView.as_view(),name="start",),
      path("<int:attempt_id>/",ExamView.as_view(),name="exam",),
      path("<int:attempt_id>/answer/",SaveAnswerView.as_view(),name="save-answer",),
      path("<int:attempt_id>/submit/",SubmitAttemptView.as_view(),name="submit",),
      path("<int:attempt_id>/result/",AttemptResultView.as_view(),name="result",),
      ]
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, TemplateView

from core.mixins import AdminRequiredMixin
from exam_tests.models import Test

from .models import AttemptAnswer, TestAttempt
from .services.attempt_service import (
      can_start_test,
      create_or_resume_attempt,
      is_attempt_expired,
)
from .services.scoring import evaluate_attempt


class StartTestView(
      LoginRequiredMixin,
      RedirectView,
      ):
      def get_redirect_url(self, *args, **kwargs):
            test = get_object_or_404(
                  Test.objects.select_related("series"),
                  pk=kwargs["test_id"],
            )

            can_start, reason = can_start_test(test)

            if not can_start:
                  messages.error(
                  self.request,
                  reason,
                  )
                  return reverse(
                  "dashboard:candidate"
                  )

            attempt, created = create_or_resume_attempt(
                  candidate=self.request.user,
                  test=test,
            )

            if attempt is None:
                  messages.warning(
                  self.request,
                  "You have already completed this test.",
                  )
                  return reverse(
                  "dashboard:candidate"
                  )

            return reverse(
                  "attempts:exam",
                  kwargs={
                  "attempt_id": attempt.pk,
                  },
            )


class ExamView(
      LoginRequiredMixin,
      DetailView,
      ):
      model = TestAttempt
      template_name = "attempts/exam.html"
      context_object_name = "attempt"

      # Your URL uses <int:attempt_id>, not <int:pk>.
      pk_url_kwarg = "attempt_id"

      def get_queryset(self):
            return (
                  TestAttempt.objects
                  .filter(
                        candidate=self.request.user,
                        status=TestAttempt.Status.IN_PROGRESS,
                  )
                  .select_related(
                        "test",
                        "test__series",
                  )
            )

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            attempt = self.object

            if is_attempt_expired(attempt):
                  evaluate_attempt(attempt)
                  context["attempt_expired"] = True
                  return context

            questions = (
                  attempt.test.questions
                  .prefetch_related("options")
                  .order_by(
                        "question_number",
                        "id",
                  )
            )

            answers = {
                  answer.question_id: answer
                  for answer in (
                        attempt.answers
                        .select_related("question")
                        .all()
                  )
            }

            question_number = self.request.GET.get(
                  "question",
                  "1",
            )

            try:
                  question_number = int(question_number)
            except ValueError:
                  question_number = 1

            current_question = (
                  questions
                  .filter(
                        question_number=question_number
                  )
                  .first()
            )

            if current_question is None:
                  current_question = questions.first()

            current_answer = answers.get(
                  current_question.pk
            )

            question_list = []

            for question in questions:
                  answer = answers.get(question.pk)

                  question_list.append(
                        {
                        "question": question,
                        "answer": answer,
                        }
                  )

            context["questions"] = questions
            context["question_list"] = question_list
            context["current_question"] = current_question
            context["current_answer"] = current_answer
            context["question_count"] = len(question_list)

            return context



class SaveAnswerView(
      LoginRequiredMixin,
      RedirectView,
      ):
      def post(self, request, *args, **kwargs):
            attempt = get_object_or_404(
                  TestAttempt,
                  pk=kwargs["attempt_id"],
                  candidate=request.user,
                  status=TestAttempt.Status.IN_PROGRESS,
            )

            if is_attempt_expired(attempt):
                  evaluate_attempt(attempt)

                  messages.warning(
                  request,
                  "Time is over. Your test has been submitted automatically.",
                  )

                  return redirect(
                  "attempts:result",
                  attempt_id=attempt.pk,
                  )

            question = get_object_or_404(
                  attempt.test.questions,
                  pk=request.POST.get("question_id"),
            )

            answer = get_object_or_404(
                  AttemptAnswer,
                  attempt=attempt,
                  question=question,
            )

            selected_option = (
                  request.POST.get("selected_option")
                  or None
            )

            valid_options = {
                  "A",
                  "B",
                  "C",
                  "D",
            }

            if selected_option not in valid_options:
                  selected_option = None

            answer.selected_option = selected_option
            answer.marked_for_review = (
                  request.POST.get("marked_for_review")
                  == "true"
            )

            if selected_option:
                  from django.utils import timezone

                  answer.answered_at = timezone.now()
            else:
                  answer.answered_at = None

            answer.save(
                  update_fields=[
                  "selected_option",
                  "marked_for_review",
                  "answered_at",
                  ]
            )

            next_question = request.POST.get(
                  "next_question"
            )

            if next_question:
                  return redirect(
                  f"{reverse('attempts:exam', kwargs={'attempt_id': attempt.pk})}"
                  f"?question={next_question}"
                  )

            return redirect(
                  "attempts:exam",
                  attempt_id=attempt.pk,
            )


class SubmitAttemptView(
      LoginRequiredMixin,
      RedirectView,
      ):
      def post(self, request, *args, **kwargs):
            attempt = get_object_or_404(
                  TestAttempt,
                  pk=kwargs["attempt_id"],
                  candidate=request.user,
                  status=TestAttempt.Status.IN_PROGRESS,
            )

            evaluate_attempt(attempt)

            return redirect(
                  "attempts:result",
                  attempt_id=attempt.pk,
            )

class AttemptResultView(LoginRequiredMixin,DetailView,):
      model = TestAttempt
      template_name = "attempts/result.html"
      context_object_name = "attempt"

      
      # URL uses <int:attempt_id>, not <int:pk>
      pk_url_kwarg = "attempt_id"

      def get_queryset(self):
            return (
                  TestAttempt.objects
                  .filter(
                        candidate=self.request.user,
                        status__in=[
                        TestAttempt.Status.SUBMITTED,
                        TestAttempt.Status.TIMED_OUT,
                        ],
                  )
                  .select_related(
                        "test",
                        "test__series",
                  )
            )

      def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            attempt = self.object

            answers = (
                  attempt.answers
                  .select_related("question")
                  .prefetch_related("question__options")
                  .order_by(
                        "question__question_number"
                  )
            )

            context["answers"] = answers

            return context

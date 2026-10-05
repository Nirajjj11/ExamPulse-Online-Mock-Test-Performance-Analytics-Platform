from django.db import models


class Question(models.Model):
      class Difficulty(models.TextChoices):
            EASY = "EASY", "Easy"
            MEDIUM = "MEDIUM", "Medium"
            HARD = "HARD", "Hard"

      class CorrectOption(models.TextChoices):
            A = "A", "Option A"
            B = "B", "Option B"
            C = "C", "Option C"
            D = "D", "Option D"

      test = models.ForeignKey(
            "exam_tests.Test",
            on_delete=models.CASCADE,
            related_name="questions",
      )

      question_number = models.PositiveIntegerField(
            default=1,
      )

      question = models.TextField()

      explanation = models.TextField(
            blank=True,
      )

      subject = models.CharField(
            max_length=100,
            blank=True,
      )

      topic = models.CharField(
            max_length=150,
            blank=True,
      )

      difficulty = models.CharField(
            max_length=20,
            choices=Difficulty.choices,
            default=Difficulty.MEDIUM,
      )

      correct_option = models.CharField(
            max_length=1,
            choices=CorrectOption.choices,
      )

      marks = models.DecimalField(
            max_digits=6,
            decimal_places=2,
            default=1.00,
      )

      negative_marks = models.DecimalField(
            max_digits=6,
            decimal_places=2,
            default=0.00,
      )

      created_at = models.DateTimeField(
            auto_now_add=True,
      )

      updated_at = models.DateTimeField(
            auto_now=True,
      )

      class Meta:
            ordering = [
                  "question_number",
                  "id",
            ]

            indexes = [
                  models.Index(
                        fields=["test", "question_number"],
                  ),
                  models.Index(
                        fields=["subject", "topic"],
                  ),
            ]

            constraints = [
                  models.UniqueConstraint(
                        fields=["test", "question_number"],
                        name="unique_question_number_per_test",
                  ),
            ]

      def __str__(self):
            return f"{self.test.title} - Question {self.question_number}"


class Option(models.Model):
      class OptionLabel(models.TextChoices):
            A = "A", "Option A"
            B = "B", "Option B"
            C = "C", "Option C"
            D = "D", "Option D"

      question = models.ForeignKey(
            Question,
            on_delete=models.CASCADE,
            related_name="options",
      )

      label = models.CharField(
            max_length=1,
            choices=OptionLabel.choices,
      )

      text = models.TextField()

      class Meta:
            ordering = ["label"]

            constraints = [
                  models.UniqueConstraint(
                  fields=["question", "label"],
                  name="unique_question_option_label",
                  ),
            ]

      def __str__(self):
            return f"{self.question} - Option {self.label}"
from django.db import models
from django.utils.text import slugify


class TestSeries(models.Model):
      class Category(models.TextChoices):
            BPSC = "BPSC", "BPSC"
            UPSC = "UPSC", "UPSC"
            SSC = "SSC", "SSC"
            BANKING = "BANKING", "Banking"
            RAILWAY = "RAILWAY", "Railway"
            OTHER = "OTHER", "Other"

      name = models.CharField(
            max_length=200,
      )

      slug = models.SlugField(
            max_length=220,
            unique=True,
            blank=True,
      )

      description = models.TextField(
            blank=True,
      )

      category = models.CharField(
            max_length=20,
            choices=Category.choices,
            default=Category.OTHER,
      )

      is_active = models.BooleanField(
            default=True,
      )

      created_at = models.DateTimeField(
            auto_now_add=True,
      )

      updated_at = models.DateTimeField(
            auto_now=True,
      )

      class Meta:
            ordering = ["name"]
            verbose_name = "Test Series"
            verbose_name_plural = "Test Series"

      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(self.name)

            super().save(*args, **kwargs)

      def __str__(self):
            return self.name


class Test(models.Model):
      class Difficulty(models.TextChoices):
            EASY = "EASY", "Easy"
            MEDIUM = "MEDIUM", "Medium"
            HARD = "HARD", "Hard"

      class Status(models.TextChoices):
            DRAFT = "DRAFT", "Draft"
            PUBLISHED = "PUBLISHED", "Published"
            CLOSED = "CLOSED", "Closed"
            ARCHIVED = "ARCHIVED", "Archived"

      series = models.ForeignKey(
            TestSeries,
            on_delete=models.CASCADE,
            related_name="tests",
      )

      title = models.CharField(
            max_length=200,
      )

      slug = models.SlugField(
            max_length=220,
            blank=True,
      )

      description = models.TextField(
            blank=True,
      )

      test_date = models.DateField(
            null=True,
            blank=True,
      )

      start_time = models.TimeField(
            null=True,
            blank=True,
      )

      duration_minutes = models.PositiveIntegerField(
            default=30,
      )

      marks_per_question = models.DecimalField(
            max_digits=6,
            decimal_places=2,
            default=1.00,
      )

      negative_marks = models.DecimalField(
            max_digits=6,
            decimal_places=2,
            default=0.3333,
      )

      difficulty = models.CharField(
            max_length=20,
            choices=Difficulty.choices,
            default=Difficulty.MEDIUM,
      )

      subject = models.CharField(
            max_length=100,
            blank=True,
      )

      topic = models.CharField(
            max_length=150,
            blank=True,
      )

      instructions = models.TextField(
            blank=True,
      )

      status = models.CharField(
            max_length=20,
            choices=Status.choices,
            default=Status.DRAFT,
      )

      is_active = models.BooleanField(
            default=True,
      )

      created_at = models.DateTimeField(
            auto_now_add=True,
      )

      updated_at = models.DateTimeField(
            auto_now=True,
      )

      class Meta:
            ordering = ["-test_date", "-start_time", "-created_at"]

            indexes = [
                  models.Index(
                  fields=["test_date", "status"],
                  ),
                  models.Index(
                  fields=["series", "status"],
                  ),
            ]

      def save(self, *args, **kwargs):
            if not self.slug:
                  self.slug = slugify(self.title)

            super().save(*args, **kwargs)

      def __str__(self):
            return self.title
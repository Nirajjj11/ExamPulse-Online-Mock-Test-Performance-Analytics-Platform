from django.db import models

# Create your models here.
from django.db import models


class PerformanceRule(models.Model):
      class Level(models.TextChoices):
            EXCELLENT = "EXCELLENT", "Excellent"
            GOOD = "GOOD", "Good"
            AVERAGE = "AVERAGE", "Average"
            NEEDS_IMPROVEMENT = "NEEDS_IMPROVEMENT", "Needs Improvement"
            WEAK = "WEAK", "Weak"

      name = models.CharField(max_length=100)

      level = models.CharField(
            max_length=30,
            choices=Level.choices,
            unique=True,
      )

      min_percentage = models.DecimalField(
            max_digits=5,
            decimal_places=2,
      )

      max_percentage = models.DecimalField(
            max_digits=5,
            decimal_places=2,
      )

      message = models.TextField()

      recommendation = models.TextField(
            blank=True
      )

      is_active = models.BooleanField(
            default=True
      )

      priority = models.PositiveIntegerField(
            default=1
      )

      created_at = models.DateTimeField(
            auto_now_add=True
      )

      updated_at = models.DateTimeField(
            auto_now=True
      )

      class Meta:
            ordering = ["priority", "-min_percentage"]

      def __str__(self):
            return self.name
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
      
      class Role(models.TextChoices):
            CANDIDATE = "CANDIDATE", "Candidate"
            ADMIN = "ADMIN", "Admin"

      email = models.EmailField( unique=True,verbose_name="Email Address",)

      role = models.CharField(max_length=20,choices=Role.choices,default=Role.CANDIDATE,)

      created_at = models.DateTimeField(auto_now_add=True,)

      updated_at = models.DateTimeField(auto_now=True,)

      def __str__(self):
            return self.username
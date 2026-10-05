from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


from .models import User


class RegisterForm(UserCreationForm):
      """
      Registration form for ExamPulse candidates.
      """

      first_name = forms.CharField(
            max_length=150,
            required=True,
            widget=forms.TextInput(
                  attrs={
                  "class": "form-control",
                  "placeholder": "Enter your first name",
                  }
            ),
      )

      last_name = forms.CharField(
            max_length=150,
            required=False,
            widget=forms.TextInput(
                  attrs={
                  "class": "form-control",
                  "placeholder": "Enter your last name",
                  }
            ),
      )

      email = forms.EmailField(
            required=True,
            widget=forms.EmailInput(
                  attrs={
                  "class": "form-control",
                  "placeholder": "Enter your email",
                  }
            ),
      )

      class Meta:
            model = User

            fields = (
                  "username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",
            )

            widgets = {
                  "username": forms.TextInput(
                  attrs={
                        "class": "form-control",
                        "placeholder": "Choose a username",
                  }
                  ),
            }

      def save(self, commit=True):
            """
            Create a candidate account.

            New registrations are always assigned the
            CANDIDATE role.
            """

            user = super().save(commit=False)

            user.role = User.Role.CANDIDATE

            if commit:
                  user.save()

            return user
      

class LoginForm(AuthenticationForm):
      """
      Login form for ExamPulse users.
      """

      username = forms.CharField(
            widget=forms.TextInput(
                  attrs={
                  "class": "form-control",
                  "placeholder": "Enter your username",
                  "autofocus": True,
                  }
            )
      )

      password = forms.CharField(
            widget=forms.PasswordInput(
                  attrs={
                  "class": "form-control",
                  "placeholder": "Enter your password",
                  }
            )
      )
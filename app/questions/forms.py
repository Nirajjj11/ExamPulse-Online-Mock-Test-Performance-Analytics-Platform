from django import forms


class QuestionCSVUploadForm(forms.Form):
      csv_file = forms.FileField(
            label="Question CSV File",
            widget=forms.ClearableFileInput(
                  attrs={
                  "class": "form-control",
                  "accept": ".csv",
                  }
            ),
      )
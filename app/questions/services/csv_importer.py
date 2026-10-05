import csv
import io

from django.db import transaction

from questions.models import Option, Question


REQUIRED_COLUMNS = {
    "question_number",
    "question",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "correct_option",
    "explanation",
    "subject",
    "topic",
    "difficulty",
    "marks",
    "negative_marks",
}

VALID_DIFFICULTIES = {
    "EASY",
    "MEDIUM",
    "HARD",
}

VALID_OPTIONS = {
    "A",
    "B",
    "C",
    "D",
}


class CSVImportError(Exception):
      """Raised when CSV question import validation fails."""


def normalize_value(value):
      if value is None:
            return ""

      return str(value).strip()


def validate_headers(fieldnames):
      if not fieldnames:
            raise CSVImportError(
                  "CSV file does not contain a header row."
            )

      headers = {
            normalize_value(field).lower()
            for field in fieldnames
            if field
      }

      missing_columns = REQUIRED_COLUMNS - headers

      if missing_columns:
            missing = ", ".join(sorted(missing_columns))

            raise CSVImportError(
                  f"Missing required columns: {missing}"
            )


def parse_decimal(value, field_name, row_number):
      value = normalize_value(value)

      if not value:
            raise CSVImportError(
                  f"Row {row_number}: {field_name} cannot be empty."
            )

      try:
            return float(value)
      except ValueError as exc:
            raise CSVImportError(
                  f"Row {row_number}: {field_name} must be a number."
            ) from exc


def parse_integer(value, field_name, row_number):
      value = normalize_value(value)

      if not value:
            raise CSVImportError(
                  f"Row {row_number}: {field_name} cannot be empty."
            )

      try:
            number = int(value)
      except ValueError as exc:
            raise CSVImportError(
                  f"Row {row_number}: {field_name} must be an integer."
            ) from exc

      if number <= 0:
            raise CSVImportError(
                  f"Row {row_number}: {field_name} must be greater than zero."
            )

      return number


@transaction.atomic
def import_questions_from_csv(test, uploaded_file):
      try:
            file_content = uploaded_file.read().decode("utf-8-sig")
      except UnicodeDecodeError as exc:
            raise CSVImportError(
                  "CSV file must be encoded as UTF-8."
            ) from exc

      csv_file = io.StringIO(file_content)

      reader = csv.DictReader(csv_file)

      validate_headers(reader.fieldnames)

      rows = list(reader)

      if not rows:
            raise CSVImportError(
                  "CSV file does not contain any question rows."
            )

      created_questions = []

      for row_index, row in enumerate(rows, start=2):
            question_number = parse_integer(
                  row.get("question_number"),
                  "question_number",
                  row_index,
            )

            question_text = normalize_value(
                  row.get("question")
            )

            if not question_text:
                  raise CSVImportError(
                  f"Row {row_index}: question cannot be empty."
                  )

            option_values = {
                  "A": normalize_value(row.get("option_a")),
                  "B": normalize_value(row.get("option_b")),
                  "C": normalize_value(row.get("option_c")),
                  "D": normalize_value(row.get("option_d")),
            }

            empty_options = [
                  label
                  for label, text in option_values.items()
                  if not text
            ]

            if empty_options:
                  raise CSVImportError(
                  f"Row {row_index}: missing option(s): "
                  f"{', '.join(empty_options)}."
                  )

            correct_option = normalize_value(
                  row.get("correct_option")
            ).upper()

            if correct_option not in VALID_OPTIONS:
                  raise CSVImportError(
                  f"Row {row_index}: correct_option must be "
                  f"A, B, C, or D."
                  )

            difficulty = normalize_value(
                  row.get("difficulty")
            ).upper()

            if difficulty not in VALID_DIFFICULTIES:
                  raise CSVImportError(
                  f"Row {row_index}: difficulty must be "
                  f"EASY, MEDIUM, or HARD."
                  )

            marks = parse_decimal(
                  row.get("marks"),
                  "marks",
                  row_index,
            )

            negative_marks = parse_decimal(
                  row.get("negative_marks"),
                  "negative_marks",
                  row_index,
            )

            if marks < 0:
                  raise CSVImportError(
                  f"Row {row_index}: marks cannot be negative."
                  )

            if negative_marks < 0:
                  raise CSVImportError(
                  f"Row {row_index}: negative_marks cannot be negative."
                  )

            question = Question.objects.create(
                  test=test,
                  question_number=question_number,
                  question=question_text,
                  explanation=normalize_value(
                  row.get("explanation")
                  ),
                  subject=normalize_value(
                  row.get("subject")
                  ),
                  topic=normalize_value(
                  row.get("topic")
                  ),
                  difficulty=difficulty,
                  correct_option=correct_option,
                  marks=marks,
                  negative_marks=negative_marks,
            )

            Option.objects.bulk_create(
                  [
                  Option(
                        question=question,
                        label=label,
                        text=text,
                  )
                  for label, text in option_values.items()
                  ]
            )

            created_questions.append(question)

      return created_questions
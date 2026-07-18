"""
Submission parsing/validation — the single place a survey response payload
is checked and persisted.

Payload shape (JSON, keyed by question ID as a string):

- single:  {"option": <id>}            or {"other": "<text>"}
- multi:   {"options": [<id>, …], "other": "<text>?"}
- matrix:  {"rows": {"<row_id>": <option_id>, …}}
- rank:    {"ranked": [<id-or-"other">, …]}, "other": "<text>?"}  (index 0 = 1st)
- text:    {"text": "<text>"}
"""
from django.db import IntegrityError, transaction

from .models import QuestionKind, SurveyAnswer, SurveySubmission

# Free-text and "Other" write-ins are capped server-side; the form mirrors
# this with maxlength.
MAX_TEXT = 4000
MAX_OTHER = 255


class SubmissionError(Exception):
    """Validation failure: `errors` maps question_id (str) → message."""

    def __init__(self, message: str, errors: dict | None = None):
        super().__init__(message)
        self.message = message
        self.errors = errors or {}


def _clean_other(raw, errors: dict, qid: str) -> str:
    text = str(raw or "").strip()
    if len(text) > MAX_OTHER:
        errors[qid] = f"Keep the “Other” text under {MAX_OTHER} characters."
    return text


def _validate_question(question, data, errors: dict) -> list[dict]:
    """Return SurveyAnswer kwargs for one question, collecting any errors."""
    qid = str(question.question_id)
    choices = {o.option_id: o for o in question.choices}
    answers = []

    if question.kind == QuestionKind.TEXT:
        text = str(data.get("text") or "").strip()
        if len(text) > MAX_TEXT:
            errors[qid] = f"Keep this answer under {MAX_TEXT} characters."
        elif text:
            answers.append({"text": text})
        elif question.required:
            errors[qid] = "An answer is required here."

    elif question.kind == QuestionKind.SINGLE:
        option_id = data.get("option")
        other = _clean_other(data.get("other"), errors, qid)
        if option_id is not None:
            if option_id not in choices:
                errors[qid] = "Pick one of the listed options."
            else:
                answers.append({"option": choices[option_id]})
        elif other and question.allow_other:
            answers.append({"text": other})
        elif question.required:
            errors[qid] = "Pick an option."

    elif question.kind == QuestionKind.MULTI:
        picked = data.get("options") or []
        other = _clean_other(data.get("other"), errors, qid)
        if not isinstance(picked, list) or len(set(picked)) != len(picked):
            errors[qid] = "Invalid selection."
            return []
        total = len(picked) + (1 if other and question.allow_other else 0)
        if question.max_choices and total > question.max_choices:
            errors[qid] = f"Pick at most {question.max_choices}."
            return []
        for option_id in picked:
            if option_id not in choices:
                errors[qid] = "Pick from the listed options."
                return []
            answers.append({"option": choices[option_id]})
        if other and question.allow_other:
            answers.append({"text": other})
        if not answers and question.required:
            errors[qid] = "Pick at least one option."

    elif question.kind == QuestionKind.MATRIX:
        rows = {o.option_id: o for o in question.matrix_rows}
        rated = data.get("rows") or {}
        if not isinstance(rated, dict):
            errors[qid] = "Invalid ratings."
            return []
        for row_key, option_id in rated.items():
            try:
                row_id = int(row_key)
            except (TypeError, ValueError):
                errors[qid] = "Invalid ratings."
                return []
            if row_id not in rows or option_id not in choices:
                errors[qid] = "Invalid ratings."
                return []
            answers.append({"row": rows[row_id], "option": choices[option_id]})
        if question.required and len(answers) < len(rows):
            errors[qid] = "Rate every row."

    elif question.kind == QuestionKind.RANK:
        ranked = data.get("ranked") or []
        other = _clean_other(data.get("other"), errors, qid)
        limit = question.max_choices or len(choices)
        if not isinstance(ranked, list) or len(ranked) > limit:
            errors[qid] = f"Rank at most {limit}."
            return []
        if len(set(map(str, ranked))) != len(ranked):
            errors[qid] = "Each pick can only hold one rank."
            return []
        for position, pick in enumerate(ranked, start=1):
            if pick == "other" and question.allow_other:
                if not other:
                    errors[qid] = "Fill in the “Other” text for its ranked slot."
                    return []
                answers.append({"text": other, "rank": position})
            elif pick in choices:
                answers.append({"option": choices[pick], "rank": position})
            else:
                errors[qid] = "Rank from the listed options."
                return []
        if question.required and not answers:
            errors[qid] = "Rank at least your first pick."

    return answers


def save_submission(survey, account, payload: dict) -> SurveySubmission:
    """Validate a full response payload and persist it atomically."""
    if not survey.is_accepting():
        raise SubmissionError("This survey is not accepting responses.")
    if survey.submissions.filter(account=account).exists():
        raise SubmissionError("You have already answered this survey.")
    if not isinstance(payload, dict):
        raise SubmissionError("Malformed submission.")

    questions = survey.questions.prefetch_related("options")
    errors: dict = {}
    validated = []
    for question in questions:
        data = payload.get(str(question.question_id)) or {}
        if not isinstance(data, dict):
            errors[str(question.question_id)] = "Malformed answer."
            continue
        for kwargs in _validate_question(question, data, errors):
            validated.append({"question": question, **kwargs})

    if errors:
        raise SubmissionError("Please fix the highlighted questions.", errors)

    try:
        with transaction.atomic():
            submission = SurveySubmission.objects.create(
                survey=survey, account=account,
            )
            SurveyAnswer.objects.bulk_create(
                SurveyAnswer(submission=submission, **kwargs)
                for kwargs in validated
            )
    except IntegrityError as exc:
        # Double-submit race: the unique constraint is the backstop.
        raise SubmissionError("You have already answered this survey.") from exc
    return submission

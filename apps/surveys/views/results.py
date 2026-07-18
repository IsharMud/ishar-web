"""
Staff results dashboard: per-question aggregates computed in Python — the
playerbase is tiny, so one pass over all answers beats aggregate-query
gymnastics and keeps every kind's shape explicit.
"""
import csv

from django.http import Http404, HttpResponse
from django.views.generic.base import TemplateView

from apps.core.views.mixins import EternalRequiredMixin, NeverCacheMixin

from ..models import QuestionKind, Survey, SurveyAnswer, SurveySubmission


class SurveyResultsBase(EternalRequiredMixin, NeverCacheMixin, TemplateView):

    def get_survey(self) -> Survey:
        try:
            return Survey.objects.prefetch_related(
                "sections", "questions__options", "questions__section",
            ).get(slug=self.kwargs["slug"])
        except Survey.DoesNotExist:
            raise Http404

    @staticmethod
    def answers_by_question(survey) -> dict:
        by_question: dict = {}
        answers = SurveyAnswer.objects.filter(
            submission__survey=survey,
        ).select_related("submission__account")
        for answer in answers:
            by_question.setdefault(answer.question_id, []).append(answer)
        return by_question

    @staticmethod
    def numbered_questions(survey) -> list:
        questions = list(survey.questions.all())
        for number, question in enumerate(questions, start=1):
            question.number = number
        return questions


def _pct(count: int, total: int) -> int:
    return round(count * 100 / total) if total else 0


def _bar_rows(counted: dict, options, total: int, extra=None) -> list:
    """label/count/pct/width rows for .ac-bars, widths scaled to the max."""
    rows = [
        {"label": option.text, "count": counted.get(option.option_id, 0)}
        for option in options
    ]
    if extra is not None:
        rows.append({"label": "Other", "count": extra})
    top = max((r["count"] for r in rows), default=0)
    for row in rows:
        row["pct"] = _pct(row["count"], total)
        row["width"] = round(row["count"] * 100 / top) if top else 0
    return rows


class SurveyResultsView(SurveyResultsBase):
    """Aggregated answers, one panel per section."""

    template_name = "survey_results.html"

    def aggregate(self, question, answers: list, respondents: int) -> dict:
        result = {"question": question, "answered": 0}
        counted: dict = {}
        others = []

        if question.kind == QuestionKind.TEXT:
            result["texts"] = [
                {"account": a.submission.account, "text": a.text,
                 "when": a.submission.submitted_at}
                for a in answers
            ]
            result["answered"] = len(answers)

        elif question.kind in (QuestionKind.SINGLE, QuestionKind.MULTI):
            for answer in answers:
                if answer.option_id:
                    counted[answer.option_id] = counted.get(answer.option_id, 0) + 1
                elif answer.text:
                    others.append(answer.text)
            result["answered"] = len({a.submission_id for a in answers})
            result["bars"] = _bar_rows(
                counted, question.choices, respondents,
                extra=len(others) if question.allow_other else None,
            )
            result["others"] = others

        elif question.kind == QuestionKind.MATRIX:
            scale = question.choices
            index = {o.option_id: i for i, o in enumerate(scale)}
            grid: dict = {}
            for answer in answers:
                if answer.row_id and answer.option_id in index:
                    grid.setdefault(answer.row_id, []).append(index[answer.option_id])
            result["scale"] = scale
            result["matrix"] = []
            for row in question.matrix_rows:
                picks = grid.get(row.option_id, [])
                cells = [picks.count(i) for i in range(len(scale))]
                top = max(cells, default=0)
                result["matrix"].append({
                    "row": row,
                    "cells": [
                        {"count": c, "top": top and c == top} for c in cells
                    ],
                    "avg": round(sum(picks) / len(picks) + 1, 1) if picks else None,
                })
            result["answered"] = len({a.submission_id for a in answers})

        elif question.kind == QuestionKind.RANK:
            slots = question.max_choices or len(question.choices)
            scored: dict = {}
            other_score = 0
            other_firsts = 0
            for answer in answers:
                points = slots - (answer.rank or slots) + 1
                if answer.option_id:
                    entry = scored.setdefault(
                        answer.option_id, {"score": 0, "firsts": 0},
                    )
                    entry["score"] += points
                    entry["firsts"] += 1 if answer.rank == 1 else 0
                elif answer.text:
                    other_score += points
                    other_firsts += 1 if answer.rank == 1 else 0
                    others.append(f"(#{answer.rank}) {answer.text}")
            rows = [
                {"label": o.text,
                 "count": scored.get(o.option_id, {}).get("score", 0),
                 "firsts": scored.get(o.option_id, {}).get("firsts", 0)}
                for o in question.choices
            ]
            if question.allow_other:
                rows.append({
                    "label": "Other", "count": other_score,
                    "firsts": other_firsts,
                })
            rows.sort(key=lambda r: -r["count"])
            top = max((r["count"] for r in rows), default=0)
            for row in rows:
                row["width"] = round(row["count"] * 100 / top) if top else 0
            result["ranked"] = rows
            result["others"] = others
            result["answered"] = len({a.submission_id for a in answers})

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.get_survey()
        submissions = list(
            survey.submissions.select_related("account").all()
        )
        respondents = len(submissions)
        by_question = self.answers_by_question(survey)
        questions = self.numbered_questions(survey)

        for question in questions:
            question.result = self.aggregate(
                question, by_question.get(question.question_id, []), respondents,
            )
        groups = [
            {"section": None, "questions": [q for q in questions if not q.section]}
        ]
        for section in survey.sections.all():
            groups.append({
                "section": section,
                "questions": [q for q in questions if q.section_id == section.pk],
            })
        context.update({
            "survey": survey,
            "respondents": respondents,
            "submissions": submissions,
            "groups": [g for g in groups if g["questions"]],
        })
        return context


class SurveySubmissionView(SurveyResultsBase):
    """One account's full response, in survey order."""

    template_name = "survey_submission.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.get_survey()
        try:
            submission = survey.submissions.select_related("account").get(
                pk=self.kwargs["pk"],
            )
        except SurveySubmission.DoesNotExist:
            raise Http404
        answers: dict = {}
        for answer in submission.answers.select_related("option", "row"):
            answers.setdefault(answer.question_id, []).append(answer)
        questions = self.numbered_questions(survey)
        for question in questions:
            question.answer_list = answers.get(question.question_id, [])
        context.update({
            "survey": survey,
            "submission": submission,
            "questions": questions,
        })
        return context


class SurveyResultsCSVView(SurveyResultsBase):
    """Flat CSV export: one row per submission, one column per datum."""

    def render_to_response(self, context, **response_kwargs):
        survey = context["survey"]
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = (
            f'attachment; filename="{survey.slug}-responses.csv"'
        )
        writer = csv.writer(response)
        writer.writerow(context["header"])
        writer.writerows(context["rows"])
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        survey = self.get_survey()
        questions = self.numbered_questions(survey)

        header = ["account", "submitted_at"]
        columns = []  # (question, matrix_row | rank_slot | None)
        for question in questions:
            if question.kind == QuestionKind.MATRIX:
                for row in question.matrix_rows:
                    header.append(f"Q{question.number} [{row.text}]")
                    columns.append((question, row.option_id, None))
            elif question.kind == QuestionKind.RANK:
                for slot in question.rank_slots:
                    header.append(f"Q{question.number} #{slot}")
                    columns.append((question, None, slot))
            else:
                header.append(f"Q{question.number}")
                columns.append((question, None, None))

        by_submission: dict = {}
        for answer in SurveyAnswer.objects.filter(
            submission__survey=survey,
        ).select_related("option"):
            by_submission.setdefault(answer.submission_id, []).append(answer)

        rows = []
        for submission in survey.submissions.select_related("account"):
            answers = by_submission.get(submission.submission_id, [])
            row = [str(submission.account), submission.submitted_at.isoformat()]
            for question, row_id, slot in columns:
                cell = [
                    a for a in answers
                    if a.question_id == question.question_id
                    and (row_id is None or a.row_id == row_id)
                    and (slot is None or a.rank == slot)
                ]
                row.append("; ".join(a.display_value for a in cell))
            rows.append(row)

        context.update({"survey": survey, "header": header, "rows": rows})
        return context

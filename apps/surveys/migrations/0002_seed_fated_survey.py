"""
Seed the "Next Evolution of Fated" design survey, in Draft — flip it Open in
the admin (or the surveys admin page) to start collecting responses.
"""
from django.db import migrations


INTRO = (
    "I'm designing the next evolution of Fated — a prestige loop layered on "
    "the class you already know. Nothing here is final; your answers will "
    "directly shape it. ~5 minutes, no wrong answers, and \"this idea is bad\" "
    "is useful data."
)

LOOP_PREAMBLE = (
    "Imagine Fated gains a prestige loop: at a milestone remort count you can "
    "choose to end the life, permanently raising your account's \"difficulty "
    "tier\" for the season — each tier adds a new challenge rule and pays "
    "better rewards. Death still restarts the current climb as today."
)

CHALLENGE_RULES = (
    "Lower max HP/mana, slower regen",
    "Reduced healing",
    "Tougher/smarter enemies",
    "Losing convenience escapes (e.g. recall)",
    "Skill level caps",
    "Rules that limit your bound skills",
    "Slower XP at high tiers",
)

# (section title, preamble, questions); question:
# (kind, text, hint, required, max_choices, allow_other, choices, matrix_rows)
SECTIONS = (
    ("A. Baseline", "", (
        ("single", "In a typical week, how many hours do you play Ishar?",
         "", True, None, False,
         ("0–5", "5–10", "10–20", "20+"), ()),
        ("single",
         "In a typical Fated life, how far do you usually get before death "
         "or abandoning?",
         "", True, None, False,
         ("Remort 0–1", "Remort 2–3", "Remort 4–5", "Remort 6–9",
          "Remort 10+"), ()),
        ("single",
         "Roughly how long does remort 0 → 5 take you, played seriously?",
         "", True, None, False,
         ("A day or two", "Under a week", "1–2 weeks", "Longer"), ()),
    )),
    ("B. What's fun about Fated", "", (
        ("matrix", "Rate each phase of a Fated life:",
         "", True, None, False,
         ("Not fun", "Fine", "Fun", "The best part"),
         ("Remorts 0–2", "Remorts 3–5", "Remorts 6–10", "Remorts 10+")),
        ("multi",
         "If early remorts are less fun for you, what makes them so?",
         "Pick up to 3 — or skip if they're fine.", False, 3, True,
         ("Losing scaled stats and renown",
          "Weak skill kit until draws land",
          "Slow leveling",
          "Re-gearing from nothing",
          "They're fine, just repetitive"), ()),
        ("rank", "What makes Fated enjoyable for you?",
         "Rank your top 2.", True, 2, True,
         ("The random skill draft each level",
          "Choosing what to bind",
          "Watching one character's power compound",
          "The permadeath stakes",
          "Competing for essence/leaderboard"), ()),
    )),
    ("C. The loop", LOOP_PREAMBLE, (
        ("single", "What's the right length for one climb?",
         "", True, None, False,
         ("Short (cap ~5 remorts, repeated more often)",
          "Medium (cap ~8–10, repeated less)",
          "Long (cap 15+, only a few climbs per season)",
          "No cap — let me decide when to prestige"), ()),
        ("single",
         "Over a whole season, how many completed climbs would feel right "
         "for a dedicated player?",
         "", True, None, False,
         ("2–3", "4–6", "7–10", "10+", "As many as I can fit"), ()),
        ("single", "How much harder should each tier get?",
         "", True, None, False,
         ("Gently — I want the loop, not the pain",
          "Noticeably — each tier should change how I play",
          "Brutally by the end — the last tiers should feel nearly "
          "impossible"), ()),
        ("multi",
         "Which kinds of challenge rules sound interesting (not just "
         "annoying)?",
         "Pick all that apply.", True, None, False,
         CHALLENGE_RULES + ("None of these — keep rules out of it",), ()),
        ("multi", "Same list — which would make you stop climbing?",
         "Pick all that apply, or skip if none of them would stop you.",
         False, None, False,
         CHALLENGE_RULES, ()),
    )),
    ("D. Stakes & rewards", "", (
        ("single", "The summit — max tier, fully climbed — should be:",
         "", True, None, False,
         ("Reachable by any regular who commits the season",
          "Reachable by the few most dedicated (a handful per season)",
          "So hard it might go unclaimed for a season or more"), ()),
        ("rank", "What would make repeated climbs worth it to you?",
         "Rank your top 2.", True, 2, False,
         ("More essence",
          "An exclusive title",
          "A permanent cosmetic",
          "Leaderboard standing",
          "The achievement/bragging rights itself",
          "Nothing would — I don't want a prestige loop"), ()),
        ("single",
         "Deliberately ending a strong, living character as the price of "
         "progression feels:",
         "", True, None, False,
         ("Exciting — that's what makes it real",
          "Acceptable if the payout is right",
          "Bad — I'd rather progression never require ending a life"), ()),
    )),
    ("E. Binding", "", (
        ("single",
         "Do you build up your bound-skill pool before committing to a "
         "serious run?",
         "", True, None, False,
         ("Always", "Sometimes", "No", "What pool? (newer player)"), ()),
        ("single",
         "If prestiging reset your bound-skill pool in exchange for the "
         "permanent tier rewards, you would:",
         "", True, None, False,
         ("Prestige anyway — the loop is the point",
          "Prestige only when my pool is weak",
          "Never prestige — the pool is my progress",
          "Depends entirely on how good the rewards are"), ()),
    )),
    ("F. Open", "", (
        ("text",
         "What one change would make repeating remorts 0–5 more fun?",
         "", False, None, False, (), ()),
        ("text",
         "Anything else about this idea — including \"don't do it\"?",
         "", False, None, False, (), ()),
    )),
)


def seed(apps, schema_editor):
    Survey = apps.get_model("surveys", "Survey")
    SurveySection = apps.get_model("surveys", "SurveySection")
    SurveyQuestion = apps.get_model("surveys", "SurveyQuestion")
    SurveyOption = apps.get_model("surveys", "SurveyOption")

    survey = Survey.objects.create(
        slug="fated-next",
        title="The Next Evolution of Fated",
        intro=INTRO,
        status="draft",
    )
    for s_pos, (title, preamble, questions) in enumerate(SECTIONS, start=1):
        section = SurveySection.objects.create(
            survey=survey, position=s_pos, title=title, preamble=preamble,
        )
        for q_pos, question in enumerate(questions, start=1):
            (kind, text, hint, required, max_choices, allow_other,
             choices, matrix_rows) = question
            record = SurveyQuestion.objects.create(
                survey=survey, section=section, position=q_pos, kind=kind,
                text=text, hint=hint, required=required,
                max_choices=max_choices, allow_other=allow_other,
            )
            SurveyOption.objects.bulk_create(
                [
                    SurveyOption(
                        question=record, position=o_pos, text=choice,
                    )
                    for o_pos, choice in enumerate(choices, start=1)
                ] + [
                    SurveyOption(
                        question=record, position=o_pos, text=row,
                        is_matrix_row=True,
                    )
                    for o_pos, row in enumerate(matrix_rows, start=1)
                ]
            )


def unseed(apps, schema_editor):
    apps.get_model("surveys", "Survey").objects.filter(
        slug="fated-next",
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]

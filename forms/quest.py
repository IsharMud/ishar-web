"""Flask forms classes for quests"""
from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, \
    SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class QuestForm(FlaskForm):
    """Quest form class"""
    name = StringField(
        'Name',
        validators=[
            DataRequired(),
            Length(min=1, max=25)
        ]
    )
    display_name = StringField(
        'Display Name',
        validators=[
            DataRequired(),
            Length(min=1, max=30)
        ]
    )
    completion_message = TextAreaField(
        'Completion Message',
        validators=[
            Length(max=80)
        ]
    )
    min_level = IntegerField(
        'Minimum Level',
        default=1,
        validators=[
            DataRequired(),
            NumberRange(min=1, max=20)
        ]
    )
    max_level = IntegerField(
        'Maximum Level',
        default=20,
        validators=[
            DataRequired(),
            NumberRange(min=1, max=20)
        ]
    )
    repeatable = BooleanField('Repeatable')
    description = TextAreaField(
         'Description',
         validators=[
             DataRequired(),
             Length(min=1, max=512)
         ]
    )
    class_restrict = SelectField(
        'Class Restriction',
        choices=[
            (-1, 'None')
        ],
        coerce=int,
        default=-1,
        validators=[
            DataRequired(),
        ]
    )
    quest_intro = TextAreaField(
        'Quest Introduction',
        validators=[
            DataRequired(),
            Length(min=1, max=1600)
        ]
    )
    prerequisite = SelectField(
        'Quest Prerequisite',
        choices=[
            (-1, 'None')
        ],
        coerce=int,
        default=-1,
        validators=[
            DataRequired(),
        ]
    )
    submit = SubmitField('Save Quest')


class QuestStepForm(FlaskForm):
    """Quest Step form class"""
    step_type = SelectField(
        'Step Type',
        choices=[
            (0, 'Object'),
            (1, 'Kill'),
            (2, 'Room')
        ],
        coerce=int,
        validators=[
            DataRequired()
        ]
    )
    target = IntegerField(
        'Target',
        validators=[
            DataRequired()
        ]
    )
    num_required = IntegerField(
        'Number Required',
        validators=[
            DataRequired()
        ]
    )
    time_limit = IntegerField('Time Limit')
    mystify = BooleanField('Mystify')
    mystify_text = StringField(
        'Mystify Text',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Save Step')


class QuestRewardForm(FlaskForm):
    """Quest Reward form class"""
    reward_num = IntegerField(
        'Reward Number',
        validators=[
            DataRequired()
        ]
    )
    reward_type = SelectField(
        'Reward Type',
        choices=[
            (0, 'Object_always'),
            (1, 'Object_Choice'),
            (2, 'Money'),
            (3, 'Alignment'),
            (4, 'Skill'),
            (5, 'Renown'),
            (6, 'Experience'),
            (7, 'Quest')
        ],
        coerce=int,
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Save Reward')

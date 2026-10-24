from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import AgeGroup, Response, Sex
from .models import Answer
from .questions import QUESTIONS, Question

EMPTY_CHOICE = ("", _("Choose…"))


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("sex", "age_group")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sex"].choices = [EMPTY_CHOICE, *Sex.choices]
        self.fields["age_group"].choices = [EMPTY_CHOICE, *AgeGroup.choices]


class QuestionForm(forms.Form):
    answer = forms.TypedChoiceField(
        label=_("Answer"),
        choices=Response.choices,
        coerce=int,
        empty_value=None,
        widget=forms.RadioSelect,
        # Unanswered questions are scored as neutral.
        required=False,
    )

    def __init__(self, *args, question: Question | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.question = question


class BaseQuestionFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index: int | None) -> dict:
        kwargs = super().get_form_kwargs(index)
        # The index is None for the empty form template.
        if index is not None:
            kwargs["question"] = QUESTIONS[index]
        return kwargs

    def clean(self):
        # Unanswered questions are allowed, but every question must be present.
        # (The built-in ``validate_min`` would reject unanswered forms as empty.)
        if self.total_form_count() != len(QUESTIONS):
            raise ValidationError(
                _("Please submit the whole questionnaire."), code="incomplete"
            )

    @property
    def responses(self) -> list[int | None]:
        """The responses in the order of the questions, valid formsets only."""
        return [form.cleaned_data["answer"] for form in self.forms]


QuestionFormSet = forms.formset_factory(
    QuestionForm,
    formset=BaseQuestionFormSet,
    extra=0,
    min_num=len(QUESTIONS),
    max_num=len(QUESTIONS),
    absolute_max=len(QUESTIONS),
)

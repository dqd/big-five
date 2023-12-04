from typing import Any
from django import forms
from django.utils.translation import gettext_lazy as _

from .constants import Response, Ordering, QUESTIONS
from .models import Answer


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("sex", "age_group")


class QuestionForm(forms.Form):
    statement = forms.CharField(label=_("Statement"), disabled=True)
    answer = forms.ChoiceField(
        label=_("Answer"),
        choices=Response.choices,
        widget=forms.RadioSelect,
        required=False,
    )
    ordering = forms.ChoiceField(
        choices=Ordering.choices,
        widget=forms.HiddenInput,
        required=False,
    )


class BaseQuestionFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        for i, form in enumerate(self.forms):
            form.cleaned_data["ordering"] = QUESTIONS[i]


QuestionFormSet = forms.formset_factory(
    QuestionForm,
    formset=BaseQuestionFormSet,
    extra=0,
)

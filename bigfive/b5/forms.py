from django import forms
from django.utils.translation import gettext_lazy as _

from .constants import Response, Ordering
from .models import Answer


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("sex", "age_group")


class QuestionForm(forms.Form):
    statement = forms.CharField(label=_("Statement"), disabled=True)  # Tvrzení
    answer = forms.ChoiceField(
        label=_("Answer"),  # Odpověď
        choices=Response.choices,
        widget=forms.RadioSelect,
        required=False,
    )
    ordering = forms.ChoiceField(
        choices=Ordering.choices,
        widget=forms.HiddenInput,
        required=False,
    )


QuestionFormSet = forms.formset_factory(QuestionForm, extra=0)

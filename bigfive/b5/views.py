from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, View

from .constants import HIGH_SCORE, LOW_SCORE
from .evaluator import evaluate
from .forms import PersonalInfoForm, QuestionFormSet
from .models import Answer


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        return self.render(request, PersonalInfoForm(), QuestionFormSet())

    def post(self, request):
        personal_info_form = PersonalInfoForm(request.POST)
        questions_formset = QuestionFormSet(request.POST)
        # Validate both so that the errors of both are shown at once.
        personal_info_valid = personal_info_form.is_valid()
        questions_valid = questions_formset.is_valid()

        if personal_info_valid and questions_valid:
            answer = personal_info_form.save(commit=False)
            answer.results = evaluate(
                answer.sex, answer.age_group, questions_formset.responses
            )
            answer.save()
            return redirect(answer)

        return self.render(request, personal_info_form, questions_formset)

    def render(self, request, personal_info_form, questions_formset):
        return render(
            request,
            self.template_name,
            {
                "personal_info_form": personal_info_form,
                "questions_formset": questions_formset,
                "questionnaire_labels": {
                    "start": _("Start the test"),
                    "back": _("Back"),
                    "next": _("Next"),
                },
            },
        )


class ResultView(DetailView):
    model = Answer
    context_object_name = "answer"
    template_name = "result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report"] = self.object.report
        context["chart_config"] = {
            "low": LOW_SCORE,
            "high": HIGH_SCORE,
            "labels": {
                "low": _("Low score threshold"),
                "high": _("High score threshold"),
                "percentile": _("Percentile"),
            },
        }
        return context

from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .constants import QUESTIONS, HIGH_SCORE, LOW_SCORE
from .evaluator import evaluate
from .forms import PersonalInfoForm, QuestionFormSet
from .models import Answer


class IndexView(View):
    def get(self, request, personal_info_form=None):
        return render(
            request,
            "index.html",
            {
                "personal_info_form": personal_info_form or PersonalInfoForm(),
                "questions_formset": QuestionFormSet(initial=QUESTIONS),
            },
        )

    def post(self, request):
        personal_info_form = PersonalInfoForm(data=request.POST)
        questions_formset = QuestionFormSet(data=request.POST, initial=QUESTIONS)

        if personal_info_form.is_valid() and questions_formset.is_valid():
            results = evaluate(
                personal_info_form.cleaned_data["sex"],
                personal_info_form.cleaned_data["age_group"],
                questions_formset.cleaned_data,
            )
            answer = personal_info_form.save(commit=False)
            answer.results = results
            answer.save()

            return redirect(reverse("result", args=(answer.slug,)))

        return self.get(request, personal_info_form)


class ResultView(View):
    def get(self, request, slug):
        answer = get_object_or_404(Answer, slug=slug)
        return render(
            request,
            "result.html",
            {"answer": answer, "high": HIGH_SCORE, "low": LOW_SCORE},
        )

from django.test import TestCase
from django.urls import reverse

from .constants import AgeGroup, Sex, QUESTIONS, SLUG_LENGTH
from .evaluator import evaluate
from .models import Answer

SAMPLE_ANSWERS = (
    "5,4,4,5,2,1,1,4,1,2,"
    "2,4,2,4,5,2,4,5,1,4,"
    "5,4,5,4,4,4,3,5,2,2,"
    "5,4,4,4,4,1,1,4,1,1,"
    "2,4,2,2,5,2,4,2,1,4,"
    "2,4,2,2,4,4,2,2,2,2,"
    "2,2,3,4,4,1,4,2,2,1,"
    "2,4,5,3,2,3,4,2,2,2,"
    "2,1,1,4,4,3,5,2,4,3,"
    "5,3,5,2,3,5,5,2,1,1,"
    "5,2,4,3,1,1,4,2,1,2,"
    "2,2,2,2,5,2,4,1,4,2"
)
EXPECTED_RESULTS = {
    "extraversion": 36,
    "friendliness": 47,
    "gregariousness": 4,
    "assertiveness": 63,
    "activity_level": 70,
    "excitement_seeking": 26,
    "cheerfulness": 46,
    "agreeableness": 57,
    "trust": 86,
    "morality": 81,
    "altruism": 13,
    "cooperation": 87,
    "modesty": 55,
    "sympathy": 2,
    "conscientiousness": 63,
    "self_efficacy": 13,
    "orderliness": 87,
    "dutifulness": 88,
    "achievement_striving": 56,
    "self_discipline": 26,
    "cautiousness": 64,
    "neuroticism": 60,
    "anxiety": 93,
    "anger": 1,
    "depression": 22,
    "self_consciousness": 48,
    "immoderation": 91,
    "vulnerability": 97,
    "openness": 59,
    "imagination": 50,
    "artistic_interests": 60,
    "emotionality": 1,
    "adventurousness": 86,
    "intellect": 70,
    "liberalism": 87,
}


class EvaluatorTestCase(TestCase):
    def test_evaluate(self):
        questions = QUESTIONS.copy()

        for question, answer in zip(questions, SAMPLE_ANSWERS.split(",")):
            question["answer"] = answer

        result = evaluate(Sex.MALE, AgeGroup.ADULTS, questions)
        self.assertDictEqual(EXPECTED_RESULTS, result)


class PageTestCase(TestCase):
    def test_display_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_send_questionnaire(self):
        Answer.objects.all().delete()

        forms_len = len(QUESTIONS)
        response = self.client.post(
            reverse("index"),
            {
                "sex": Sex.MALE,
                "age_group": AgeGroup.ADULTS,
                "form-TOTAL_FORMS": forms_len,
                "form-INITIAL_FORMS": forms_len,
            },
        )

        answer = Answer.objects.last()
        self.assertIsNotNone(answer)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("result", kwargs={"slug": answer.slug}))

    def test_display_result(self):
        answer = Answer.objects.create(
            sex=Sex.MALE, age_group=AgeGroup.ADULTS, results=EXPECTED_RESULTS
        )
        response = self.client.get(reverse("result", kwargs={"slug": answer.slug}))
        self.assertEqual(response.status_code, 200)

    def test_result_not_found(self):
        response = self.client.get(
            reverse("result", kwargs={"slug": "x" * SLUG_LENGTH})
        )
        self.assertEqual(response.status_code, 404)

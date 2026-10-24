import re
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import translation

from .constants import (
    HIGH_SCORE,
    LOW_SCORE,
    SLUG_LENGTH,
    AgeGroup,
    Level,
    Response,
    Sex,
)
from .evaluator import MAX_T_SCORE, MIN_T_SCORE, evaluate, percentile, score
from .models import Answer
from .norms import NORMS
from .questions import QUESTIONS
from .traits import DOMAINS, build_report

SAMPLE_ANSWERS_CSV = (
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
SAMPLE_ANSWERS = [int(answer) for answer in SAMPLE_ANSWERS_CSV.split(",")]
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
ALL_TRAIT_KEYS = {
    key
    for domain in DOMAINS
    for key in (domain.key, *(facet.key for facet in domain.facets))
}


def questionnaire_data(answers=(), **personal_info):
    """Build the POST data of the questionnaire."""
    data = {
        "form-TOTAL_FORMS": len(QUESTIONS),
        "form-INITIAL_FORMS": 0,
        **personal_info,
    }
    for index, answer in enumerate(answers):
        data[f"form-{index}-answer"] = answer
    return data


class EvaluatorTests(SimpleTestCase):
    def test_sample_questionnaire(self):
        results = evaluate(Sex.MALE, AgeGroup.ADULTS, SAMPLE_ANSWERS)
        self.assertDictEqual(EXPECTED_RESULTS, results)

    def test_accepts_plain_strings_as_group(self):
        results = evaluate("M", "A", SAMPLE_ANSWERS)
        self.assertDictEqual(EXPECTED_RESULTS, results)

    def test_results_cover_all_traits(self):
        results = evaluate(Sex.FEMALE, AgeGroup.ELDERLY, SAMPLE_ANSWERS)
        self.assertSetEqual(ALL_TRAIT_KEYS, set(results))
        self.assertTrue(all(1 <= value <= 99 for value in results.values()))

    def test_unanswered_questions_count_as_neutral(self):
        unanswered = evaluate(Sex.FEMALE, AgeGroup.YOUNG, [None] * len(QUESTIONS))
        neutral = evaluate(
            Sex.FEMALE, AgeGroup.YOUNG, [Response.NEUTRAL] * len(QUESTIONS)
        )
        self.assertDictEqual(unanswered, neutral)

    def test_answers_change_the_results(self):
        neutral = evaluate(
            Sex.MALE, AgeGroup.ADULTS, [Response.NEUTRAL] * len(QUESTIONS)
        )
        self.assertNotEqual(neutral, EXPECTED_RESULTS)

    def test_reversed_items_are_scored_backwards(self):
        straight = next(question for question in QUESTIONS if not question.reversed)
        reversed_ = next(question for question in QUESTIONS if question.reversed)
        self.assertEqual(score(straight, Response.VERY_ACCURATE), 5)
        self.assertEqual(score(reversed_, Response.VERY_ACCURATE), 1)
        self.assertEqual(score(reversed_, Response.NEUTRAL), 3)
        self.assertEqual(score(reversed_, None), 3)

    def test_wrong_number_of_responses(self):
        with self.assertRaises(ValueError):
            evaluate(Sex.MALE, AgeGroup.ADULTS, SAMPLE_ANSWERS[:-1])

    def test_percentile(self):
        self.assertEqual(percentile(MIN_T_SCORE - 1), 1)
        self.assertEqual(percentile(50), 49)
        self.assertEqual(percentile(60), 82)
        self.assertEqual(percentile(MAX_T_SCORE + 1), 99)
        percentiles = [
            percentile(t_score) for t_score in range(MIN_T_SCORE, MAX_T_SCORE + 1)
        ]
        self.assertTrue(all(1 <= value <= 99 for value in percentiles))

    def test_norms_cover_all_groups(self):
        for sex in Sex:
            for age_group in AgeGroup:
                with self.subTest(sex=sex, age_group=age_group):
                    norms = NORMS[sex, age_group]
                    self.assertSetEqual(set(norms), {domain.code for domain in DOMAINS})
                    for domain_norms in norms.values():
                        self.assertEqual(len(domain_norms.facets), 6)


class LevelTests(SimpleTestCase):
    def test_boundaries(self):
        self.assertEqual(Level.of(LOW_SCORE - 1), Level.LOW)
        self.assertEqual(Level.of(LOW_SCORE), Level.AVERAGE)
        self.assertEqual(Level.of(HIGH_SCORE), Level.AVERAGE)
        self.assertEqual(Level.of(HIGH_SCORE + 1), Level.HIGH)


class ReportTests(SimpleTestCase):
    def test_build_report(self):
        report = build_report(EXPECTED_RESULTS)
        self.assertEqual(
            [result.domain.key for result in report], [d.key for d in DOMAINS]
        )

        extraversion = report[0]
        self.assertEqual(extraversion.score, 36)
        self.assertEqual(extraversion.level, Level.LOW)
        self.assertEqual(
            extraversion.interpretation, DOMAINS[0].interpretations[Level.LOW]
        )
        self.assertEqual(
            [facet.score for facet in extraversion.facets], [47, 4, 63, 70, 26, 46]
        )
        self.assertEqual(extraversion.facets[1].level, Level.LOW)


class IndexPageTests(TestCase):
    def test_display_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["questions_formset"]), len(QUESTIONS))
        self.assertContains(response, 'class="question"', count=len(QUESTIONS))
        self.assertContains(response, QUESTIONS[0].statement)

    def test_display_index_in_english(self):
        with translation.override("cs"):
            czech = self.client.get(reverse("index"))
        with translation.override("en"):
            english = self.client.get(reverse("index"))

        self.assertContains(czech, '<html lang="cs">')
        self.assertContains(czech, 'href="/en/"')
        self.assertContains(english, '<html lang="en">')
        self.assertContains(english, 'href="/"')
        self.assertEqual(english.request["PATH_INFO"], "/en/")

    def test_submit_questionnaire(self):
        response = self.client.post(
            reverse("index"),
            questionnaire_data(SAMPLE_ANSWERS, sex=Sex.MALE, age_group=AgeGroup.ADULTS),
        )

        answer = Answer.objects.get()
        self.assertRedirects(response, reverse("result", kwargs={"slug": answer.slug}))
        self.assertEqual(len(answer.slug), SLUG_LENGTH)
        self.assertDictEqual(answer.results, EXPECTED_RESULTS)

    def test_submit_without_answers(self):
        response = self.client.post(
            reverse("index"),
            questionnaire_data(sex=Sex.FEMALE, age_group=AgeGroup.YOUNG),
        )

        answer = Answer.objects.get()
        self.assertEqual(response.status_code, 302)
        self.assertDictEqual(
            answer.results,
            evaluate(Sex.FEMALE, AgeGroup.YOUNG, [None] * len(QUESTIONS)),
        )

    def test_missing_personal_info_keeps_the_answers(self):
        response = self.client.post(
            reverse("index"),
            questionnaire_data(SAMPLE_ANSWERS, sex=Sex.MALE, age_group=""),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Answer.objects.exists())
        self.assertIn("age_group", response.context["personal_info_form"].errors)
        formset = response.context["questions_formset"]
        self.assertEqual(formset.forms[0]["answer"].value(), str(SAMPLE_ANSWERS[0]))

    def test_invalid_answer(self):
        response = self.client.post(
            reverse("index"),
            questionnaire_data([6], sex=Sex.MALE, age_group=AgeGroup.ADULTS),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Answer.objects.exists())
        self.assertIn("answer", response.context["questions_formset"].forms[0].errors)

    def test_too_few_forms(self):
        data = questionnaire_data(sex=Sex.MALE, age_group=AgeGroup.ADULTS)
        data["form-TOTAL_FORMS"] = 1
        response = self.client.post(reverse("index"), data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Answer.objects.exists())
        self.assertTrue(response.context["questions_formset"].non_form_errors())


class ResultPageTests(TestCase):
    def setUp(self):
        self.answer = Answer.objects.create(
            sex=Sex.MALE, age_group=AgeGroup.ADULTS, results=EXPECTED_RESULTS
        )

    def test_display_result(self):
        response = self.client.get(self.answer.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["answer"], self.answer)
        self.assertEqual(len(response.context["report"]), len(DOMAINS))
        self.assertContains(response, 'id="chart-config"')
        self.assertContains(response, 'data-values="36,57,63,60,59"')

    def test_display_result_in_english(self):
        response = self.client.get(f"/en/{self.answer.slug}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="/{self.answer.slug}/"')
        self.assertContains(response, "Your score on <em>Extraversion</em> is low.")

    def test_result_not_found(self):
        response = self.client.get(
            reverse("result", kwargs={"slug": "x" * SLUG_LENGTH})
        )
        self.assertEqual(response.status_code, 404)

    def test_malformed_slug(self):
        response = self.client.get("/abc/")
        self.assertEqual(response.status_code, 404)


class TranslationTests(SimpleTestCase):
    PO_FILE = Path(settings.BASE_DIR) / "locale" / "cs" / "LC_MESSAGES" / "django.po"

    def test_czech_translation_is_complete(self):
        entries = self.PO_FILE.read_text(encoding="utf-8").split("\n\n")[1:]
        self.assertGreater(len(entries), 100)

        for entry in entries:
            with self.subTest(entry=entry[:80]):
                self.assertNotIn("#, fuzzy", entry)
                self.assertIsNone(
                    re.search(r'msgstr ""\s*$', entry), "untranslated entry"
                )

    def test_czech_translation_is_compiled(self):
        with translation.override("cs"):
            self.assertEqual(translation.gettext("Female"), "Žena")
            self.assertEqual(translation.gettext("Choose…"), "Vyberte…")


class MigrationTests(TestCase):
    def test_migrations_are_up_to_date(self):
        call_command("makemigrations", "--check", "--dry-run", verbosity=0)

"""
Scoring of the IPIP-NEO-120 questionnaire.

A port of https://github.com/kholia/IPIP-NEO-PI/blob/21.06/app/evaluator.py, which
follows the original implementation by John A. Johnson.
"""

from collections.abc import Sequence

from .constants import AgeGroup, Response, Sex
from .norms import NORMS
from .questions import QUESTIONS, Question
from .traits import DOMAINS

# The 120 items form 30 facet scales of 4 items each. Consecutive items belong to
# consecutive facet scales, and the facet scales cycle through the domains in
# the order N, E, O, A, C: items 1, 6, 11, … belong to Neuroticism, 2, 7, 12, …
# to Extraversion, and so on.
DOMAIN_CODES = "NEOAC"
ITEMS_PER_FACET = 4
FACETS_PER_DOMAIN = 6
FACET_SCALES = len(QUESTIONS) // ITEMS_PER_FACET

# T-scores outside this range are mapped to the 1st and the 99th percentile.
MIN_T_SCORE = 32
MAX_T_SCORE = 73
# Coefficients of the cubic polynomial approximating the percentile of a T-score.
CUBIC_COEFFICIENTS = (
    210.335958661391,
    -16.7379362643389,
    0.405936512733332,
    -0.00270624341822222,
)


def percentile(t_score: float) -> int:
    """Approximate the percentile rank of a T-score, clamped to 1–99."""
    if t_score < MIN_T_SCORE:
        return 1
    if t_score > MAX_T_SCORE:
        return 99

    a, b, c, d = CUBIC_COEFFICIENTS
    return int(a + b * t_score + c * t_score**2 + d * t_score**3)


def score(question: Question, response: int | None) -> int:
    """Return the item score of a response; unanswered items count as neutral."""
    if response is None:
        return Response.NEUTRAL
    if question.reversed:
        return Response.VERY_ACCURATE + Response.VERY_INACCURATE - response
    return response


def evaluate(
    sex: Sex, age_group: AgeGroup, responses: Sequence[int | None]
) -> dict[str, int]:
    """
    Evaluate the responses to all questions, given in the order of ``QUESTIONS``.

    Return the percentile estimates of the five domains and their 30 facets,
    keyed by their result keys (see ``traits``).
    """
    if len(responses) != len(QUESTIONS):
        raise ValueError(f"Expected {len(QUESTIONS)} responses, got {len(responses)}.")

    scores = [
        score(question, response)
        for question, response in zip(QUESTIONS, responses, strict=True)
    ]
    norms = NORMS[sex, age_group]
    results = {}

    for domain in DOMAINS:
        offset = DOMAIN_CODES.index(domain.code)
        facet_scores = [
            sum(
                scores[offset + len(DOMAIN_CODES) * facet + FACET_SCALES * item]
                for item in range(ITEMS_PER_FACET)
            )
            for facet in range(FACETS_PER_DOMAIN)
        ]
        domain_norms = norms[domain.code]
        results[domain.key] = percentile(
            domain_norms.domain.standardize(sum(facet_scores))
        )

        for facet, facet_score, norm in zip(
            domain.facets, facet_scores, domain_norms.facets, strict=True
        ):
            results[facet.key] = percentile(norm.standardize(facet_score))

    return results

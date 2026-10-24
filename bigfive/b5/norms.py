"""
Normative data of the IPIP-NEO-120: means and standard deviations of the raw
domain and facet scores, split by sex and age group.

Source: https://github.com/kholia/IPIP-NEO-PI/blob/21.06/app/norms.py
"""

from dataclasses import dataclass

from .constants import AgeGroup, Sex


@dataclass(frozen=True, slots=True)
class Norm:
    """Mean and standard deviation of a raw score within a reference group."""

    mean: float
    sd: float

    def standardize(self, raw: float) -> float:
        """Convert a raw score to a T-score (mean 50, standard deviation 10)."""
        return 50 + 10 * (raw - self.mean) / self.sd


@dataclass(frozen=True, slots=True)
class DomainNorms:
    domain: Norm
    facets: tuple[Norm, Norm, Norm, Norm, Norm, Norm]


# Keyed by (sex, age group), then by domain code: N, E, O, A, C.
NORMS: dict[tuple[Sex, AgeGroup], dict[str, DomainNorms]] = {
    (Sex.MALE, AgeGroup.YOUNG): {
        "N": DomainNorms(
            Norm(67.84, 15.83),
            (
                Norm(11.72, 3.76),
                Norm(11.93, 4.41),
                Norm(10.58, 4.25),
                Norm(12.38, 3.83),
                Norm(11.67, 3.25),
                Norm(9.63, 3.38),
            ),
        ),
        "E": DomainNorms(
            Norm(80.7, 15.37),
            (
                Norm(13.76, 3.78),
                Norm(12.23, 4.17),
                Norm(14.06, 3.66),
                Norm(11.54, 3.15),
                Norm(14.67, 3.38),
                Norm(14.41, 3.68),
            ),
        ),
        "O": DomainNorms(
            Norm(85.98, 12.37),
            (
                Norm(16.68, 2.96),
                Norm(14.51, 3.87),
                Norm(14.52, 3.31),
                Norm(12.84, 3.16),
                Norm(15.47, 3.5),
                Norm(11.86, 3.17),
            ),
        ),
        "A": DomainNorms(
            Norm(81.98, 14.66),
            (
                Norm(13.18, 3.69),
                Norm(14.85, 3.44),
                Norm(15.37, 3.1),
                Norm(12.73, 4.05),
                Norm(12.01, 3.94),
                Norm(13.96, 3.35),
            ),
        ),
        "C": DomainNorms(
            Norm(79.66, 14.49),
            (
                Norm(15.31, 2.55),
                Norm(10.97, 3.93),
                Norm(15.22, 2.92),
                Norm(13.61, 3.65),
                Norm(12.35, 3.24),
                Norm(12.08, 4.02),
            ),
        ),
    },
    (Sex.MALE, AgeGroup.ADULTS): {
        "N": DomainNorms(
            Norm(66.97, 16.48),
            (
                Norm(11.44, 3.76),
                Norm(11.75, 4.3),
                Norm(10.37, 4.12),
                Norm(12.11, 3.81),
                Norm(12.18, 3.52),
                Norm(9.13, 3.48),
            ),
        ),
        "E": DomainNorms(
            Norm(78.9, 15.21),
            (
                Norm(13.31, 3.8),
                Norm(11.34, 3.99),
                Norm(14.58, 3.58),
                Norm(12.07, 3.23),
                Norm(13.34, 3.43),
                Norm(14.3, 3.53),
            ),
        ),
        "O": DomainNorms(
            Norm(86.51, 12.65),
            (
                Norm(15.94, 3.18),
                Norm(14.94, 3.63),
                Norm(14.6, 3.19),
                Norm(13.14, 3.39),
                Norm(16.11, 3.25),
                Norm(11.66, 3.72),
            ),
        ),
        "A": DomainNorms(
            Norm(84.22, 13.1),
            (
                Norm(12.81, 3.69),
                Norm(15.93, 3.18),
                Norm(15.37, 2.92),
                Norm(14.58, 3.7),
                Norm(11.43, 3.57),
                Norm(13.77, 3.29),
            ),
        ),
        "C": DomainNorms(
            Norm(85.5, 14.27),
            (
                Norm(15.8, 2.44),
                Norm(12.05, 4.26),
                Norm(15.68, 2.76),
                Norm(15.36, 3.39),
                Norm(13.27, 3.31),
                Norm(13.31, 4.03),
            ),
        ),
    },
    (Sex.MALE, AgeGroup.MATURE): {
        "N": DomainNorms(
            Norm(64.11, 16.04),
            (
                Norm(10.79, 3.56),
                Norm(11.6, 4.16),
                Norm(9.78, 3.94),
                Norm(11.85, 3.62),
                Norm(11.24, 3.55),
                Norm(8.81, 3.35),
            ),
        ),
        "E": DomainNorms(
            Norm(77.06, 14.31),
            (
                Norm(13.22, 3.71),
                Norm(10.45, 3.68),
                Norm(14.95, 3.44),
                Norm(12.27, 3.3),
                Norm(11.82, 3.23),
                Norm(14.32, 3.29),
            ),
        ),
        "O": DomainNorms(
            Norm(83.04, 13.05),
            (
                Norm(14.65, 3.35),
                Norm(14.66, 3.59),
                Norm(14.76, 3.02),
                Norm(12.69, 3.44),
                Norm(15.4, 3.43),
                Norm(11.04, 3.93),
            ),
        ),
        "A": DomainNorms(
            Norm(88.33, 11.76),
            (
                Norm(13.42, 3.49),
                Norm(16.94, 2.83),
                Norm(15.65, 2.88),
                Norm(15.66, 3.33),
                Norm(11.96, 3.34),
                Norm(14.21, 3.17),
            ),
        ),
        "C": DomainNorms(
            Norm(91.27, 13.35),
            (
                Norm(16.19, 2.25),
                Norm(13.33, 4.32),
                Norm(16.56, 2.5),
                Norm(16.51, 2.93),
                Norm(14.05, 3.13),
                Norm(14.6, 3.78),
            ),
        ),
    },
    (Sex.MALE, AgeGroup.ELDERLY): {
        "N": DomainNorms(
            Norm(58.42, 15.48),
            (
                Norm(9.81, 3.54),
                Norm(11.46, 4.31),
                Norm(8.18, 3.59),
                Norm(11.08, 3.82),
                Norm(9.91, 3.36),
                Norm(8.24, 3.28),
            ),
        ),
        "E": DomainNorms(
            Norm(79.73, 13.63),
            (
                Norm(14.55, 3.47),
                Norm(11.19, 3.58),
                Norm(15.29, 3.1),
                Norm(12.81, 3.25),
                Norm(11.03, 2.88),
                Norm(15.02, 3.16),
            ),
        ),
        "O": DomainNorms(
            Norm(79.78, 12.21),
            (
                Norm(14.06, 3.13),
                Norm(14.22, 3.64),
                Norm(14.34, 2.9),
                Norm(12.42, 3.2),
                Norm(14.61, 3.89),
                Norm(10.11, 4.02),
            ),
        ),
        "A": DomainNorms(
            Norm(90.2, 11.73),
            (
                Norm(13.96, 3.13),
                Norm(17.74, 2.39),
                Norm(15.76, 2.74),
                Norm(16.18, 3.41),
                Norm(11.87, 3.5),
                Norm(14.0, 3.11),
            ),
        ),
        "C": DomainNorms(
            Norm(95.31, 11.99),
            (
                Norm(16.32, 2.31),
                Norm(14.41, 4.49),
                Norm(17.54, 2.3),
                Norm(16.65, 2.68),
                Norm(14.98, 2.76),
                Norm(15.18, 3.61),
            ),
        ),
    },
    (Sex.FEMALE, AgeGroup.YOUNG): {
        "N": DomainNorms(
            Norm(73.41, 15.61),
            (
                Norm(13.31, 3.62),
                Norm(13.09, 4.18),
                Norm(11.05, 4.2),
                Norm(12.11, 3.82),
                Norm(12.48, 3.3),
                Norm(11.3, 3.47),
            ),
        ),
        "E": DomainNorms(
            Norm(84.26, 14.98),
            (
                Norm(14.47, 3.6),
                Norm(13.12, 4.13),
                Norm(14.03, 3.68),
                Norm(12.67, 3.09),
                Norm(14.69, 3.48),
                Norm(15.34, 3.42),
            ),
        ),
        "O": DomainNorms(
            Norm(89.01, 11.84),
            (
                Norm(16.86, 2.89),
                Norm(15.93, 3.44),
                Norm(16.02, 2.95),
                Norm(12.95, 3.24),
                Norm(15.06, 3.51),
                Norm(12.17, 3.02),
            ),
        ),
        "A": DomainNorms(
            Norm(89.14, 13.21),
            (
                Norm(13.46, 3.72),
                Norm(16.11, 2.94),
                Norm(16.66, 2.69),
                Norm(13.73, 4.14),
                Norm(13.23, 3.79),
                Norm(15.7, 2.84),
            ),
        ),
        "C": DomainNorms(
            Norm(81.27, 14.38),
            (
                Norm(15.3, 2.54),
                Norm(11.11, 4.17),
                Norm(15.62, 2.76),
                Norm(14.69, 3.37),
                Norm(12.73, 3.19),
                Norm(11.82, 4.01),
            ),
        ),
    },
    (Sex.FEMALE, AgeGroup.ADULTS): {
        "N": DomainNorms(
            Norm(72.14, 16.16),
            (
                Norm(13.08, 3.68),
                Norm(12.72, 4.13),
                Norm(10.79, 4.07),
                Norm(12.2, 3.79),
                Norm(12.71, 3.58),
                Norm(10.69, 3.64),
            ),
        ),
        "E": DomainNorms(
            Norm(80.78, 14.64),
            (
                Norm(14.05, 3.66),
                Norm(11.92, 4.05),
                Norm(14.25, 3.61),
                Norm(12.77, 3.24),
                Norm(12.84, 3.53),
                Norm(14.96, 3.31),
            ),
        ),
        "O": DomainNorms(
            Norm(88.25, 12.15),
            (
                Norm(15.64, 3.34),
                Norm(15.97, 3.3),
                Norm(16.41, 2.69),
                Norm(12.84, 3.44),
                Norm(15.28, 3.47),
                Norm(12.06, 3.46),
            ),
        ),
        "A": DomainNorms(
            Norm(91.91, 11.39),
            (
                Norm(13.15, 3.71),
                Norm(17.34, 2.61),
                Norm(16.81, 2.53),
                Norm(15.57, 3.5),
                Norm(12.98, 3.57),
                Norm(15.52, 2.87),
            ),
        ),
        "C": DomainNorms(
            Norm(87.57, 13.87),
            (
                Norm(16.02, 2.34),
                Norm(12.67, 4.51),
                Norm(16.36, 2.54),
                Norm(16.11, 3.05),
                Norm(13.56, 3.23),
                Norm(12.91, 4.18),
            ),
        ),
    },
    (Sex.FEMALE, AgeGroup.MATURE): {
        "N": DomainNorms(
            Norm(67.38, 16.1),
            (
                Norm(12.05, 3.72),
                Norm(11.19, 4.03),
                Norm(10.07, 3.97),
                Norm(12.07, 3.73),
                Norm(11.98, 3.69),
                Norm(10.07, 3.56),
            ),
        ),
        "E": DomainNorms(
            Norm(78.62, 14.19),
            (
                Norm(14.1, 3.72),
                Norm(10.84, 3.86),
                Norm(14.51, 3.5),
                Norm(13.03, 3.46),
                Norm(11.08, 3.42),
                Norm(15.0, 3.26),
            ),
        ),
        "O": DomainNorms(
            Norm(86.15, 12.62),
            (
                Norm(14.43, 3.49),
                Norm(16.0, 3.2),
                Norm(16.37, 2.58),
                Norm(12.58, 3.45),
                Norm(14.87, 3.65),
                Norm(11.85, 3.74),
            ),
        ),
        "A": DomainNorms(
            Norm(95.73, 9.84),
            (
                Norm(13.79, 3.52),
                Norm(18.16, 2.21),
                Norm(17.04, 2.4),
                Norm(17.02, 2.88),
                Norm(13.41, 3.3),
                Norm(15.82, 2.71),
            ),
        ),
        "C": DomainNorms(
            Norm(93.45, 12.94),
            (
                Norm(16.5, 2.16),
                Norm(13.68, 4.51),
                Norm(17.29, 2.27),
                Norm(17.16, 2.73),
                Norm(14.35, 3.13),
                Norm(14.41, 3.86),
            ),
        ),
    },
    (Sex.FEMALE, AgeGroup.ELDERLY): {
        "N": DomainNorms(
            Norm(63.48, 14.92),
            (
                Norm(11.39, 3.61),
                Norm(10.52, 3.82),
                Norm(9.1, 3.68),
                Norm(12.0, 3.61),
                Norm(10.21, 3.58),
                Norm(9.87, 3.44),
            ),
        ),
        "E": DomainNorms(
            Norm(78.22, 12.73),
            (
                Norm(14.85, 3.43),
                Norm(10.93, 3.7),
                Norm(14.19, 3.64),
                Norm(12.76, 3.26),
                Norm(10.08, 3.2),
                Norm(15.65, 3.04),
            ),
        ),
        "O": DomainNorms(
            Norm(81.56, 12.66),
            (
                Norm(13.15, 3.71),
                Norm(15.95, 3.12),
                Norm(15.73, 2.74),
                Norm(11.8, 3.26),
                Norm(14.21, 3.47),
                Norm(10.81, 3.89),
            ),
        ),
        "A": DomainNorms(
            Norm(97.17, 9.52),
            (
                Norm(14.19, 3.39),
                Norm(18.64, 1.9),
                Norm(17.13, 2.18),
                Norm(17.98, 2.56),
                Norm(13.58, 3.38),
                Norm(15.83, 2.85),
            ),
        ),
        "C": DomainNorms(
            Norm(96.44, 12.43),
            (
                Norm(16.5, 2.24),
                Norm(15.15, 4.07),
                Norm(18.34, 1.81),
                Norm(17.19, 2.49),
                Norm(14.7, 3.15),
                Norm(15.11, 3.66),
            ),
        ),
    },
}

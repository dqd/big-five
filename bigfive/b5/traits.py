"""
The five personality domains of the Big Five model and their facets, together
with the texts of the report.

The descriptions are based on the IPIP-NEO narrative report by John A. Johnson.
"""

from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _

from .constants import Level


@dataclass(frozen=True, slots=True)
class Facet:
    key: str
    name: str
    description: str


@dataclass(frozen=True, slots=True)
class Domain:
    key: str
    # One-letter code used by the norms and the scoring: N, E, O, A or C.
    code: str
    name: str
    facets_title: str
    description: tuple[str, ...]
    # Interpretation of a low, an average and a high score.
    interpretations: dict[Level, str]
    # The six facets, in the order of the norms.
    facets: tuple[Facet, Facet, Facet, Facet, Facet, Facet]


@dataclass(frozen=True, slots=True)
class FacetResult:
    facet: Facet
    score: int
    level: Level


@dataclass(frozen=True, slots=True)
class DomainResult:
    domain: Domain
    score: int
    level: Level
    facets: list[FacetResult]

    @property
    def interpretation(self) -> str:
        return self.domain.interpretations[self.level]


def build_report(results: dict[str, int]) -> list[DomainResult]:
    """Combine the percentile estimates with the descriptions of the traits."""
    return [
        DomainResult(
            domain=domain,
            score=results[domain.key],
            level=Level.of(results[domain.key]),
            facets=[
                FacetResult(
                    facet=facet,
                    score=results[facet.key],
                    level=Level.of(results[facet.key]),
                )
                for facet in domain.facets
            ],
        )
        for domain in DOMAINS
    ]


EXTRAVERSION = Domain(
    key="extraversion",
    code="E",
    name=_("Extraversion"),
    facets_title=_("Extraversion facets"),
    description=(
        _(
            "<em>Extraversion</em> describes how strongly a person engages with the "
            "outside world. Extraverts enjoy being with people, are full of energy, "
            "and often experience positive emotions. They tend to be enthusiastic "
            "and action-oriented, the kind of people who say “Yes!” or “Let’s go!” "
            "to a chance for excitement. In groups they like to talk, assert "
            "themselves, and draw attention to themselves."
        ),
        _(
            "Introverts have less of the exuberance, energy, and activity of "
            "extraverts. They tend to be quiet, low-key, deliberate, and less "
            "involved in the social world. This should <em>not</em> be mistaken for "
            "shyness or depression: an introvert simply needs less stimulation than "
            "an extravert and prefers to be alone. Their independence and reserve "
            "are sometimes misread as unfriendliness or arrogance. In reality, an "
            "introvert who scores high on <em>Agreeableness</em> will not seek "
            "others out, but will be quite pleasant when approached."
        ),
    ),
    interpretations={
        Level.LOW: _(
            "Your score on <em>Extraversion</em> is low. You are introverted, "
            "reserved, and quiet. You enjoy solitude and solitary activities, and "
            "you tend to socialize with a few close friends."
        ),
        Level.AVERAGE: _(
            "Your score on <em>Extraversion</em> is average. You are neither a "
            "subdued loner nor a jovial chatterbox: you enjoy time with others, but "
            "also time alone."
        ),
        Level.HIGH: _(
            "Your score on <em>Extraversion</em> is high. You are sociable, "
            "outgoing, energetic, and lively, and you prefer to be around people "
            "much of the time."
        ),
    },
    facets=(
        Facet(
            key="friendliness",
            name=_("Friendliness"),
            description=_(
                "Friendly people genuinely like others and openly show them positive "
                "feelings. They make friends quickly and easily form close, intimate "
                "relationships. Low scorers are not necessarily cold or hostile, but "
                "they do not reach out to others and come across as distant and "
                "reserved."
            ),
        ),
        Facet(
            key="gregariousness",
            name=_("Gregariousness"),
            description=_(
                "Gregarious people find the company of others pleasantly stimulating "
                "and rewarding, and they enjoy the excitement of crowds. Low scorers "
                "tend to feel overwhelmed by large crowds and actively avoid them. "
                "They do not necessarily dislike company, but their need for privacy "
                "and time to themselves is much greater."
            ),
        ),
        Facet(
            key="assertiveness",
            name=_("Assertiveness"),
            description=_(
                "High scorers like to speak out, take charge, and direct the "
                "activities of others. They tend to lead groups. Low scorers tend not "
                "to talk much and let others run the show."
            ),
        ),
        Facet(
            key="activity_level",
            name=_("Activity level"),
            description=_(
                "Active people lead fast-paced, busy lives. They move quickly, "
                "energetically, and vigorously, and they are involved in many "
                "activities. Low scorers follow a slower, more leisurely, and relaxed "
                "pace."
            ),
        ),
        Facet(
            key="excitement_seeking",
            name=_("Excitement-seeking"),
            description=_(
                "High scorers are easily bored without a lot of stimulation. They "
                "love bright lights, hustle and bustle, and they are likely to take "
                "risks and seek thrills. Low scorers are overwhelmed by noise and "
                "commotion and avoid thrill-seeking."
            ),
        ),
        Facet(
            key="cheerfulness",
            name=_("Cheerfulness"),
            description=_(
                "This scale measures positive mood and feelings, not negative "
                "emotions (those belong to the <em>Neuroticism</em> domain). High "
                "scorers typically experience a range of positive feelings, "
                "including happiness, enthusiasm, optimism, and joy. Low scorers are "
                "less prone to such energetic high spirits."
            ),
        ),
    ),
)

AGREEABLENESS = Domain(
    key="agreeableness",
    code="A",
    name=_("Agreeableness"),
    facets_title=_("Agreeableness facets"),
    description=(
        _(
            "<em>Agreeableness</em> reflects how much a person values cooperation "
            "and social harmony. Agreeable people want to get along with others. "
            "They are therefore considerate, friendly, generous, helpful, and "
            "willing to compromise. They also have an optimistic view of human "
            "nature: they believe that people are basically honest, decent, and "
            "trustworthy."
        ),
        _(
            "Disagreeable people put self-interest above getting along with others. "
            "They are generally unconcerned with others’ well-being and therefore "
            "unlikely to go out of their way for other people. Sometimes their "
            "skepticism about others’ motives makes them suspicious, unfriendly, "
            "and uncooperative."
        ),
        _(
            "Agreeableness is obviously an advantage for gaining and keeping "
            "popularity: agreeable people are better liked than disagreeable "
            "people. On the other hand, it is not useful in situations that call "
            "for tough or strictly objective decisions. Disagreeable people can "
            "make excellent scientists, critics, or soldiers."
        ),
    ),
    interpretations={
        Level.LOW: _(
            "Your score on <em>Agreeableness</em> is low. You care less about "
            "others’ needs than about your own, and people see you as tough, "
            "critical, and uncompromising."
        ),
        Level.AVERAGE: _(
            "Your score on <em>Agreeableness</em> is average. You care about "
            "others’ needs to some extent, but you are generally unwilling to "
            "sacrifice yourself for others."
        ),
        Level.HIGH: _(
            "Your score on <em>Agreeableness</em> is high. You take a strong "
            "interest in others’ needs and well-being, and you are pleasant, "
            "sympathetic, and cooperative."
        ),
    },
    facets=(
        Facet(
            key="trust",
            name=_("Trust"),
            description=_(
                "People high in trust assume that most others are fair, honest, and "
                "well-meaning. People low in trust see others as selfish, devious, "
                "and potentially dangerous."
            ),
        ),
        Facet(
            key="morality",
            name=_("Morality"),
            description=_(
                "High scorers see no need for pretense or manipulation when dealing "
                "with others, so they are candid, frank, and sincere. Low scorers "
                "believe that a certain amount of deception is necessary in social "
                "relationships. Others find it easier to relate to straightforward "
                "high scorers than to guarded low scorers. Low scorers are "
                "<em>not</em> unprincipled or immoral; they are simply more cautious "
                "about revealing the whole truth."
            ),
        ),
        Facet(
            key="altruism",
            name=_("Altruism"),
            description=_(
                "Altruistic people find helping others genuinely rewarding, so they "
                "are generally willing to assist those in need. To them, doing "
                "things for others is a form of self-fulfillment rather than "
                "self-sacrifice. Low scorers do not particularly like helping those "
                "in need; requests for help feel like an imposition rather than an "
                "opportunity."
            ),
        ),
        Facet(
            key="cooperation",
            name=_("Cooperation"),
            description=_(
                "High scorers dislike confrontation. They are perfectly willing to "
                "compromise or to set their own needs aside in order to get along "
                "with others. Low scorers are more likely to intimidate others to "
                "get their way."
            ),
        ),
        Facet(
            key="modesty",
            name=_("Modesty"),
            description=_(
                "High scorers do not like to claim that they are better than other "
                "people. Sometimes this attitude stems from low self-confidence or "
                "self-esteem, but some people with high self-esteem simply find "
                "immodesty unseemly. Those who <em>are</em> willing to call "
                "themselves superior tend to be seen as disagreeably arrogant."
            ),
        ),
        Facet(
            key="sympathy",
            name=_("Sympathy"),
            description=_(
                "High scorers are tender-hearted and compassionate. They feel the "
                "pain of others and are easily moved to pity. Low scorers are not "
                "strongly affected by human suffering. They pride themselves on "
                "objective judgments based on reason, and they care more about "
                "truth and impartial justice than about mercy."
            ),
        ),
    ),
)

CONSCIENTIOUSNESS = Domain(
    key="conscientiousness",
    code="C",
    name=_("Conscientiousness"),
    facets_title=_("Conscientiousness facets"),
    description=(
        _(
            "<em>Conscientiousness</em> concerns the way we control, regulate, and "
            "direct our impulses. Impulses are not inherently bad. Sometimes time "
            "pressure calls for a snap decision, and acting on a first impulse can "
            "be an effective response. At play rather than at work, acting "
            "spontaneously can be fun, and impulsive people are often seen as "
            "colorful, fun to be with, and zany."
        ),
        _(
            "Nonetheless, acting on impulse can lead to trouble in a number of "
            "ways. Some impulses are antisocial, and uncontrolled antisocial acts "
            "harm others and invite retribution. Impulsive acts also tend to bring "
            "immediate rewards but undesirable long-term consequences: think of "
            "excessive socializing that leads to being fired, an insult that ends "
            "an important relationship, or drug use that eventually destroys "
            "one’s health."
        ),
        _(
            "Even when it is not seriously destructive, impulsive behavior makes a "
            "person less effective. Acting on impulse leaves no room to consider "
            "alternatives, some of which would have been wiser. Impulsivity also "
            "sidetracks people during projects that require an organized sequence "
            "of steps, so the accomplishments of an impulsive person tend to be "
            "small, scattered, and inconsistent."
        ),
        _(
            "A hallmark of intelligence is the ability to think about future "
            "consequences before acting on an impulse. Intelligent activity "
            "involves contemplating long-range goals, planning the route to them, "
            "and persisting in the face of short-lived impulses to the contrary. "
            "This is why <em>prudence</em>, meaning both wise and cautious, is an "
            "alternative label for this domain. People who score high on "
            "<em>Conscientiousness</em> are, in fact, perceived by others as "
            "intelligent."
        ),
        _(
            "The benefits of high conscientiousness are obvious. Conscientious "
            "people avoid trouble and achieve high levels of success through "
            "purposeful planning and persistence, and others regard them as "
            "intelligent and reliable. On the negative side, they can be "
            "compulsive perfectionists and workaholics, and extremely "
            "conscientious people may come across as stuffy and boring. "
            "Unconscientious people may be criticized for their unreliability, "
            "lack of ambition, and failure to stay within the lines, but they "
            "enjoy many short-lived pleasures and are never called stuffy."
        ),
    ),
    interpretations={
        Level.LOW: _(
            "Your score on <em>Conscientiousness</em> is low. You like to live for "
            "the moment and do what feels good now. Your work tends to be careless "
            "and disorganized."
        ),
        Level.AVERAGE: _(
            "Your score on <em>Conscientiousness</em> is average. You are "
            "reasonably reliable, organized, and self-controlled."
        ),
        Level.HIGH: _(
            "Your score on <em>Conscientiousness</em> is high. You set clear goals "
            "and pursue them with determination, and people regard you as reliable "
            "and hard-working."
        ),
    },
    facets=(
        Facet(
            key="self_efficacy",
            name=_("Self-efficacy"),
            description=_(
                "Self-efficacy is confidence in one’s ability to get things done. "
                "High scorers believe they have the intelligence (common sense), "
                "drive, and self-control needed to succeed. Low scorers do not feel "
                "effective and may feel that they are not in control of their lives."
            ),
        ),
        Facet(
            key="orderliness",
            name=_("Orderliness"),
            description=_(
                "High scorers are well organized. They like to live by routines and "
                "schedules, keep lists, and make plans. Low scorers tend to be "
                "disorganized and scattered."
            ),
        ),
        Facet(
            key="dutifulness",
            name=_("Dutifulness"),
            description=_(
                "This scale reflects the strength of a person’s sense of duty and "
                "obligation. High scorers have a strong sense of moral obligation. "
                "Low scorers find contracts, rules, and regulations overly confining "
                "and are likely to be seen as unreliable or even irresponsible."
            ),
        ),
        Facet(
            key="achievement_striving",
            name=_("Achievement-striving"),
            description=_(
                "High scorers strive hard for excellence. Their drive to be "
                "recognized as successful keeps them on track toward their lofty "
                "goals, and they often have a strong sense of direction in life. "
                "Extremely high scorers, however, may be too single-minded and "
                "obsessed with their work. Low scorers are content to get by with a "
                "minimum of work and may be seen by others as lazy."
            ),
        ),
        Facet(
            key="self_discipline",
            name=_("Self-discipline"),
            description=_(
                "Self-discipline, which many people call willpower, is the ability "
                "to persist at difficult or unpleasant tasks until they are "
                "completed. People with high self-discipline overcome their "
                "reluctance to begin tasks and stay on track despite distractions. "
                "People with low self-discipline procrastinate and show poor "
                "follow-through, often failing to complete even tasks they very "
                "much want to complete."
            ),
        ),
        Facet(
            key="cautiousness",
            name=_("Cautiousness"),
            description=_(
                "Cautiousness is the disposition to think through possibilities "
                "before acting. High scorers take their time when making decisions. "
                "Low scorers often say or do the first thing that comes to mind "
                "without weighing the alternatives and their probable consequences."
            ),
        ),
    ),
)

NEUROTICISM = Domain(
    key="neuroticism",
    code="N",
    name=_("Neuroticism"),
    facets_title=_("Neuroticism facets"),
    description=(
        _(
            "Freud originally used the term <em>neurosis</em> for a condition "
            "marked by mental distress, emotional suffering, and an inability to "
            "cope effectively with the normal demands of life. He suggested that "
            "everyone shows some signs of neurosis, but that we differ in how much "
            "we suffer and in our specific symptoms. Today <em>Neuroticism</em> "
            "refers to the tendency to experience negative feelings. High scorers "
            "may experience mainly one specific negative feeling, such as anxiety, "
            "anger, or depression, but they are likely to experience several of "
            "them."
        ),
        _(
            "People high in Neuroticism are emotionally reactive. They respond "
            "emotionally to events that would not affect most people, and their "
            "reactions tend to be more intense than usual. They are more likely to "
            "interpret ordinary situations as threatening and minor frustrations "
            "as hopelessly difficult. Their negative emotional reactions tend to "
            "persist for unusually long periods, which means they are often in a "
            "bad mood. These problems with emotional regulation can diminish their "
            "ability to think clearly, make decisions, and cope with stress."
        ),
        _(
            "At the other end of the scale, people who score low in Neuroticism "
            "are less easily upset and less emotionally reactive. They tend to be "
            "calm, emotionally stable, and free from persistent negative feelings. "
            "Freedom from negative feelings does not mean that low scorers "
            "experience a lot of positive feelings, though: the frequency of "
            "positive emotions is part of the <em>Extraversion</em> domain."
        ),
    ),
    interpretations={
        Level.LOW: _(
            "Your score on <em>Neuroticism</em> is low. You are exceptionally "
            "calm, composed, and unflappable, and you do not react with intense "
            "emotions even to situations that most people would call stressful."
        ),
        Level.AVERAGE: _(
            "Your score on <em>Neuroticism</em> is average. Your emotional "
            "reactivity is typical of the general population: stressful and "
            "frustrating situations are somewhat upsetting, but you are generally "
            "able to get over these feelings and cope."
        ),
        Level.HIGH: _(
            "Your score on <em>Neuroticism</em> is high. You are easily upset, even "
            "by what most people consider the normal demands of living, and people "
            "consider you sensitive and emotional."
        ),
    },
    facets=(
        Facet(
            key="anxiety",
            name=_("Anxiety"),
            description=_(
                "The “fight or flight” system in the brain of anxious people is "
                "engaged too easily and too often, so high scorers often feel that "
                "something dangerous is about to happen. They may fear specific "
                "situations or just be generally fearful, and they feel tense, "
                "jittery, and nervous. Low scorers are generally calm and fearless."
            ),
        ),
        Facet(
            key="anger",
            name=_("Anger"),
            description=_(
                "High scorers feel enraged when things do not go their way. They "
                "are sensitive about being treated fairly and feel resentful and "
                "bitter when they think they are being cheated. This scale measures "
                "the tendency to <em>feel</em> angry; whether a person "
                "<em>expresses</em> annoyance and hostility depends on their level "
                "of <em>Agreeableness</em>. Low scorers do not get angry often or "
                "easily."
            ),
        ),
        Facet(
            key="depression",
            name=_("Depression"),
            description=_(
                "This scale measures the tendency to feel sad, dejected, and "
                "discouraged. High scorers lack energy and have difficulty starting "
                "activities. Low scorers tend to be free from these depressive "
                "feelings."
            ),
        ),
        Facet(
            key="self_consciousness",
            name=_("Self-consciousness"),
            description=_(
                "Self-conscious people are sensitive about what others think of "
                "them. Their fear of rejection and ridicule makes them shy and "
                "uncomfortable around others; they are easily embarrassed and often "
                "feel ashamed. Their fear that others will criticize or mock them is "
                "exaggerated and unrealistic, but their awkwardness and discomfort "
                "may turn it into a self-fulfilling prophecy. Low scorers, in "
                "contrast, do not suffer from the mistaken impression that everyone "
                "is watching and judging them, and they do not feel nervous in "
                "social situations."
            ),
        ),
        Facet(
            key="immoderation",
            name=_("Immoderation"),
            description=_(
                "Immoderate people feel strong cravings and urges that they have "
                "difficulty resisting. They tend to be oriented toward short-term "
                "pleasures and rewards rather than long-term consequences. Low "
                "scorers do not experience strong, irresistible cravings and are "
                "therefore not tempted to overindulge."
            ),
        ),
        Facet(
            key="vulnerability",
            name=_("Vulnerability"),
            description=_(
                "High scorers experience panic, confusion, and helplessness under "
                "pressure or stress. Low scorers feel more poised, confident, and "
                "clear-headed when stressed."
            ),
        ),
    ),
)

OPENNESS = Domain(
    key="openness",
    code="O",
    name=_("Openness to experience"),
    facets_title=_("Openness to experience facets"),
    description=(
        _(
            "<em>Openness to experience</em> describes a dimension of cognitive "
            "style that distinguishes imaginative, creative people from "
            "down-to-earth, conventional people. Open people are intellectually "
            "curious, appreciate art, and are sensitive to beauty. Compared with "
            "closed people, they tend to be more aware of their feelings, and they "
            "think and act in individualistic and nonconforming ways. "
            "Intellectuals typically score high on this domain, which is why it "
            "has also been called <em>Culture</em> or <em>Intellect</em>. "
            "Intellect is probably best regarded as just one aspect of openness, "
            "though: scores on <em>Openness to experience</em> are only modestly "
            "related to years of education and to scores on standard intelligence "
            "tests."
        ),
        _(
            "Another characteristic of the open cognitive style is a facility for "
            "thinking in symbols and abstractions far removed from concrete "
            "experience. Depending on the person’s specific intellectual "
            "abilities, this may take the form of mathematical, logical, or "
            "geometric thinking, an artistic and metaphorical use of language, "
            "composing or performing music, or one of the many visual or "
            "performing arts. People with low scores tend to have narrow, common "
            "interests. They prefer the plain, straightforward, and obvious over "
            "the complex, ambiguous, and subtle. They may regard the arts and "
            "sciences with suspicion, as abstruse or of no practical use. Closed "
            "people prefer familiarity over novelty: they are conservative and "
            "resistant to change."
        ),
        _(
            "Psychologists, who are often themselves open to experience, tend to "
            "present openness as healthier or more mature. However, open and "
            "closed styles of thinking are useful in different environments. The "
            "intellectual style of an open person may serve a professor well, but "
            "research has shown that closed thinking is related to superior job "
            "performance in police work, sales, and a number of service "
            "occupations."
        ),
    ),
    interpretations={
        Level.LOW: _(
            "Your score on <em>Openness to experience</em> is low. You like to "
            "think in plain and simple terms, and others describe you as "
            "down-to-earth, practical, and conservative."
        ),
        Level.AVERAGE: _(
            "Your score on <em>Openness to experience</em> is average. You enjoy "
            "tradition but are willing to try new things. Your thinking is neither "
            "simple nor complex, and to others you appear to be a well-educated "
            "person but not an intellectual."
        ),
        Level.HIGH: _(
            "Your score on <em>Openness to experience</em> is high. You enjoy "
            "novelty, variety, and change, and you are curious, imaginative, and "
            "creative."
        ),
    },
    facets=(
        Facet(
            key="imagination",
            name=_("Imagination"),
            description=_(
                "To imaginative people, the real world is often too plain and "
                "ordinary. High scorers use fantasy to create a richer, more "
                "interesting world. Low scorers are more oriented toward facts than "
                "fantasy."
            ),
        ),
        Facet(
            key="artistic_interests",
            name=_("Artistic interests"),
            description=_(
                "High scorers love beauty, both in art and in nature. They easily "
                "become involved and absorbed in artistic and natural events. They "
                "are not necessarily artistically trained or talented, although "
                "many are: what defines this scale is <em>interest in</em> and "
                "<em>appreciation of</em> natural and artificial beauty. Low scorers "
                "lack aesthetic sensitivity and interest in the arts."
            ),
        ),
        Facet(
            key="emotionality",
            name=_("Emotionality"),
            description=_(
                "High scorers have good access to and awareness of their own "
                "feelings. Low scorers are less aware of their feelings and tend "
                "not to express their emotions openly."
            ),
        ),
        Facet(
            key="adventurousness",
            name=_("Adventurousness"),
            description=_(
                "High scorers are eager to try new activities, travel to foreign "
                "lands, and experience different things. They find familiarity and "
                "routine boring, and they will take a new route home just because "
                "it is different. Low scorers tend to feel uncomfortable with change "
                "and prefer familiar routines."
            ),
        ),
        Facet(
            key="intellect",
            name=_("Intellect"),
            description=_(
                "Intellect and artistic interests are the two most central aspects "
                "of openness to experience. High scorers love to play with ideas. "
                "They are open to new and unusual ideas, like to debate "
                "intellectual issues, and enjoy riddles, puzzles, and brain "
                "teasers. Low scorers prefer dealing with people or things rather "
                "than ideas, and they regard intellectual exercises as a waste of "
                "time. Intellect should <em>not</em> be equated with intelligence: "
                "it is an intellectual style, not an intellectual ability, although "
                "high scorers do score <em>slightly</em> higher than low scorers on "
                "standardized intelligence tests."
            ),
        ),
        Facet(
            key="liberalism",
            name=_("Liberalism"),
            description=_(
                "Psychological liberalism is a readiness to challenge authority, "
                "convention, and traditional values. In its most extreme form it "
                "can even mean outright hostility toward rules, sympathy for "
                "law-breakers, and a love of ambiguity, chaos, and disorder. "
                "Psychological conservatives prefer the security and stability that "
                "come with conformity to tradition. Psychological liberalism and "
                "conservatism are not the same as political affiliation, but they "
                "certainly incline people toward certain political parties."
            ),
        ),
    ),
)

# In the order of the report.
DOMAINS = (EXTRAVERSION, AGREEABLENESS, CONSCIENTIOUSNESS, NEUROTICISM, OPENNESS)

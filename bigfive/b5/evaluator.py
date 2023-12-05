from .constants import Response, NORMS

CONST1 = 210.335958661391
CONST2 = 16.7379362643389
CONST3 = 0.405936512733332
CONST4 = 0.00270624341822222

ITERATIONS = 7


def approximate(criterion):
    """
    Cubic approximations for percentiles.
    """
    result = int(
        CONST1
        - (CONST2 * criterion)
        + (CONST3 * criterion**2)
        - (CONST4 * criterion**3)
    )

    if criterion < 32:
        return 1

    if criterion > 73:
        return 99

    return result


def evaluate(sex, age_group, answers):
    """
    Evaluate the Big Five personality traits questionnaire.
    Original code: https://github.com/kholia/IPIP-NEO-PI/blob/21.06/app/evaluator.py
    """
    count = len(answers) + 1
    Q = [Response.NEITHER.value] * count

    possibilities = range(0, len(Response.values) + 1)

    for i, answer in enumerate(answers):
        try:
            Q[i + 1] = possibilities[int(answer["answer"]) * int(answer["ordering"])]
        except Exception:
            pass

    # Score facet scales
    ss = [0] * count

    for i in range(1, 31):
        k = 0

        for _ in range(0, 4):
            ss[i] += Q[i + k]
            k += 30

    # Number each facet set from 1-6
    NF = [0] * (ITERATIONS + 1)
    EF = [0] * (ITERATIONS + 1)
    OF = [0] * (ITERATIONS + 1)
    AF = [0] * (ITERATIONS + 1)
    CF = [0] * (ITERATIONS + 1)
    j = 0

    for i in range(1, ITERATIONS):
        NF[i] = ss[i + j]
        EF[i] = ss[i + j + 1]
        OF[i] = ss[i + j + 2]
        AF[i] = ss[i + j + 3]
        CF[i] = ss[i + j + 4]
        j += 4

    # Score domain scales
    #           1       2        3        4        5        6
    domain_scales = {
        "N": ss[1] + ss[6] + ss[11] + ss[16] + ss[21] + ss[26],
        "E": ss[2] + ss[7] + ss[12] + ss[17] + ss[22] + ss[27],
        "O": ss[3] + ss[8] + ss[13] + ss[18] + ss[23] + ss[28],
        "A": ss[4] + ss[9] + ss[14] + ss[19] + ss[24] + ss[29],
        "C": ss[5] + ss[10] + ss[15] + ss[20] + ss[25] + ss[30],
    }

    # Standardize scores
    norm = NORMS[sex][age_group]

    SN = (10 * (domain_scales["N"] - norm[1]) / norm[6]) + 50
    SE = (10 * (domain_scales["E"] - norm[2]) / norm[7]) + 50
    SO = (10 * (domain_scales["O"] - norm[3]) / norm[8]) + 50
    SA = (10 * (domain_scales["A"] - norm[4]) / norm[9]) + 50
    SC = (10 * (domain_scales["C"] - norm[5]) / norm[10]) + 50

    SNF = [0] * (ITERATIONS + 1)
    SEF = [0] * (ITERATIONS + 1)
    SOF = [0] * (ITERATIONS + 1)
    SAF = [0] * (ITERATIONS + 1)
    SCF = [0] * (ITERATIONS + 1)

    for i in range(1, ITERATIONS):
        SNF[i] = 50 + (10 * (NF[i] - norm[i + 10]) / norm[i + 16])
        SEF[i] = 50 + (10 * (EF[i] - norm[i + 22]) / norm[i + 28])
        SOF[i] = 50 + (10 * (OF[i] - norm[i + 34]) / norm[i + 40])
        SAF[i] = 50 + (10 * (AF[i] - norm[i + 46]) / norm[i + 52])
        SCF[i] = 50 + (10 * (CF[i] - norm[i + 58]) / norm[i + 64])

    # Approximations for percentiles
    SNP = approximate(SN)
    SEP = approximate(SE)
    SOP = approximate(SO)
    SAP = approximate(SA)
    SCP = approximate(SC)

    # Create percentile scores
    SNFP = [0] * (ITERATIONS + 1)
    SEFP = [0] * (ITERATIONS + 1)
    SOFP = [0] * (ITERATIONS + 1)
    SAFP = [0] * (ITERATIONS + 1)
    SCFP = [0] * (ITERATIONS + 1)

    for i in range(1, ITERATIONS):
        SNFP[i] = approximate(SNF[i])
        SEFP[i] = approximate(SEF[i])
        SOFP[i] = approximate(SOF[i])
        SAFP[i] = approximate(SAF[i])
        SCFP[i] = approximate(SCF[i])

    return {
        "extraversion": SEP,
        "friendliness": SEFP[1],
        "gregariousness": SEFP[2],
        "assertiveness": SEFP[3],
        "activity_level": SEFP[4],
        "excitement_seeking": SEFP[5],
        "cheerfulness": SEFP[6],
        "agreeableness": SAP,
        "trust": SAFP[1],
        "morality": SAFP[2],
        "altruism": SAFP[3],
        "cooperation": SAFP[4],
        "modesty": SAFP[5],
        "sympathy": SAFP[6],
        "conscientiousness": SCP,
        "self_efficacy": SCFP[1],
        "orderliness": SCFP[2],
        "dutifulness": SCFP[3],
        "achievement_striving": SCFP[4],
        "self_discipline": SCFP[5],
        "cautiousness": SCFP[6],
        "neuroticism": SNP,
        "anxiety": SNFP[1],
        "anger": SNFP[2],
        "depression": SNFP[3],
        "self_consciousness": SNFP[4],
        "immoderation": SNFP[5],
        "vulnerability": SNFP[6],
        "openness": SOP,
        "imagination": SOFP[1],
        "artistic_interests": SOFP[2],
        "emotionality": SOFP[3],
        "adventurousness": SOFP[4],
        "intellect": SOFP[5],
        "liberalism": SOFP[6],
    }

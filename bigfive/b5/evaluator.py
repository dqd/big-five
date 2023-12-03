from .constants import Response, NORMS


def evaluate(sex, age_group, answers):
    count = len(answers) + 1
    Q = [Response.NEITHER.value] * count

    possibilities = range(0, len(Response.values) + 1)

    for i, answer in enumerate(answers):
        try:
            Q[i] = possibilities[int(answer["answer"]) * int(answer["ordering"])]
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
    NF = [0] * count
    EF = [0] * count
    OF = [0] * count
    AF = [0] * count
    CF = [0] * count
    j = 0
    for i in range(1, 7):
        NF[i] = ss[i + j]
        EF[i] = ss[i + j + 1]
        OF[i] = ss[i + j + 2]
        AF[i] = ss[i + j + 3]
        CF[i] = ss[i + j + 4]
        j = j + 4

    # Score domain scales
    #      1       2         3        4        5        6
    N = ss[1] + ss[6] + ss[11] + ss[16] + ss[21] + ss[26]
    E = ss[2] + ss[7] + ss[12] + ss[17] + ss[22] + ss[27]
    O = ss[3] + ss[8] + ss[13] + ss[18] + ss[23] + ss[28]
    A = ss[4] + ss[9] + ss[14] + ss[19] + ss[24] + ss[29]
    C = ss[5] + ss[10] + ss[15] + ss[20] + ss[25] + ss[30]

    # Standardize scores
    norm = NORMS[sex][age_group]

    SN = (10 * (N - norm[1]) / norm[6]) + 50
    SE = (10 * (E - norm[2]) / norm[7]) + 50
    SO = (10 * (O - norm[3]) / norm[8]) + 50
    SA = (10 * (A - norm[4]) / norm[9]) + 50
    SC = (10 * (C - norm[5]) / norm[10]) + 50

    SNF = [0] * count
    SEF = [0] * count
    SOF = [0] * count
    SAF = [0] * count
    SCF = [0] * count

    for i in range(1, 7):
        SNF[i] = 50 + (10 * (NF[i] - norm[i + 10]) / norm[i + 16])
        SEF[i] = 50 + (10 * (EF[i] - norm[i + 22]) / norm[i + 28])
        SOF[i] = 50 + (10 * (OF[i] - norm[i + 34]) / norm[i + 40])
        SAF[i] = 50 + (10 * (AF[i] - norm[i + 46]) / norm[i + 52])
        SCF[i] = 50 + (10 * (CF[i] - norm[i + 58]) / norm[i + 64])

    # Cubic approximations for percentiles

    CONST1 = 210.335958661391
    CONST2 = 16.7379362643389
    CONST3 = 0.405936512733332
    CONST4 = 0.00270624341822222

    SNP = int(CONST1 - (CONST2 * SN) + (CONST3 * SN**2) - (CONST4 * SN**3))
    SEP = int(CONST1 - (CONST2 * SE) + (CONST3 * SE**2) - (CONST4 * SE**3))
    SOP = int(CONST1 - (CONST2 * SO) + (CONST3 * SO**2) - (CONST4 * SO**3))
    SAP = int(CONST1 - (CONST2 * SA) + (CONST3 * SA**2) - (CONST4 * SA**3))
    SCP = int(CONST1 - (CONST2 * SC) + (CONST3 * SC**2) - (CONST4 * SC**3))

    if SN < 32:
        SNP = 1
    if SE < 32:
        SEP = 1
    if SO < 32:
        SOP = 1
    if SA < 32:
        SAP = 1
    if SC < 32:
        SCP = 1

    if SN > 73:
        SNP = 99
    if SE > 73:
        SEP = 99
    if SO > 73:
        SOP = 99
    if SA > 73:
        SAP = 99
    if SC > 73:
        SCP = 99

    # Create percentile scores
    SNFP = [0] * count
    SEFP = [0] * count
    SOFP = [0] * count
    SAFP = [0] * count
    SCFP = [0] * count

    for i in range(1, 7):
        SNFP[i] = int(
            CONST1 - (CONST2 * SNF[i]) + (CONST3 * SNF[i] ** 2) - (CONST4 * SNF[i] ** 3)
        )

        if SNF[i] < 32:
            SNFP[i] = 1

        if SNF[i] > 73:
            SNFP[i] = 99

    for i in range(1, 7):
        SEFP[i] = int(
            CONST1 - (CONST2 * SEF[i]) + (CONST3 * SEF[i] ** 2) - (CONST4 * SEF[i] ** 3)
        )

        if SEF[i] < 32:
            SEFP[i] = 1
        if SEF[i] > 73:
            SEFP[i] = 99

    for i in range(1, 7):
        SOFP[i] = int(
            CONST1 - (CONST2 * SOF[i]) + (CONST3 * SOF[i] ** 2) - (CONST4 * SOF[i] ** 3)
        )

        if SOF[i] < 32:
            SOFP[i] = 1
        if SOF[i] > 73:
            SOFP[i] = 99

    for i in range(1, 7):
        SAFP[i] = int(
            CONST1 - (CONST2 * SAF[i]) + (CONST3 * SAF[i] ** 2) - (CONST4 * SAF[i] ** 3)
        )

        if SAF[i] < 32:
            SAFP[i] = 1
        if SAF[i] > 73:
            SAFP[i] = 99

    for i in range(1, 7):
        SCFP[i] = int(
            CONST1 - (CONST2 * SCF[i]) + (CONST3 * SCF[i] ** 2) - (CONST4 * SCF[i] ** 3)
        )

        if SCF[i] < 32:
            SCFP[i] = 1
        if SCF[i] > 73:
            SCFP[i] = 99

    m = {}

    labels = [
        "EXTRAVERSION",
        "Friendliness",
        "Gregariousness",
        "Assertiveness",
        "Activity Level",
        "Excitement-Seeking",
        "Cheerfulness",
    ]
    m[labels[0]] = SEP
    for i in range(1, len(labels)):
        m[labels[i]] = SEFP[i]

    labels = [
        "AGREEABLENESS",
        "Trust",
        "Morality",
        "Altruism",
        "Cooperation",
        "Modesty",
        "Sympathy",
    ]
    m[labels[0]] = SAP
    for i in range(1, len(labels)):
        m[labels[i]] = SAFP[i]

    labels = [
        "CONSCIENTIOUSNESS",
        "Self-Efficacy",
        "Orderliness",
        "Dutifulness",
        "Achievement-Striving",
        "Self-Discipline",
        "Cautiousness",
    ]
    m[labels[0]] = SCP
    for i in range(1, len(labels)):
        m[labels[i]] = SCFP[i]

    labels = [
        "NEUROTICISM",
        "Anxiety",
        "Anger",
        "Depression",
        "Self-Consciousness",
        "Immoderation",
        "Vulnerability",
    ]
    m[labels[0]] = SNP
    for i in range(1, len(labels)):
        m[labels[i]] = SNFP[i]

    labels = [
        "OPENNESS",
        "Imagination",
        "Artistic Interests",
        "Emotionality",
        "Adventurousness",
        "Intellect",
        "Liberalism",
    ]
    m[labels[0]] = SOP
    for i in range(1, len(labels)):
        m[labels[i]] = SOFP[i]

    return m

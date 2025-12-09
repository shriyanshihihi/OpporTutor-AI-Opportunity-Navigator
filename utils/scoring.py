def year_match_score(opp, profile):
    year = profile["year"]
    min_year = opp.get("year_min", 1)
    max_year = opp.get("year_max", 4)

    if min_year <= year <= max_year:
        return 0.15
    elif abs(year - min_year) == 1 or abs(year - max_year) == 1:
        return 0.05
    return -0.10


def location_score(opp, profile):
    pref = profile["location_pref"]
    opp_loc = opp["location"]

    if pref == "no preference":
        return 0.00

    if pref == opp_loc:
        return 0.12
    elif pref in ["remote", "hybrid"] and opp_loc in ["remote", "hybrid"]:
        return 0.05

    return -0.05


def stipend_score(opp, profile):
    if not profile["needs_stipend"]:
        return 0.00

    if opp["stipend"]:
        return 0.10
    return -0.10


def inclusion_score(opp, profile):
    score = 0.0

    if profile["is_female"] and "women" in opp["inclusive_flags"]:
        score += 0.20

    if profile["low_income"] and "low-income" in opp["inclusive_flags"]:
        score += 0.15

    if opp["inclusive_flags"]:
        score += 0.03

    return score


def tag_relevance_score(opp, profile):
    interests = profile["interests"].lower().split()
    tags = [t.lower() for t in opp.get("tags", [])]

    common = len(set(interests).intersection(tags))

    if common >= 2:
        return 0.12
    elif common == 1:
        return 0.05
    return 0.00


def penalty_for_irrelevant(opp, profile):
    interests = profile["interests"].lower()
    desc = opp["description"].lower()

    if not any(w in desc for w in interests.split()):
        return -0.05
    return 0.0


def total_score(base_similarity, opp, profile, return_details=False):
    """Returns final score AND optionally detailed explanation."""
    details = {}

    # semantic
    sim = base_similarity
    details["Semantic Similarity"] = round(sim, 3)

    # scoring components
    yr = year_match_score(opp, profile)
    loc = location_score(opp, profile)
    stipend = stipend_score(opp, profile)
    inc = inclusion_score(opp, profile)
    tag = tag_relevance_score(opp, profile)
    pen = penalty_for_irrelevant(opp, profile)

    details["Year Match"] = yr
    details["Location Match"] = loc
    details["Stipend Match"] = stipend
    details["Inclusion Match"] = inc
    details["Interest-Tag Match"] = tag
    details["Irrelevance Penalty"] = pen

    final = sim + yr + loc + stipend + inc + tag + pen

    if return_details:
        return final, details

    return final

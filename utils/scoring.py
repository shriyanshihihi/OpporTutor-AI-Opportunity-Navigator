"""
scoring.py

Handles all scoring logic for ranking opportunities.
This file keeps the scoring rules clean, modular, and easy to tweak.
"""

def score_similarity(base_similarity: float) -> float:
    """Base AI similarity score."""
    return base_similarity


def score_year(opp, profile):
    year = profile.get("year")
    if opp["year_min"] <= year <= opp["year_max"]:
        return 0.15
    return -0.10


def score_location(opp, profile):
    pref = profile.get("location_pref", "no preference").lower()
    location = opp["location"].lower()

    if pref == "no preference":
        return 0.05
    if pref in location:
        return 0.10
    return -0.05


def score_stipend(opp, profile):
    needs = profile.get("needs_stipend", False)
    if needs and opp["stipend"]:
        return 0.10
    if needs and not opp["stipend"]:
        return -0.05
    return 0.0


def score_inclusivity(opp, profile):
    score = 0.0

    if profile.get("is_female") and "women" in opp["inclusive_flags"]:
        score += 0.20

    if profile.get("low_income") and "low-income" in opp["inclusive_flags"]:
        score += 0.15

    return score


def total_score(base_similarity, opp, profile):
    """
    Combines all scoring rules into a final score.
    Called from model.py for each opportunity.
    """
    score = 0

    score += score_similarity(base_similarity)
    score += score_year(opp, profile)
    score += score_location(opp, profile)
    score += score_stipend(opp, profile)
    score += score_inclusivity(opp, profile)

    return score

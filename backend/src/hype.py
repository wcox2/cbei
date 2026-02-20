from models import Team
from typing import Optional

# AP Poll ranking tier thresholds and their base hype scores
AP_TIERS = {
    "elite": {"range": range(1, 6),   "score": 100},  # 1-5
    "high":  {"range": range(6, 10),  "score": 80},   # 6-9
    "mid":   {"range": range(10, 16), "score": 60},   # 10-15
    "low":   {"range": range(16, 26), "score": 40},   # 16-25
}

# When one team is unranked, the ranked team's hype is reduced
SINGLE_RANKED_MULTIPLIER = 0.6

# KenPom rank thresholds for unranked teams
KENPOM_TIERS = {
    50:  0.9,   # top 50 unranked team — close to ranked quality
    100: 0.75,  # top 100
    200: 0.6,   # outside top 100
}

def get_effective_ranks(team: Team) -> tuple[Optional[int], Optional[int]]:
    """
    Return the effective AP and KenPom ranks for a team.
    Falls back to previous season data if current season rankings
    are not yet available (early season).
    """
    ap_rank = team.ap_rank or team.previous_season_ap_rank
    kenpom_rank = team.kenpom_rank or team.previous_season_kenpom_rank
    return ap_rank, kenpom_rank

def get_ap_tier_score(rank: int) -> int:
    """Return the base hype score for a given AP rank."""
    for tier in AP_TIERS.values():
        if rank in tier["range"]:
            return tier["score"]
    raise ValueError(f"Invalid AP rank: {rank}. Must be between 1 and 25.")


def get_ranking_gap_penalty(rank_a: int, rank_b: int) -> float:
    """
    Calculate penalty for large ranking gaps between two ranked teams.
    Each position difference subtracts 2 points.
    e.g. #3 vs #18 = 15 positions apart = -30 points
    """
    gap = abs(rank_a - rank_b)
    return gap * 2


def get_kenpom_multiplier(kenpom_rank: int) -> float:
    """Return hype multiplier for an unranked team based on KenPom rank."""
    for threshold, multiplier in KENPOM_TIERS.items():
        if kenpom_rank <= threshold:
            return multiplier
    return 0.5  # outside top 200 — low quality unranked team


def calculate_hype(home_team: Team, away_team: Team) -> float:
    """
    Calculate the hype score (0-100) for a matchup based on AP rankings
    and KenPom ratings.

    Three scenarios:
    1. Both ranked — base score from higher team, penalized for gap
    2. One ranked — base score reduced by SINGLE_RANKED_MULTIPLIER,
                    further adjusted by unranked team's KenPom rank
    3. Neither ranked — KenPom-driven score with a ceiling of 40
    """
    home_rank, home_kenpom = get_effective_ranks(home_team)
    away_rank, away_kenpom = get_effective_ranks(away_team)

    # --- Scenario 1: Both ranked ---
    if home_rank and away_rank:
        base_score = get_ap_tier_score(min(home_rank, away_rank))
        penalty = get_ranking_gap_penalty(home_rank, away_rank)
        return max(0, base_score - penalty)

    # --- Scenario 2: One ranked ---
    if bool(home_rank) != bool(away_rank):
        ranked_rank = home_rank or away_rank
        unranked_team = away_team if home_rank else home_team
        base_score = get_ap_tier_score(ranked_rank) * SINGLE_RANKED_MULTIPLIER

        if unranked_team.kenpom_rank:
            kenpom_multiplier = get_kenpom_multiplier(unranked_team.kenpom_rank)
            return base_score * kenpom_multiplier

        return base_score

    # --- Scenario 3: Neither ranked ---
    if home_team.kenpom_rank and away_team.kenpom_rank:
        avg_kenpom = (home_team.kenpom_rank + away_team.kenpom_rank) / 2
        # Normalize to 0-40 ceiling (unranked games have lower hype cap)
        return max(0, 40 - (avg_kenpom / 10))

    return 20  # default fallback if no data available
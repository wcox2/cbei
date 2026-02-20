import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from models import Team
from hype import calculate_hype


class TestBothRanked:
    def test_close_rankings_produces_high_hype(self):
        """#3 vs #5 should produce a high hype score."""
        home = Team(name="Duke", ap_rank=3, kenpom_rank=3)
        away = Team(name="Kentucky", ap_rank=5, kenpom_rank=5)
        score = calculate_hype(home, away)
        assert score >= 80, f"Expected >= 80 for close top-5 matchup, got {score}"

    def test_far_apart_rankings_produces_lower_hype(self):
        """#1 vs #25 should score lower than #1 vs #5."""
        close_matchup_home = Team(name="Kansas", ap_rank=1, kenpom_rank=1)
        close_matchup_away = Team(name="Duke", ap_rank=5, kenpom_rank=5)
        far_matchup_home = Team(name="Kansas", ap_rank=1, kenpom_rank=1)
        far_matchup_away = Team(name="Arkansas", ap_rank=25, kenpom_rank=22)

        close_score = calculate_hype(close_matchup_home, close_matchup_away)
        far_score = calculate_hype(far_matchup_home, far_matchup_away)

        assert close_score > far_score, (
            f"Expected close matchup ({close_score}) to outscore "
            f"far matchup ({far_score})"
        )


class TestOneRanked:
    def test_single_ranked_team_reduces_hype(self):
        """One ranked team should score lower than two ranked teams at same level."""
        both_ranked_home = Team(name="Duke", ap_rank=3, kenpom_rank=3)
        both_ranked_away = Team(name="Kentucky", ap_rank=5, kenpom_rank=5)
        both_score = calculate_hype(both_ranked_home, both_ranked_away)

        one_ranked_home = Team(name="Duke", ap_rank=3, kenpom_rank=3)
        one_ranked_away = Team(name="Davidson", ap_rank=None, kenpom_rank=45)
        one_score = calculate_hype(one_ranked_home, one_ranked_away)

        assert both_score > one_score, (
            f"Expected both ranked ({both_score}) to outscore "
            f"one ranked ({one_score})"
        )

    def test_high_kenpom_unranked_boosts_hype(self):
        """An unranked top-50 KenPom team should score higher than a top-200 team."""
        home = Team(name="Duke", ap_rank=3, kenpom_rank=3)

        strong_unranked = Team(name="Davidson", ap_rank=None, kenpom_rank=30)
        weak_unranked = Team(name="Wofford", ap_rank=None, kenpom_rank=180)

        strong_score = calculate_hype(home, strong_unranked)
        weak_score = calculate_hype(home, weak_unranked)

        assert strong_score > weak_score, (
            f"Expected strong unranked ({strong_score}) to outscore "
            f"weak unranked ({weak_score})"
        )
    
    def test_early_season_fallback_uses_previous_rankings(self):
        """When no current rankings exist, previous season data should be used."""
        home = Team(
            name="Duke",
            ap_rank=None,
            kenpom_rank=None,
            previous_season_ap_rank=3,
            previous_season_kenpom_rank=3
        )
        away = Team(
            name="Kentucky",
            ap_rank=None,
            kenpom_rank=None,
            previous_season_ap_rank=5,
            previous_season_kenpom_rank=5
        )
        score = calculate_hype(home, away)
        assert score >= 80, f"Expected high hype using previous season ranks, got {score}"

    def test_unranked_team_with_no_kenpom_still_scores(self):
        """One ranked team vs unranked team with no KenPom data should still return a score."""
        home = Team(name="Duke", ap_rank=3, kenpom_rank=3)
        away = Team(name="Unknown", ap_rank=None, kenpom_rank=None)
        score = calculate_hype(home, away)
        assert score > 0, f"Expected score > 0 with no KenPom data, got {score}"

    def test_very_weak_unranked_team_low_hype(self):
        """One ranked team vs a very weak unranked team (KenPom > 200) should use 0.5 multiplier."""
        home = Team(name="Duke", ap_rank=3, kenpom_rank=3)
        away = Team(name="Weak Team", ap_rank=None, kenpom_rank=250)
        score = calculate_hype(home, away)
        assert score > 0, f"Expected score > 0, got {score}"


class TestNeitherRanked:
    def test_kenpom_data_produces_reasonable_score(self):
        """Two unranked teams with KenPom data should score between 0 and 40."""
        home = Team(name="Davidson", ap_rank=None, kenpom_rank=60)
        away = Team(name="Wofford", ap_rank=None, kenpom_rank=80)
        score = calculate_hype(home, away)
        assert 0 <= score <= 40, f"Expected score between 0-40, got {score}"

    def test_no_data_returns_fallback(self):
        """No rankings or KenPom data should return the default fallback score."""
        home = Team(name="Unknown A", ap_rank=None, kenpom_rank=None)
        away = Team(name="Unknown B", ap_rank=None, kenpom_rank=None)
        score = calculate_hype(home, away)
        assert score == 20, f"Expected fallback score of 20, got {score}"
    
    def test_low_quality_kenpom_produces_low_score(self):
        """Two teams outside KenPom top 200 should produce a low hype score."""
        home = Team(name="Team A", ap_rank=None, kenpom_rank=280)
        away = Team(name="Team B", ap_rank=None, kenpom_rank=310)
        score = calculate_hype(home, away)
        assert score <= 20, f"Expected low score for weak unranked teams, got {score}"

class TestHelpers:
    def test_invalid_ap_rank_raises_error(self):
        """Passing a rank outside 1-25 to get_ap_tier_score should raise ValueError."""
        from hype import get_ap_tier_score
        with pytest.raises(ValueError, match="Invalid AP rank"):
            get_ap_tier_score(30)
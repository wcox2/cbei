from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class GameState(Enum):
    PRE_GAME = "pre_game"
    LIVE = "live"
    FINAL = "final"


class Tier(Enum):
    ELITE = "Elite Game"
    GOOD = "Good Watch"
    AVERAGE = "Average"
    SKIP = "Skip"


@dataclass
class Team:
    name: str
    ap_rank: Optional[int] = None        # None if unranked
    kenpom_rank: Optional[int] = None    # None if unavailable


@dataclass
class GameSnapshot:
    """Represents game state at a single point in time (every 15 min update)."""
    clock_seconds_remaining: int         # seconds left in game (0 = final)
    home_score: int
    away_score: int
    lead_changes: int                    # total lead changes so far
    home_fg_made: int                    # field goals made by home team
    away_fg_made: int                    # field goals made by away team
    possessions: int                     # estimated total possessions so far
    overtime_periods: int = 0


@dataclass
class Game:
    game_id: str
    home_team: Team
    away_team: Team
    state: GameState
    snapshots: list[GameSnapshot] = field(default_factory=list)
    final_snapshot: Optional[GameSnapshot] = None
    predicted_score: Optional[float] = None
    live_score: Optional[float] = None
    final_score: Optional[float] = None
    tier: Optional[Tier] = None
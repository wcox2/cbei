# College Basketball Entertainment Index (CBEI)

A web application that scores every Division I men's college basketball game
on a 1–100 entertainment scale using pure on-court signals — closeness, pace,
scoring volume, and team hype.

## What It Does

- Computes a daily entertainment score for every D1 men's basketball game
- Displays games in a public-facing dashboard sorted by entertainment value
- Updates scores every 15 minutes during live games
- Shows predicted scores before tip-off based on team rankings and KenPom ratings

## Entertainment Factors

| Factor | Weight | Description |
|---|---|---|
| Closeness (end-weighted) | 35% | Final stretch margin weighted most heavily |
| Lead Changes | 25% | Late-game lead changes weighted 3x |
| Scoring Volume & Pace | 20% | Made field goals + possessions per game |
| Hype (Rankings + KenPom) | 15% | AP poll tiers + KenPom quality gap |
| Overtime Bonus | 5% | Flat bonus per OT period |

## Score Tiers

| Tier | Range | Label |
|---|---|---|
| 4 | 85–100 | Elite Game |
| 3 | 65–84 | Good Watch |
| 2 | 40–64 | Average |
| 1 | 0–39 | Skip |

## Project Structure
```
cbei/
  backend/
    src/          # Python scoring engine and data pipeline
    tests/        # Unit tests mirroring src structure
  frontend/       # React application (Phase 4)
  docs/           # Spec documents and architecture decisions
  README.md
```

## Tech Stack

- **Scoring Engine:** Python
- **Backend:** Firebase Cloud Functions
- **Database:** Firebase Firestore
- **Frontend:** React
- **Data Sources:** ESPN Unofficial API, KenPom (weekly CSV)

## Development Phases

- [x] Phase 0 — Project skeleton
- [ ] Phase 1 — Scoring engine (Python)
- [ ] Phase 2 — Data ingestion (ESPN API)
- [ ] Phase 3 — Firebase backend
- [ ] Phase 4 — React frontend
- [ ] Phase 5 — Polish and calibration
- [ ] Phase 6 — Auth and user preferences

## Setup

_Instructions will be added as each phase is completed._
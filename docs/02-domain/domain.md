# Domain

## Purpose

This document defines the core domain concepts and rules of Data-Futbol.

The domain is focused on historical analysis of official football matches. The system uses match data, competition context, team performance, cards, results, and bookmaker odds to produce statistical analysis and decision-support insights.

The MVP does not provide AI-based match predictions.

## Core Domain Concepts

### Team
A football team participating in official competitions and matches. A team can participate in many matches and can appear as either the home or away team.

### Competition
An official football competition in which matches are played. Examples include domestic leagues, domestic cups, continental competitions, official international competitions, official playoffs, and official super cups.

Friendly, preseason, exhibition, and other non-official competitions are excluded.

### Season
A competition period that groups matches belonging to the same competition season.

### Match
The central domain entity. A match connects competition, season, date, home team, away team, score, cards, match status, extra-time information, penalty-shootout information, and betting odds when available.

## Match Eligibility

A match is eligible when it is official, actually played, and not cancelled, abandoned, annulled, or otherwise invalid.

A postponed match does not count until it is actually played.

## Official Matches Only

Friendly matches, preseason matches, exhibition matches, and other non-official fixtures are excluded from recent form, goals, results, cards, standings-related analysis, H2H, market analysis, and insight generation.

"All Competitions" means all available official competitions.

## Match Result and Match Duration

The domain distinguishes the result after regular time from the final outcome.

### Regular Time

Regular time is the initial 90 minutes including normal stoppage time. The MVP statistical result is based on the score at the end of regular time.

### Extra Time

Extra-time information is stored separately. If a match is level after regular time, its statistical result remains a draw even if a team wins during extra time.

Example:
- Regular time: 1-1
- Final after extra time: 2-1
- Statistical result: Draw

### Penalty Shootout

Penalty shootouts are stored separately. Penalty-kick goals do not count as match goals.

Example:
- Regular time: 1-1
- Extra time: 2-2
- Penalties: 4-3
- Statistical result: Draw

The domain preserves regular-time score, final score after extra time, and penalty-shootout result.

## Recent Match Analysis

The system supports the last N eligible official matches of a team. N is configurable, with 10 as the primary use case.

Supported scopes:
- All official competitions
- A specific competition
- Overall
- Home
- Away

The selected scope must be explicit in an analysis result.

## Head-to-Head

H2H is an independent statistical context representing previous official matches between two teams.

It may include wins, draws, losses, goals, yellow cards, red cards, total cards, which team received more cards, competition, home/away context, and date.

H2H must not be silently merged into recent-form statistics.

## Team Performance

Performance may include wins, draws, losses, goals scored, goals conceded, average goals scored/conceded, clean sheets, matches conceding goals, yellow cards, red cards, and total cards.

Performance can be segmented by overall, home, away, competition, and recent N matches.

## League Position

When standings are available, the system may include position, matches played, wins, draws, losses, goals for, goals against, goal difference, and points.

Historical standings must retain competition and temporal context.

## Betting Markets

### 1X2
- Home
- Draw
- Away

### Double Chance
- 1X
- X2
- 12

### Goals Over/Under
Whether total match goals are above or below a specified line. Specific lines depend on source availability.

### Most Cards
Which team receives more cards:
- Home
- Draw
- Away

### Cards Over/Under
Whether total match cards are above or below a specified line. Specific lines depend on source availability.

### Post-MVP: Both Teams To Score
- Yes
- No

BTTS is outside the initial MVP.

## Odds

The primary odds target for the MVP is opening odds. An odds record may contain match, market, selection, bookmaker, and opening odds.

Closing odds are outside the initial MVP.

The exact source, bookmaker coverage, and market availability will be defined during Data Definition.

## Statistics, Insights, and Decisions

### Raw Data
Recorded facts such as result, goals, cards, and odds.

### Statistics
Values calculated from raw data, such as win rate or average goals.

### Insights
Interpretations derived from statistical evidence.

### Decision Support
Comparison of statistical evidence with other information, such as implied probability from bookmaker odds.

The system supports decisions rather than automatically making betting decisions.

## Domain Boundaries

The MVP does not include:
- Live match data
- Live odds
- AI-based predictions
- Automatic betting
- Real-time recommendations
- Friendly-match statistics

Future probabilistic or machine-learning models may be considered separately.

## Core Domain Relationship

```text
Competition
     │
     └── Season
           │
           └── Match
                ├── Home Team
                ├── Away Team
                ├── Result
                ├── Goals
                ├── Cards
                ├── Extra Time
                ├── Penalty Shootout
                └── Odds
```

## Domain Principles

1. Official competitive matches are the only valid source for MVP statistics.
2. Invalid, cancelled, abandoned, or annulled matches do not enter statistical samples.
3. Extra time and penalty shootouts are preserved as additional match context.
4. The statistical result is based on the score at the end of regular time.
5. Penalty-shootout goals are not match goals.
6. Recent form and H2H are independent analytical contexts.
7. Competition scope must be explicit.
8. The number of recent matches must be configurable.
9. Raw data, statistics, insights, and decisions are separate concepts.
10. Market lines and data availability must be validated against real historical sources before implementation.

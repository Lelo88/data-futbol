
This design enables seamless provider switching and multi-provider support without restructuring the core domain model.

## Entity Attributes Quick Reference

### Provider
- provider_id (PK)
- name (UNIQUE)
- base_url
- description

### Competition
- competition_id (PK)
- name
- type (ENUM)
- country_code

### Season
- season_id (PK)
- competition_id (FK)
- season_year
- display_name

### Team
- team_id (PK)
- name (UNIQUE)
- short_name

### Match
- match_id (PK)
- competition_id (FK)
- season_id (FK)
- home_team_id (FK)
- away_team_id (FK)
- match_date
- match_status
- home_goals, away_goals
- home_goals_et, away_goals_et (nullable)
- extra_time_played
- penalty_shootout_played
- home_penalties, away_penalties (nullable)

### MatchEvent
- event_id (PK)
- match_id (FK)
- event_type
- team_id (FK)
- player_id (FK, nullable)
- minute
- extra_time_minute

### Standing
- standing_id (PK)
- competition_id (FK)
- season_id (FK)
- team_id (FK)
- position
- played, wins, draws, losses
- goals_for, goals_against, goal_difference
- points
- source (provider/derived)
- snapshot_date (nullable)

### Bookmaker
- bookmaker_id (PK)
- name (UNIQUE)

### Market
- market_id (PK)
- code (UNIQUE)
- name
- description

### Selection
- selection_id (PK)
- market_id (FK)
- code
- name
- line_value (nullable)

### OddsObservation
- observation_id (PK)
- provider_id (FK) ← **CRITICAL: Explicitly tracks source**
- match_id (FK)
- bookmaker_id (FK)
- market_id (FK)
- selection_id (FK)
- odds_value
- odds_type (opening/closing/snapshot)
- observation_timestamp

### ProviderMapping
- mapping_id (PK)
- provider_id (FK)
- entity_type
- internal_id
- external_id
- external_url (nullable)

---

## Design Notes

1. **Provider Agnostic:** The ProviderMapping table separates internal IDs from external provider IDs, allowing the system to switch providers or use multiple providers without restructuring core entities.

2. **Temporal Odds:** OddsObservation stores multiple observations with timestamps, supporting opening, closing, and snapshot odds without requiring separate columns.

3. **H2H Derived:** Head-to-head data is derived from Match queries, not persisted, avoiding redundancy.

4. **Regular Time Focus:** Match stores regular-time goals as the statistical result; extra-time and penalties are stored separately.

5. **Flexible Events:** MatchEvent uses event_type discriminator for extensibility (goals, cards, substitutions, etc.).

6. **Standings Context:** Standing tracks league position with source metadata (provider or derived) and optional snapshot_date for historical tracking.
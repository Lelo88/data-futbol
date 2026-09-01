# Data Model

## 1. Purpose

This document defines the conceptual and logical data model for Data-Futbol's PostgreSQL database.

The data model translates the project's domain concepts and data requirements into a normalized relational structure capable of supporting historical football statistics, standings analysis, head-to-head computation, and historical betting odds analysis.

It serves as the blueprint for the Implementation phase, which will create PostgreSQL migrations and establish database constraints.

## 2. Scope

The data model covers:

- **Entities:** Competition, Season, Team, Match, MatchEvent, Standing, Bookmaker, Market, Selection, OddsObservation, Provider, ProviderMapping.
- **MVP Competitions:** Premier League, La Liga, Bundesliga, Serie A, UEFA Champions League.
- **MVP Markets:** 1X2, Double Chance, Goals Over/Under, Most Cards, Cards Over/Under.
- **MVP Match Events:** Goals, Yellow Cards, Red Cards.
- **Historical Odds:** Mandatory MVP requirement.
- **Opening and Closing Odds:** Optional / desirable when reliably provided by the source.
- **Derived Outputs:** H2H, Recent Form, Standings aggregates (where applicable).

The model does NOT cover AI predictions, real-time ingestion, player-level analytics beyond match events, BTTS (post-MVP), streaming architectures, or multi-user access control.

## 3. Design Principles

### 3.1 Internal IDs vs. Provider IDs

Core domain entities use stable internal identifiers (team_id, competition_id, match_id) that are decoupled from provider-specific external identifiers.

Provider-specific identifiers are stored separately in ProviderMapping tables:

```
Internal Entity (e.g., Team with team_id=1)
    ↓
ProviderMapping (records external IDs)
    ├─ provider_id: 1 (TheStatsAPI)
    ├─ external_id: "33"
    └─ AND separately:
    ├─ provider_id: 2 (UK Odds API)
    └─ external_id: "MAN_UTD"
```

This strategy allows seamless provider switching and multi-provider support without restructuring core domain entities.

### 3.2 Normalization for Consistency

The model follows Third Normal Form (3NF) normalization to:

- eliminate redundant storage (e.g., bookmaker name stored once, not repeated in each odds observation);
- preserve referential integrity through foreign keys;
- reduce update anomalies (a bookmaker name change updates one row, not thousands).

Normalization is applied judiciously; denormalization (e.g., caching goal_difference on Standing) is acceptable where it improves query performance without violating domain consistency.

### 3.3 Temporal Context and Multiple Observations

Entities like OddsObservation explicitly track timestamps to support:

- historical odds series for the same match/bookmaker/market/selection;
- distinct opening, closing, and intermediate snapshot observations;
- time-series analysis without requiring separate "opening_odds_value" and "closing_odds_value" columns.

### 3.4 Separation of Concerns

Statistics and derived data (wins, losses, recent form, H2H) are computed from base entities (Match, MatchEvent, OddsObservation) at query time rather than stored redundantly.

This keeps the data model simple and ensures a single source of truth.

### 3.5 Provider Flexibility

The model is provider-agnostic. Adding a new provider requires only:

1. Registering it in the Provider table.
2. Populating ProviderMapping records for its entities.
3. No structural changes to core entities.

## 4. Core Entities

### 4.1 Provider

Represents a data source from which external data originates.

**Attributes:**
- `provider_id` (PK): Stable internal identifier.
- `name` (UNIQUE): Provider name (e.g., "TheStatsAPI", "UK Odds API").
- `base_url` (nullable): Base URL or endpoint prefix.
- `description` (nullable): Purpose and scope of this provider.
- `created_at`, `updated_at`: Audit timestamps.

**Purpose:** Allows tracking which provider supplied each piece of data and supports future provider additions.

### 4.2 Competition

Represents an official football competition.

**Attributes:**
- `competition_id` (PK): Stable internal identifier.
- `name`: Competition name (e.g., "Premier League").
- `type` (ENUM): Competition category (domestic_league, domestic_cup, continental, international, other).
- `country_code` (nullable): ISO 3166-1 alpha-2 country code when applicable.
- `created_at`, `updated_at`: Audit timestamps.

**Constraint:** `(name, type, country_code)` should be unique to prevent duplicates.

**Purpose:** Static reference entity that groups seasons and provides competition context for matches.

### 4.3 Season

Represents a season within a competition.

**Attributes:**
- `season_id` (PK): Stable internal identifier.
- `competition_id` (FK): References Competition (required).
- `season_year` (Integer): Starting year of the season (e.g., 2025 for 2025/26 season).
- `display_name` (nullable): Human-readable season label.
- `created_at`, `updated_at`: Audit timestamps.

**Constraint:** `(competition_id, season_year)` should be unique.

**Purpose:** Allows normalizing season identity across providers using a consistent year reference, enabling matches from different providers (with different season label formats) to be properly grouped.

### 4.4 Team

Represents a football team.

**Attributes:**
- `team_id` (PK): Stable internal identifier.
- `name` (UNIQUE): Team's canonical name.
- `short_name` (nullable): Abbreviated name or code.
- `created_at`, `updated_at`: Audit timestamps.

**Purpose:** Reference entity; provider-specific team identifiers are stored in ProviderMapping.

### 4.5 Match

The central domain entity representing a single official football match.

**Attributes:**
- `match_id` (PK): Stable internal identifier.
- `competition_id` (FK): References Competition (required).
- `season_id` (FK): References Season (required).
- `home_team_id` (FK): References Team for home side (required; must differ from away_team_id).
- `away_team_id` (FK): References Team for away side (required; must differ from home_team_id).
- `match_date` (Timestamp): Kickoff date and time in UTC.
- `match_status` (ENUM): Status code (scheduled, in_progress, completed, postponed, cancelled, abandoned).
- `home_goals` (Integer >= 0): Goals scored by home team at end of regular time.
- `away_goals` (Integer >= 0): Goals scored by away team at end of regular time.
- `home_goals_et` (nullable, Integer >= 0): Home goals at end of extra time (if applicable).
- `away_goals_et` (nullable, Integer >= 0): Away goals at end of extra time (if applicable).
- `extra_time_played` (Boolean): Whether extra time was played.
- `penalty_shootout_played` (Boolean): Whether a penalty shootout occurred.
- `home_penalties` (nullable, Integer >= 0): Home team penalty shootout score.
- `away_penalties` (nullable, Integer >= 0): Away team penalty shootout score.
- `created_at`, `updated_at`: Audit timestamps.

**Critical Design Decision (Regular Time as Statistical Result):**

Regular-time goals (home_goals, away_goals) represent the MVP statistical result. A match ending 1-1 after regular time is a draw for statistics, even if a team wins after extra time or penalties. Extra-time and penalty information are stored separately to preserve both the statistical result and the full match context.

**Constraints:**
- home_team_id ≠ away_team_id (a team cannot play itself)
- home_goals >= 0, away_goals >= 0
- If extra_time_played = true: home_goals_et and away_goals_et must not be NULL
- If penalty_shootout_played = true: home_penalties and away_penalties must not be NULL

**Purpose:** Central entity from which most other data flows; enables all match-based analysis (H2H, recent form, standings derivation).

### 4.6 MatchEvent

Represents a discrete event within a match (goals, cards, potentially substitutions or VAR reviews).

**Attributes:**
- `event_id` (PK): Stable internal identifier.
- `match_id` (FK): References Match (required).
- `event_type` (ENUM): goal, yellow_card, red_card, substitution, other.
- `team_id` (FK): References Team; must be home or away team of the match.
- `player_id` (FK, nullable): References Player (if player data is reliably available; otherwise NULL).
- `minute` (Integer, nullable >= 0): Event minute in the match.
- `extra_time_minute` (Boolean, nullable): Indicates whether minute is in extra time.
- `created_at`, `updated_at`: Audit timestamps.

**Constraints:**
- team_id must be home_team_id OR away_team_id of the referenced match

**Design Decision (Generic Event Model):**

Using a single event_type discriminator allows future event types (substitutions, VAR reviews) without schema redesign. This is preferable to separate Goal, YellowCard, RedCard tables, which would require joins for every event query.

**Design Decision (Player ID Optional):**

player_id is nullable because external providers may not consistently provide player-level identifiers for all competitions and matches, especially for MVP-stage providers. Player tracking can be added later if data availability improves.

**Purpose:** Captures match-level granular data; enables card aggregation and goal tracking independent of match-level goal fields.

### 4.7 Standing

Represents league position and related statistics for a team within a competition-season context.

**Attributes:**
- `standing_id` (PK): Stable internal identifier.
- `competition_id` (FK): References Competition (required).
- `season_id` (FK): References Season (required).
- `team_id` (FK): References Team (required).
- `position` (Integer > 0): Position in the table.
- `played` (Integer >= 0): Number of matches played.
- `wins` (Integer >= 0): Number of matches won.
- `draws` (Integer >= 0): Number of matches drawn.
- `losses` (Integer >= 0): Number of matches lost.
- `goals_for` (Integer >= 0): Total goals scored.
- `goals_against` (Integer >= 0): Total goals conceded.
- `goal_difference` (Integer, derived): goals_for - goals_against (stored for query efficiency).
- `points` (Integer >= 0): Total points in the competition.
- `source` (Text): "provider" (directly from source) or "derived" (computed from match results).
- `snapshot_date` (Timestamp, nullable): Point-in-time snapshot date (if tracking historical standings; otherwise NULL for current standings only).
- `created_at`, `updated_at`: Audit timestamps.

**Design Decision (Current vs. Historical Standings):**

The MVP persists current standings supplied by providers. The optional `snapshot_date` field allows persisting historical standings if the project later requires tracking league table changes over time. For the MVP, `snapshot_date` should remain NULL, and only current standings are retained. If historical standings prove necessary, `snapshot_date` can be populated without schema changes.

**Rationale for Persistence:**

Standing information from providers represents the official league table at a specific time. While standings can be derived from match results, provider-supplied standings are the canonical source of truth and should be persisted to preserve official historical context.

**Purpose:** Supports league position and context analysis; distinguishes between source-provided and derived standings.

### 4.8 Bookmaker

Represents a betting bookmaker.

**Attributes:**
- `bookmaker_id` (PK): Stable internal identifier.
- `name` (UNIQUE): Bookmaker name (e.g., "Bet365", "Pinnacle").
- `created_at`, `updated_at`: Audit timestamps.

**Purpose:** Reference entity; allows odds observations to reference the same bookmaker without redundant name storage. Provider-specific bookmaker identifiers are managed via ProviderMapping.

### 4.9 Market

Represents a betting market type or category.

**Attributes:**
- `market_id` (PK): Stable internal identifier.
- `code` (UNIQUE): Machine-readable market identifier (e.g., "1X2", "DOUBLE_CHANCE", "GOALS_OVER_UNDER", "MOST_CARDS", "CARDS_OVER_UNDER").
- `name`: Human-readable market name.
- `description` (nullable): Market description.
- `created_at`, `updated_at`: Audit timestamps.

**MVP Markets (predefined):**
- 1X2 (home/draw/away)
- Double Chance (1X / X2 / 12)
- Goals Over/Under
- Most Cards
- Cards Over/Under

**Design Decision (Predefined Markets):**

MVP markets are predefined at initialization. Adding new markets is a configuration-only change; no schema redesign is required.

**Purpose:** Separates market identity from selections, avoiding redundant market name storage in Selection.

### 4.10 Selection

Represents a specific outcome or option within a betting market.

**Attributes:**
- `selection_id` (PK): Stable internal identifier.
- `market_id` (FK): References Market (required).
- `code`: Machine-readable selection identifier (e.g., "HOME", "DRAW", "AWAY" for 1X2; "OVER_2_5", "UNDER_2_5" for Goals Over/Under).
- `name`: Human-readable selection name.
- `line_value` (Decimal, nullable): Line value for line-based markets (e.g., 2.5 for Over/Under 2.5).
- `created_at`, `updated_at`: Audit timestamps.

**Constraint:** `(market_id, code)` should be unique to prevent duplicate selections within a market.

**Design Decision (Selection Structure for Line Markets):**

For line-based markets like Goals Over/Under, Selection records represent specific line combinations:
- Market: GOALS_OVER_UNDER
- Selections: (code="OVER_2_5", line_value=2.5), (code="UNDER_2_5", line_value=2.5), (code="OVER_3_5", line_value=3.5), etc.

This approach:
- Avoids storing "Over 2.5" as an indivisible string
- Supports multiple line values for the same market without structural changes
- Allows querying all selections for a specific line (e.g., all Over/Under options at 2.5)

**Purpose:** Encodes the available options within a market; separates market category from specific outcomes.

### 4.11 OddsObservation

Represents a single historical odds observation. This is a critical MVP entity supporting historical betting analysis.

**Attributes:**
- `observation_id` (PK): Stable internal identifier.
- `provider_id` (FK): References Provider (required). Explicitly captures the source of this observation.
- `match_id` (FK): References Match (required).
- `bookmaker_id` (FK): References Bookmaker (required).
- `market_id` (FK): References Market (required).
- `selection_id` (FK): References Selection (required).
- `odds_value` (Decimal > 0): The decimal odds at the time of observation.
- `odds_type` (ENUM): Type of odds: "opening", "closing", "snapshot".
- `observation_timestamp` (Timestamp): When the odds were observed/captured (required).
- `created_at`, `updated_at`: Audit timestamps.

**Design Decision (provider_id in OddsObservation):**

OddsObservation includes provider_id to explicitly capture provenance. While ProviderMapping also tracks provider relationships, including provider_id directly in OddsObservation ensures that:
- The origin of an odds observation is never ambiguous
- Queries for odds from a specific provider do not require joining ProviderMapping
- The data model reflects the fact that OddsObservation is inherently provider-supplied

**Design Decision (Multiple Observations Over Time):**

The model expects multiple OddsObservation records for the same match/bookmaker/market/selection combination, each with a different observation_timestamp. This enables:
- Historical odds series analysis
- Opening, intermediate, and closing odds capture
- Time-series modeling of odds movements

**Design Decision (Opening/Closing Odds Semantics):**

Per Provider Selection (Section 2.1), Opening Odds and Closing Odds are OPTIONAL, not mandatory:

- **Historical Odds:** MANDATORY. Every odds observation includes match, bookmaker, market, selection, odds_value, and timestamp.
- **Opening Odds:** OPTIONAL / DESIRABLE. Stored only when the provider explicitly identifies and labels an odds value as "opening" or when a future project rule defines a valid derivation method. Represented as `odds_type = "opening"`.
- **Closing Odds:** OPTIONAL / DESIRABLE. Stored only when explicitly identified by the provider. Represented as `odds_type = "closing"`.
- **Intermediate Snapshots:** SUPPORTED. Historical capture timestamps are preserved as `odds_type = "snapshot"`.

**Critical Rule (NO AUTOMATIC INFERENCE):**

The first captured odds snapshot is NOT automatically treated as an Opening Odds unless the provider documentation explicitly states that behavior. Silently inferring opening prices violates the Provider Selection decision and introduces analysis errors.

**Constraints:**
- odds_value > 0
- odds_type IN ("opening", "closing", "snapshot")
- observation_timestamp must be a valid timestamp

**Purpose:** Enables historical odds analysis, bookmaker comparison, market movement tracking, and decision-support insights.

### 4.12 ProviderMapping

Represents the association between internal domain entities and their provider-specific external identifiers.

**Attributes:**
- `mapping_id` (PK): Stable internal identifier.
- `provider_id` (FK): References Provider (required).
- `entity_type` (ENUM): Type of entity being mapped (competition, season, team, match, bookmaker, market, selection).
- `internal_id` (Text or UUID): The internal ID of the entity (e.g., team_id=1, competition_id=42).
- `external_id` (Text): The provider-specific external identifier (e.g., "33", "MAN_UTD", "39").
- `external_url` (nullable): URL or reference within the provider's system.
- `created_at`, `updated_at`: Audit timestamps.

**Constraints (Logical):**

The model must enforce:

1. **Uniqueness by Provider/Entity/Internal:** `UNIQUE(provider_id, entity_type, internal_id)` — Each internal entity has at most one external ID per provider/entity-type combination.
2. **Uniqueness by Provider/Entity/External:** `UNIQUE(provider_id, entity_type, external_id)` — Each external ID is assigned to at most one internal entity per provider/entity-type combination.

These constraints prevent:
- The same internal entity from having conflicting mappings for the same provider
- The same external ID from being assigned to multiple internal entities (which would cause reconciliation ambiguity)

**Design Decision (Generic ProviderMapping vs. Separate Tables):**

The model uses a single generic ProviderMapping table with entity_type discriminator rather than separate mapping tables for each entity type (e.g., CompetitionMapping, TeamMapping, MatchMapping).

**Trade-off: Flexibility vs. Relational Enforcement**

*Advantages:*
- Single schema for all provider mappings; no duplication
- Supports adding new entity types without schema changes
- Unified query interface for all mappings
- Simpler to scale to many providers

*Disadvantages:*
- Cannot use conventional foreign keys from internal_id to specific domain tables (FK enforcement depends on entity_type)
- Application/domain boundary must validate entity_type/internal_id consistency
- Database cannot prevent orphaned internal_ids (e.g., a standing_id with entity_type="team")

*Mitigation:*
- Application layer validates that entity_type and internal_id refer to valid entities before inserting/updating
- Tests validate entity_type/internal_id consistency
- Uniqueness constraints prevent duplicate or conflicting mappings

**Purpose:** Decouples internal identities from provider identities; enables seamless provider switching and multi-provider support.

## 5. Relationships and Cardinalities

| Relationship | Cardinality | Notes |
|---|---|---|
| Provider → ProviderMapping | 1:N | One provider has many mappings |
| Competition → Season | 1:N | One competition spans many seasons |
| Season → Match | 1:N | One season contains many matches |
| Competition → Match | 1:N | Matches belong to a competition (via Season) |
| Team → Match (home) | 1:N | A team plays as home in many matches |
| Team → Match (away) | 1:N | A team plays as away in many matches |
| Match → MatchEvent | 1:N | One match has many events (goals, cards) |
| Competition → Standing | 1:N | Standings are recorded per competition |
| Season → Standing | 1:N | Standings are recorded per season |
| Team → Standing | 1:N | A team has one or more standing records |
| Bookmaker → OddsObservation | 1:N | One bookmaker has many observations |
| Market → Selection | 1:N | One market has many selections |
| Selection → OddsObservation | 1:N | A selection has many observations |
| Match → OddsObservation | 1:N | One match has many odds observations |
| Provider → OddsObservation | 1:N | One provider supplies many observations |

## 6. Provider Mapping Strategy

### 6.1 Design

Provider mappings use a single `ProviderMapping` table with `entity_type` discriminator. When ingesting data from a provider:

1. Check if an internal entity exists (by name for Competition/Team, by match properties for Match, etc.).
2. Check `ProviderMapping` for `(provider_id, entity_type, internal_id)`.
3. If mapping exists, verify external_id matches; update if inconsistency detected.
4. If no mapping exists, insert it.
5. If internal entity doesn't exist, create it and insert mapping.

### 6.2 Entities Requiring Mappings

- **Competition:** Different providers use different competition codes (e.g., "39" vs. "PL").
- **Team:** Providers assign different IDs (e.g., "33" vs. "MAN_UTD").
- **Match:** Different match ID schemes across providers.
- **Bookmaker:** Provider-specific bookmaker codes may differ.
- **Market:** Market codes may have provider variations.
- **Selection:** Selection codes may differ.

### 6.3 Example

Manchester United (internal team_id = 1):
- TheStatsAPI → external_id = "33"
- UK Odds API → external_id = "MAN_UTD"

Each mapping is a separate ProviderMapping record:
```
provider_id=1, entity_type="team", internal_id="1", external_id="33"
provider_id=2, entity_type="team", internal_id="1", external_id="MAN_UTD"
```

## 7. Odds Model

### 7.1 Conceptual Flow

```
Match (match_id=1, Premier League, Man United vs Liverpool, 2025-08-30)
  ↓
OddsObservation
  ├── provider_id (source)
  ├── bookmaker_id (e.g., Bet365)
  ├── market_id (e.g., 1X2)
  ├── selection_id (e.g., HOME)
  ├── odds_value (e.g., 1.50)
  ├── odds_type (opening, closing, or snapshot)
  └── observation_timestamp
```

### 7.2 Key Features

- **Multiple bookmakers:** A single match can have odds from Bet365, Pinnacle, Betfair, etc. Each observation is a separate row.
- **Multiple observations over time:** The same bookmaker/market/selection can have many observations representing odds changes.
- **Temporal semantics:** `odds_type` preserves the provider's semantics about when odds were captured.
- **Optional Opening/Closing:** Opening and Closing odds are stored when the provider explicitly identifies them. They are never inferred from first/last snapshot.

### 7.3 Opening and Closing Odds (MANDATORY VS. OPTIONAL)

**Provider Decision (from Provider Selection):**

- **TheStatsAPI:** Explicitly documents opening and last-seen prices where captured. Availability is not guaranteed for every match or market.
- **UK Odds API:** Provides historical snapshots with timestamps but does NOT explicitly define opening prices. The first snapshot is NOT automatically an opening price.

**Data Model Response:**

- `odds_type = "opening"` only when the provider explicitly labels an observation as opening.
- `odds_type = "closing"` only when the provider explicitly labels an observation as closing.
- `odds_type = "snapshot"` for historical captures without explicit opening/closing semantics.

**CRITICAL RULE:**

Do NOT automatically treat the first odds snapshot as an opening price. This violates the Provider Selection decision and introduces analysis errors.

### 7.4 Querying Odds

Examples of queries supported:

```sql
-- Opening odds for a match (where provider explicitly labeled opening)
SELECT o.odds_value, b.name, m.code, s.name
FROM OddsObservation o
JOIN Bookmaker b ON o.bookmaker_id = b.bookmaker_id
JOIN Market m ON o.market_id = m.market_id
JOIN Selection s ON o.selection_id = s.selection_id
WHERE o.match_id = 1 AND o.odds_type = 'opening'
ORDER BY b.name, m.code, s.name;

-- Historical odds timeline for a specific match/bookmaker/market/selection
SELECT observation_timestamp, odds_value, odds_type
FROM OddsObservation
WHERE match_id = 1 AND bookmaker_id = 1 AND market_id = 1 AND selection_id = 1
ORDER BY observation_timestamp;

-- Latest odds for all markets on a match
SELECT DISTINCT ON (bookmaker_id, market_id, selection_id)
  bookmaker_id, market_id, selection_id, odds_value, observation_timestamp
FROM OddsObservation
WHERE match_id = 1
ORDER BY bookmaker_id, market_id, selection_id, observation_timestamp DESC;
```

## 8. H2H Strategy

### 8.1 Decision: Derived, Not Persisted

Head-to-Head data is **derived** from the Match table at query time, not persisted as a separate H2H entity.

**Rationale:**

- All H2H information exists in Match: home_team_id, away_team_id, competition_id, season_id, match_date, goals, cards.
- Storing H2H separately introduces redundancy and update anomalies (if a match is updated, H2H records must also be updated).
- H2H contexts (same competition, all competitions, date windows) are query-time concerns, not storage concerns.

### 8.2 H2H Derivation Examples

```sql
-- Same-competition H2H between Team A (team_id=1) and Team B (team_id=2)
SELECT * FROM Match
WHERE competition_id = 1
  AND ((home_team_id = 1 AND away_team_id = 2)
    OR (home_team_id = 2 AND away_team_id = 1))
ORDER BY match_date DESC;

-- All-competition H2H
SELECT * FROM Match
WHERE ((home_team_id = 1 AND away_team_id = 2)
    OR (home_team_id = 2 AND away_team_id = 1))
ORDER BY match_date DESC;

-- Recent 10-match H2H window
SELECT * FROM Match
WHERE ((home_team_id = 1 AND away_team_id = 2)
    OR (home_team_id = 2 AND away_team_id = 1))
ORDER BY match_date DESC
LIMIT 10;
```

H2H statistics (wins, draws, losses, goals, cards) are computed in the application layer from query results.

## 9. Constraints

### 9.1 Check Constraints (Logical)

```sql
-- Match constraints
CHECK (home_team_id != away_team_id)  -- A team cannot play itself
CHECK (home_goals >= 0 AND away_goals >= 0)  -- Goals are non-negative
CHECK (match_status IN ('scheduled', 'in_progress', 'completed', 'postponed', 'cancelled', 'abandoned'))

-- MatchEvent constraints
CHECK (event_type IN ('goal', 'yellow_card', 'red_card', 'substitution', 'other'))

-- OddsObservation constraints
CHECK (odds_value > 0)  -- Odds must be positive
CHECK (odds_type IN ('opening', 'closing', 'snapshot'))

-- Standing constraints
CHECK (position > 0)  -- Position is 1-indexed
CHECK (played >= 0 AND wins >= 0 AND draws >= 0 AND losses >= 0 AND points >= 0)
```

### 9.2 Referential Integrity

All foreign keys must enforce referential integrity:
- Competition.competition_id must exist when referenced
- Team.team_id must exist when referenced
- All FK references maintain valid relationships

### 9.3 Uniqueness Constraints (Logical)

- Provider.name (unique)
- Competition: (name, type, country_code) unique
- Season: (competition_id, season_year) unique
- Team.name (unique)
- Bookmaker.name (unique)
- Market.code (unique)
- Selection: (market_id, code) unique
- ProviderMapping: (provider_id, entity_type, internal_id) unique
- ProviderMapping: (provider_id, entity_type, external_id) unique

## 10. Indexing Considerations

Indexes should support common query patterns. These are conceptual recommendations for the Implementation phase:

| Query Pattern | Recommended Index | Rationale |
|---|---|---|
| Recent form (matches by team) | (home_team_id, match_date DESC), (away_team_id, match_date DESC) | Efficient recent-form queries |
| H2H lookups | (home_team_id, away_team_id, match_date DESC) | Efficient H2H joins |
| Matches by competition/season | (competition_id, season_id, match_date) | League and season filtering |
| Odds by match | (match_id, bookmaker_id, market_id) | Retrieve all odds for a match |
| Odds by timestamp | (observation_timestamp) | Time-range odds queries |
| Provider mappings | (provider_id, entity_type, external_id) | Reverse lookups (external ID → internal) |
| Standings by season | (competition_id, season_id, team_id) | League table queries |

Specific index creation and tuning decisions are deferred to the Implementation phase and performance analysis.

## 11. Decisions and Trade-Offs

### 11.1 Match Score: Direct Fields vs. Separate Score Entity

**Decision:** home_goals and away_goals stored directly on Match.

**Rationale:** Scores are fundamental match information. Keeping them on Match avoids unnecessary joins and aligns with the domain's Match-centric design.

### 11.2 Match Events: Single Generic Table vs. Specialized Tables

**Decision:** Single MatchEvent table with event_type discriminator.

**Rationale:** Supports future event types (substitutions, VAR reviews, etc.) without schema redesign. Flexible and queryable.

### 11.3 Standing Snapshots: Optional Persistence

**Decision:** MVP persists current standings; optional snapshot_date for future historical tracking.

**Rationale:** MVP captures current standings supplied by providers. Historical standings can be added later without schema changes.

### 11.4 H2H: Derived Not Persisted

**Decision:** H2H is derived from Match at query time, not persisted.

**Rationale:** Single source of truth, no redundancy, eliminates update anomalies. Materialized views can be added later if performance requires.

### 11.5 Opening Odds: Explicit Only, Never Inferred

**Decision:** Opening odds stored only when provider explicitly identifies them; first snapshot is NOT automatically opening.

**Rationale:** Respects Provider Selection decision. Opening odds are optional, not mandatory. Silently inferring would introduce analysis errors.

### 11.6 Provider Mapping: Generic Table with Entity Type Discriminator

**Decision:** Single ProviderMapping table with entity_type instead of separate mapping tables per entity.

**Trade-off Analysis:**

*Advantages:*
- Single schema; no redundancy
- Scalable to many entity types and providers
- Supports adding new entity types without schema changes
- Unified query interface

*Disadvantages:*
- Cannot use conventional foreign keys based on entity_type
- Application must validate entity_type/internal_id consistency
- Database cannot prevent orphaned internal_ids

*Mitigation:*
- Application-layer validation and testing ensure consistency
- Uniqueness constraints prevent duplicate or conflicting mappings
- Documented design decision serves as contract for future work

### 11.7 OddsObservation: Includes Provider ID

**Decision:** OddsObservation includes provider_id as a foreign key.

**Rationale:** Ensures provenance is never ambiguous; enables provider-specific odds queries without joining ProviderMapping; reflects that OddsObservation is inherently provider-supplied data.

## 12. Out of Scope

The following are explicitly NOT part of the Data Model:

- **AI predictions** (future Insights Engine)
- **Real-time odds or live data** (MVP is historical only)
- **Player-level analytics beyond match events** (can be added if provider data improves)
- **BTTS market implementation** (postponed to post-MVP)
- **Streaming or event-sourcing architecture** (traditional relational model)
- **Multi-user access control or authentication** (future concerns)
- **Caching strategy** (database-agnostic)

## 13. Open Questions

Explicit unresolved questions for the Implementation phase:

1. **Player ID persistence:** Should player_id on MatchEvent be persisted for all providers, or only when available? *(Recommendation: nullable, persist when available)*

2. **Historical odds depth (UK Odds API):** How many seasons of historical odds are available per MVP competition? *(Requires provider verification)*

3. **Standing snapshots:** Should snapshot_date be populated for all sources to track historical league positions over time? *(Recommendation: MVP captures current standings only; historical snapshots optional post-MVP)*

4. **Market normalization:** How should provider-specific market codes (1X2 vs. 1x2 vs. WIN_DRAW_LOSS) be normalized to canonical codes? *(Recommendation: ingestion layer normalizes to canonical codes; ProviderMapping tracks external codes)*

5. **Selection line precision:** Should line values use Decimal(5,1), Decimal(5,2), or Float? *(Recommendation: Decimal for financial precision)*

6. **Timezone handling:** Should match_date include timezone info or be stored UTC-only? *(Recommendation: store UTC; derive timezone from Competition.country_code if needed)*

7. **Provider Terms verification:** Legal review of TheStatsAPI and UK Odds API commercial terms required before production deployment. *(Documented in Provider Selection; must be completed pre-implementation)*

## 14. MVP Markets Verification

The model must support all MVP markets without structural changes:

- **1X2:** Market with 3 selections (HOME, DRAW, AWAY) ✓
- **Double Chance:** Market with 3 selections (1X, X2, 12) ✓
- **Goals Over/Under:** Market with selections at various lines (Over 2.5, Under 2.5, Over 3.5, etc.) ✓
- **Most Cards:** Market with selections (Home, Away, Draw/Tie) ✓
- **Cards Over/Under:** Market with selections at various lines ✓

**BTTS (Post-MVP):** Model supports BTTS without schema changes but treats it as secondary/post-MVP per Provider Selection.

## 15. Implementation Readiness Checklist

- ✅ All mandatory MVP concepts represented (5 competitions, 5 markets, historical odds)
- ✅ Provider provenance preserved (provider_id in OddsObservation, ProviderMapping for entity IDs)
- ✅ Provider mappings logically constrained (uniqueness by provider/entity/internal and provider/entity/external)
- ✅ Standing strategy resolved (current standings persisted; historical optional via snapshot_date)
- ✅ Odds semantics resolved (opening/closing optional, never inferred; snapshots supported)
- ✅ Opening Odds correctly optional (respects Provider Selection decision)
- ✅ Closing Odds correctly optional
- ✅ H2H correctly derived (not persisted; fully derivable from Match)
- ✅ All MVP markets representable (1X2, Double Chance, Goals O/U, Most Cards, Cards O/U)
- ✅ Model consistent with Data Definition (corrected contradictions)
- ✅ Model consistent with Provider Selection (respects all decisions)
- ✅ Model consistent with Source Mapping (no unsupported capabilities assumed)
- ✅ No critical unresolved design decision remains

---

## Summary

This Data Model provides a normalized relational structure for PostgreSQL capable of supporting:

- Historical football statistics (matches, results, cards, standings)
- Head-to-head and recent-form derivation
- Bookmaker comparison and odds analysis
- Multi-provider support via decoupled provider mappings
- Future extensibility (additional markets, providers, competitions)

The model respects all decisions from Data Definition, Provider Selection, and Source Mapping phases while remaining implementation-ready for the next phase.

**STATUS: READY FOR IMPLEMENTATION**

The logical design is complete and consistent. The next phase will translate this model into PostgreSQL migrations, table definitions, and constraints.
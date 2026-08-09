# Data Definition

## 1. Purpose

This document defines the data requirements for Data-Futbol based on the current domain definition and project documentation.

It describes what data the system needs in order to support historical football statistics, statistical summaries, and decision-support analysis.

This document does not define the final data providers, the database schema, or the ingestion implementation.

The purpose of this document is to separate data requirements from source selection so that different providers can be evaluated independently for different parts of the domain.

## 2. Data Principles

The data layer must follow the principles below.

- Historical data only.
- No real-time ingestion.
- Official matches only.
- Friendly matches are excluded.
- Data must preserve source provenance.
- Different providers may be used for different purposes.
- Raw external data must be distinguishable from normalized internal data.
- Source selection must not dictate the domain model.
- Data quality and consistency must be validated before data is used for statistics.

These principles follow the current project vision and domain definition, which are focused on historical football analysis and decision support rather than live or predictive use cases.

## 3. Required Data Domains

The system requires the data domains below in order to support the MVP and the currently documented statistical questions.

### 3.1 Competitions

The system requires competition data that can identify the competition context of each match and standings record.

Required information:

- competition identity
- season
- competition type
- country/region when applicable

Competition data must support official competitions only.

### 3.2 Teams

The system requires team data that can identify both participants in a match and the teams referenced by recent form, H2H, standings, and market-related analysis.

Required information:

- team identity
- normalized team name
- source-specific identifiers where applicable

Team identity must remain stable across sources whenever possible, even when source-specific identifiers differ.

### 3.3 Matches

The system requires match-level data that identifies and describes each eligible official match.

Required information:

- match identity
- date
- competition
- season
- home team
- away team
- match status
- regular_time_result
- extra_time_played
- penalty_shootout_played
- penalty_shootout_winner when applicable
- goals
- extra-time information when applicable
- penalty-shootout information when applicable

Match data must support historical analysis only.

Penalty-shootout goals must not be treated as regular match goals for statistical calculations.

A match decided after extra time or penalties must retain the additional outcome information without changing the regular-time statistical result.

Matches that are not official, are not actually played, or are otherwise invalid must not enter statistical samples.

### 3.4 Match Statistics

The system requires the match statistics currently used by the domain and statistical questions.

Required statistics:

- home goals
- away goals
- yellow cards
- red cards
- total cards derived from card data

No additional match statistics are required at this stage unless they are explicitly added by the existing project documentation.

### 3.5 Standings

The system requires competition standings data to support league position analysis.

Required information:

- position
- played
- wins
- draws
- losses
- points
- goals for
- goals against
- goal difference

The system must distinguish between:

- source-provided standings
- standings derived from match results

Source-provided standings and derived standings may both be useful, but they are not interchangeable.

### 3.6 Head-to-Head Data

Head-to-head data is derived from historical matches between two teams.

The system must support:

- H2H across all eligible official competitions
- H2H filtered by competition
- H2H over a configurable historical period or match count

H2H should be derivable from match-level data and should not require a separate H2H fact table unless that becomes necessary in a later data model phase.

### 3.7 Recent Form

Recent form data is derived from the last N eligible official matches for a team.

The primary use case is:

- last 10 official matches

The system must support:

- all competitions
- a specific competition
- home-only matches
- away-only matches

Recent form must be derived from match-level data rather than stored as a duplicated statistic.

### 3.8 Betting Odds

The system requires historical odds data for the markets included in the MVP.

The MVP requires:

- 1X2
- Double Chance
- Goals Over/Under
- Most Cards
- Cards Over/Under

BTTS is post-MVP and must be explicitly treated as such.

For odds data, the conceptual requirements are:

- match
- bookmaker/source
- market
- selection
- line when applicable
- odds value
- odds type
- timestamp when available

Opening odds are the preferred odds reference for the project.

The conceptual meaning of odds type must distinguish between:

- opening odds
- closing odds
- intermediate/snapshot odds

The MVP uses opening odds only. Closing odds and intermediate/snapshot odds are not required by the MVP.

Opening odds may be provided per bookmaker or as an aggregated value. These concepts are not equivalent and must not be treated as interchangeable.

The project must not assume that every source provides opening odds with the same semantics. Exact source meaning and coverage must be established during source research.

## 4. Derived Data

Some project outputs should be derived from raw or normalized data rather than stored redundantly.

Examples of derived data include:

- total goals
- goal difference
- match result
- total cards
- win/draw/loss counts
- recent-form statistics
- H2H statistics
- implied probability from odds

The system must clearly distinguish between:

- source data
- normalized data
- derived statistics

Derived data is a product of the domain rules and statistical logic, not an independent source of truth.

## 5. Data Provenance

Externally sourced data must retain provenance.

At minimum, the conceptual model should support:

- source/provider
- source-specific identifier
- ingestion date
- original/raw representation when applicable

This requirement allows the project to compare, validate, and reconcile records from different sources without losing traceability.

## 6. Data Quality Requirements

The data layer must validate quality and consistency before data is used for statistics.

Validation must consider:

- duplicate matches
- conflicting source records
- invalid teams
- invalid competitions
- impossible scores
- inconsistent dates
- missing required values
- invalid odds
- duplicate odds
- inconsistent identifiers across providers

A data conflict must not silently overwrite another source.

## 7. Source Independence

The system must support multiple providers.

The data layer must distinguish between:

- primary source
- secondary/fallback source
- source-specific data
- normalized project data

Different providers may be used for different data domains, but provider choice must not define the domain model.

## 8. Data Availability Matrix

| Data Requirement | Required for MVP | Source Defined | Notes |
|---|---|---|---|
| Competitions | Yes | TBD | Must support competition identity, season, type, and country/region when applicable. |
| Teams | Yes | TBD | Must support normalized team names and source-specific identifiers where applicable. |
| Matches | Yes | TBD | Must support official matches only, including regular time and optional extra time and penalties. |
| Match statistics | Yes | TBD | Must support goals and cards required by the domain. |
| Standings | Yes | TBD | Must support source-provided standings and standings derived from results. |
| Head-to-head data | Yes | TBD | Must be derivable from match history and support competition filters. |
| Recent form | Yes | TBD | Must be derivable from match history and support configurable N. |
| 1X2 odds | Yes | TBD | Opening odds preferred. |
| Double Chance odds | Yes | TBD | Opening odds preferred. |
| Goals Over/Under odds | Yes | TBD | Opening odds preferred. |
| Most Cards odds | Yes | TBD | Opening odds preferred. |
| Cards Over/Under odds | Yes | TBD | Opening odds preferred. |
| BTTS odds | No | TBD | Post-MVP only. |

Source availability must be verified during source research.

## 9. MVP vs Future Data

### MVP

The MVP only requires data needed for:

- recent form
- H2H
- goals
- cards
- standings
- 1X2
- Double Chance
- Goals Over/Under
- Most Cards
- Cards Over/Under
- opening odds

### Post-MVP

The following data is outside the initial MVP scope:

- BTTS
- additional statistical dimensions
- advanced metrics
- player-level data
- xG
- real-time data
- AI prediction models

No additional future requirements are introduced here unless they are already supported by the existing project documentation.

## 10. Open Data Questions

The following questions must be answered during source research.

- Which provider covers each required data domain?
- Which providers provide historical opening odds?
- Which providers provide Double Chance odds?
- Which providers provide Goals Over/Under odds?
- Which providers provide Most Cards odds?
- Which providers provide Cards Over/Under odds?
- What historical depth is available?
- What competitions are covered?
- What licensing or usage restrictions apply?
- Which data can be downloaded as CSV?
- Which data requires an API?
- What are the rate limits and costs?
- How can records from different providers be matched reliably?

These questions are intentionally left open until source research and source mapping are completed.

## 11. Relationship to Next Phase

This document defines data requirements, but it does not define:

- final providers
- database schema
- ingestion implementation
- API clients
- ETL code

Those decisions belong to subsequent phases.

Status: Draft

Phase: Data Definition

Next step: Source Research and Source Mapping
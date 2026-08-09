# Source Mapping

## 1. Purpose

This document maps the data requirements defined in [data-definition.md](data-definition.md) to the candidate external sources researched in [source-research.md](source-research.md).

The goal is to determine which source can provide each required data element, whether the element is direct or derived, whether a secondary source is required, and what limitations remain before provider selection.

This document does not select a definitive provider and does not define ingestion, APIs, or the database model.

## 2. Source Mapping Approach

The mapping below uses only the evidence already documented in the repository.

- Verified: the source documentation explicitly states the capability.
- Partially verified: the source documentation suggests the capability, but the exact semantics, coverage, or completeness are not fully confirmed.
- Unknown: the source documentation does not clearly confirm the capability.
- Not available: the source is not currently a candidate for that requirement based on the reviewed evidence.

Direct means the source is expected to provide the data element itself. Derived means the element should be calculated internally from match-level or source-normalized data.

## 3. Required Data Element Mapping

### 3.1 Competitions

| Field | Description | Category | Required | Primary source | Secondary source | Direct or derived | Evidence status | Historical coverage | Competition coverage | Limitations | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Competition identity | Competition identifier and normalized competition context | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified / Partially verified | TheStatsAPI: 10 years; Football-Data.co.uk: many years, exact depth varies | TheStatsAPI: 150 by default, up to 1,196; Football-Data.co.uk: main and extra leagues, exact coverage not normalized | Football-Data.co.uk has no verified structured API; exact competition list varies by area | Required to attach matches and standings to the correct competition |
| Season | Competition season or season identifier | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified / Partially verified | TheStatsAPI: per-season; Football-Data.co.uk: historical archive across many seasons | TheStatsAPI: documented competition-season endpoints; Football-Data.co.uk: league-based archives | Exact season normalization must be handled carefully across sources | Needed for standings, historical match grouping, and competition context |
| Competition type | League / cup / tournament / group-stage context | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Partially verified / Unknown | TheStatsAPI: competition data documented; Football-Data.co.uk: implied by archive structure | TheStatsAPI: 150+ competitions; Football-Data.co.uk: league and extra league coverage | TheStatsAPI documentation reviewed here does not fully classify every competition type; Football-Data.co.uk type metadata is not fully verified | Useful for differentiating linear leagues, cups, and group-stage tournaments |
| Country/region when applicable | Country or regional competition context | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified / Partially verified | TheStatsAPI: 100+ countries; Football-Data.co.uk: league-focused archive | TheStatsAPI: explicit country coverage; Football-Data.co.uk: country-specific league sections | Country metadata is not equally verified across both sources | Useful for organizing competition scope and data provenance |

### 3.2 Teams

| Field | Description | Category | Required | Primary source | Secondary source | Direct or derived | Evidence status | Historical coverage | Competition coverage | Limitations | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Team identity | Stable team identifier | Team | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified / Partially verified | TheStatsAPI: historical team data; Football-Data.co.uk: results archive contains team names | TheStatsAPI: broad coverage across documented competitions; Football-Data.co.uk: league archives | Source-specific identifiers must be normalized carefully | Required for match linking, standings, and H2H |
| Normalized team name | Canonical team name used internally | Team | Yes | Derived from source-normalized team records | Derived from source-normalized team records | Derived | Verified | Historical coverage depends on source history | Competition coverage follows the source | Normalization rules must resolve spelling differences and naming variants | Must preserve traceability to source-specific names |
| Source-specific identifiers | Provider-specific team identifiers | Team | Yes | TheStatsAPI | Unknown / source-dependent | Direct | Verified / Unknown | TheStatsAPI has documented API identifiers; other sources may only expose names | Depends on provider | Football-Data.co.uk research did not verify stable team IDs; CSV archives may rely on names only | Required for provenance and cross-source reconciliation |

### 3.3 Matches

| Field | Description | Category | Required | Primary source | Secondary source | Direct or derived | Evidence status | Historical coverage | Competition coverage | Limitations | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Match identity | Unique match identifier | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified / Partially verified | TheStatsAPI: historical match data; Football-Data.co.uk: historical results archive | TheStatsAPI: documented competitions; Football-Data.co.uk: league archives | Football-Data.co.uk IDs are not verified in the reviewed documentation | Needed to avoid duplicate records and reconcile provider data |
| Match date | Fixture date and kickoff context | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified | Both sources provide historical dates | Both sources provide competition coverage tied to results | Time zone semantics may vary by provider | Important for recent form and odds alignment |
| Home team | Home-side team reference | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified | Historical match data available | Broad competition coverage | Source-specific team naming may differ | Required for results and home/away splits |
| Away team | Away-side team reference | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified | Historical match data available | Broad competition coverage | Source-specific team naming may differ | Required for results and home/away splits |
| Match status | Scheduled / played / final / invalid / abandoned context | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Partially verified / Unknown | TheStatsAPI supports finalized and live match contexts; Football-Data.co.uk historical results imply completed matches | TheStatsAPI supports multiple competition formats | Non-played or invalid match handling is not equally verified in all sources | Must exclude friendly and invalid matches from MVP statistics |
| Home goals | Goals scored by the home team | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified | Historical results and match stats available | Broad competition coverage | Source semantics for extra time must be handled carefully | Primary input for match result and goals statistics |
| Away goals | Goals scored by the away team | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified | Historical results and match stats available | Broad competition coverage | Source semantics for extra time must be handled carefully | Primary input for match result and goals statistics |
| Match result | Full-time result derived from regular time | Derived | Yes | Derived from match-level data | Derived from match-level data | Derived | Verified | Derived from historical match results | Depends on match coverage | Extra time and penalties must not overwrite the regular-time result | Must be treated as a statistical result based on regular time |
| Regular time result | 90-minute result used for statistics | Match | Yes | TheStatsAPI / Football-Data.co.uk | Derived when necessary | Derived | Verified | Historical match data supports result derivation | Broad competition coverage | Source may expose final result only; regular-time result must be derived or explicitly supported | If a match is decided after extra time or penalties, the regular-time result remains the statistical result |
| Extra time indicator | Whether extra time was played | Match | Yes | Unknown | Unknown | Direct / Derived | Unknown | Not explicitly verified in the reviewed sources | Depends on competition format | Not all sources expose extra-time metadata | Must be retained separately when available |
| Penalty shootout indicator | Whether penalties were used | Match | Yes | Unknown | Unknown | Direct / Derived | Unknown | Not explicitly verified in the reviewed sources | Depends on competition format | Not all sources expose penalty metadata | Must be retained separately when available |
| Penalty shootout winner | Winner after penalties when applicable | Match | No | Unknown | Unknown | Direct / Derived | Unknown | Not explicitly verified in the reviewed sources | Depends on competition format | Requires additional match context not consistently documented | Only relevant when penalty shootout occurred |

### 3.4 Team Performance

| Field | Description | Category | Required | Primary source | Secondary source | Direct or derived | Evidence status | Historical coverage | Competition coverage | Limitations | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Last N matches | Configurable recent-match sample | Derived | Yes | Derived from match-level data | Derived from match-level data | Derived | Verified | Depends on historical match coverage | All official competitions, specific competition, home-only, away-only | Requires enough historical depth per team and competition | Primary use case is last 10 matches |
| Wins | Count of matches won in the selected scope | Derived | Yes | Derived from match-level data | Derived from match-level data | Derived | Verified | Depends on match coverage | Same as last N | Requires regular-time result logic | Must support recent form, H2H, and splits |
| Draws | Count of matches drawn in the selected scope | Derived | Yes | Derived from match-level data | Derived from match-level data | Derived | Verified | Depends on match coverage | Same as last N | Extra time and penalties must not alter the regular-time draw result | Must support recent form, H2H, and splits |
| Losses | Count of matches lost in the selected scope | Derived | Yes | Derived from match-level data | Derived from match-level data | Derived | Verified | Depends on match coverage | Same as last N | Requires consistent home/away and regular-time logic | Must support recent form, H2H, and splits |
| Goals scored | Goals scored in the selected scope | Derived | Yes | Derived from match-level data | Derived from match-level data | Derived | Verified | Depends on match coverage | Same as last N | Must exclude penalty shootout goals | Must support recent form and H2H |
| Goals conceded | Goals conceded in the selected scope | Derived | Yes | Derived from match-level data | Derived from match-level data | Derived | Verified | Depends on match coverage | Same as last N | Must exclude penalty shootout goals | Must support recent form and H2H |
| Yellow cards | Yellow cards in the selected scope | Derived / Direct | Yes | TheStatsAPI | Football-Data.co.uk / Football-Bet-Data | Direct where available; otherwise derived from match stats | Verified / Partially verified | TheStatsAPI explicitly documents cards; Football-Data.co.uk and Football-Bet-Data card statistics are not fully verified | Depends on match coverage | Card betting markets are not the same as card statistics | Use direct card stats where the source is verified; otherwise derive from event data if available |
| Red cards | Red cards in the selected scope | Derived / Direct | Yes | TheStatsAPI | Football-Data.co.uk / Football-Bet-Data | Direct where available; otherwise derived from match stats | Verified / Partially verified | TheStatsAPI explicitly documents cards; other sources not fully verified | Depends on match coverage | Card betting markets are not the same as card statistics | Use direct card stats where the source is verified; otherwise derive from event data if available |
| League position | Standings position for a competition context | Standings | Yes | TheStatsAPI | Unknown / source-dependent | Direct / Derived | Verified | Standings endpoints documented; historical standings may also be derived from match results | Coverage depends on competition-season availability | Linear leagues are best supported; cup formats may not provide standings | Must distinguish source-provided standings from derived standings |
| Historical H2H | Historical results between two teams | Derived | Yes | Derived from match-level data | Depends on provider | Derived | Verified as derivable | Depends on match-history coverage | Can be filtered to same competition or mixed competitions | Requires sufficient historical records, consistent team normalization, and competition scoping | Must remain configurable by competition and historical window |

### 3.5 Betting Markets

Core MVP markets are mapped below first. Both Teams To Score remains documented as a secondary/post-MVP market and must not be treated as a required MVP market.

| Field | Description | Category | Required | Primary source | Secondary source | Direct or derived | Evidence status | Historical coverage | Competition coverage | Limitations | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1X2 | Home / Draw / Away market | Odds | Yes | TheStatsAPI | UK Odds API / Odds-API.io / Football-Bet-Data | Direct | Verified | Historical odds available on multiple sources | Coverage depends on provider | Exact market semantics differ across providers | Core MVP market |
| Double Chance | 1X / X2 / 12 market | Odds | Yes | TheStatsAPI | UK Odds API / Football-Bet-Data | Direct | Verified / Partially verified | Documented on TheStatsAPI and Football-Bet-Data | Coverage depends on provider | Historical retrieval and opening line semantics are not uniformly verified | Core MVP market |
| Goals Over/Under | Goals line market | Odds | Yes | TheStatsAPI | UK Odds API / Football-Bet-Data / Odds-API.io | Direct | Verified / Partially verified | Historical odds available on multiple sources | Coverage depends on provider | Must verify line semantics and historical retrieval | Core MVP market |
| Most Cards | Card-result market | Odds | Yes | UK Odds API | Unknown / source-dependent | Direct | Partially verified | Cards are documented as a market category by UK Odds API | Coverage not fully verified by competition | Must distinguish card statistics from card betting markets | Selected cards market for MVP |
| Cards Over/Under | Cards line market | Odds | Yes | UK Odds API | Unknown / source-dependent | Direct | Partially verified | Cards are documented as a market category by UK Odds API | Coverage not fully verified by competition | Must distinguish card statistics from card betting markets | Core MVP market, separate from card event statistics |
| Both Teams To Score | Secondary/post-MVP market | Odds | No | TheStatsAPI / Odds-API.io / UK Odds API / Football-Bet-Data | Any verified odds source | Direct | Verified / Partially verified | Documented by multiple sources | Coverage depends on provider | Explicitly post-MVP and secondary | Not a core MVP market |
| Opening odds | Preferred odds reference | Odds | Yes | Football-Data.co.uk / TheStatsAPI / source-specific | Unknown / source-dependent | Direct | Partially verified | Historical opening odds are explicitly referenced by Football-Data.co.uk and TheStatsAPI | Coverage varies by provider | Opening odds must not be conflated with closing or early snapshot odds | Can be bookmaker-specific or aggregated, depending on source |

## 4. Derived Statistics

The statistics below should be calculated internally from match-level or odds data rather than requested as separate source-provided facts whenever possible.

- Last N match form.
- Wins, draws, and losses.
- Goals scored and conceded.
- Goals per match.
- Average goals conceded per match.
- Average yellow cards.
- Average red cards.
- H2H aggregates.
- Home/away splits.
- Table-derived metrics.
- Implied probability from odds.

These derived statistics reduce external dependencies and preserve consistent project logic across sources.

## 5. Opening Odds Mapping

Opening odds are a critical requirement and must be treated separately from generic historical odds.

- Football-Data.co.uk: opening odds are explicitly referenced, but the exact semantics and bookmaker versus aggregated representation are only partially verified.
- TheStatsAPI: opening and closing lines are referenced, but opening odds semantics are only partially verified.
- Football-Bet-Data: opening odds semantics are unknown.
- Odds-API.io: opening odds semantics are unknown.
- UK Odds API: opening odds semantics are unknown.

Historical odds must not be treated as equivalent to opening odds.

## 6. Cards Market Mapping

Pay particular attention to the difference between card statistics and card betting markets.

- TheStatsAPI: card statistics are verified; cards betting markets are not verified.
- Football-Data.co.uk: card markets are unknown; card statistics are not fully verified.
- Football-Bet-Data: cards markets are unknown; card statistics are not fully verified.
- Odds-API.io: cards markets are unknown.
- UK Odds API: cards betting markets are partially verified, but the distinction between Most Cards and Cards Over/Under must be confirmed before provider selection.

## 7. Candidates for Provider Selection

The sources below are candidates identified for evaluation in the next phase, Provider Selection. They are not selected providers and they are not definitive choices.

The strongest candidates by data area are:

1. Match and historical statistics: TheStatsAPI, with Football-Data.co.uk as a complementary archive source.
   - TheStatsAPI has verified matches, results, standings, and match statistics.
   - Football-Data.co.uk provides a broad historical archive with downloadable results and odds.

2. Standings: TheStatsAPI.
   - Standings endpoints are explicitly documented.

3. Match cards: TheStatsAPI.
   - Card statistics are explicitly documented.

4. Opening odds: TheStatsAPI and Football-Data.co.uk.
   - Both sources explicitly reference opening lines or opening odds, though the exact semantics remain only partially verified.

5. Betting markets: TheStatsAPI, UK Odds API, Odds-API.io, and Football-Bet-Data.
   - TheStatsAPI documents several relevant football betting markets.
   - UK Odds API documents broad market coverage including cards and over/under.
   - Odds-API.io documents a wide set of markets, though it is primarily real-time.
   - Football-Bet-Data documents several relevant betting markets and historical odds.

6. Cards betting markets: UK Odds API.
   - It explicitly documents cards as a market category.
   - The exact mapping for Most Cards versus Cards Over/Under still needs verification.

## 8. Coverage Gaps

The following requirements remain insufficiently verified across the current candidate sources:

- H2H coverage as a directly documented provider capability.
- Verified yellow and red card statistics outside TheStatsAPI.
- Verified Most Cards semantics with a clear historical opening odds model.
- Verified Cards Over/Under semantics with a clear historical opening odds model.
- Uniform opening-odds semantics across all candidate odds providers.
- Consistent CSV availability across all required data domains.
- Clear commercial-use terms for several candidate sources.

## 9. Provider Selection Criteria

The next phase should evaluate providers using objective criteria:

- Historical depth.
- Competition coverage.
- Data completeness.
- Opening odds availability.
- Betting market coverage.
- Cards market coverage.
- Data consistency.
- API or CSV accessibility.
- Pricing.
- Rate limits.
- Licensing.
- Commercial usage.
- Reliability.
- Ease of Python integration.
- Ability to preserve source provenance.

## 10. Recommendation

Provider selection remains pending.

No definitive provider has been selected.

The candidates listed in this document must be evaluated during the Provider Selection phase.

Provider selection must be based on objective criteria rather than the current candidate ranking.

The current evidence is sufficient to identify strong candidates for different data areas, but it is not sufficient to definitively select a single provider for the entire project.

## 11. Data Element Matrix

This matrix mirrors the detailed mapping above and uses the same evidence levels, direct-versus-derived decisions, and required-versus-optional distinctions.

| Data element | Category | Required | Primary source | Secondary source | Direct or derived | Evidence status | Historical coverage | Competition coverage | Limitations | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Competition identity | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified / Partially verified | Strong | Strong | Normalization required | Used to attach matches and standings to competition context |
| Season | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified / Partially verified | Strong | Strong | Season mapping varies by source | Needed for historical grouping |
| Match date | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified | Strong | Strong | Time zone semantics may differ | Needed for recent form and odds alignment |
| Home team | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified | Strong | Strong | Source naming differences | Required for home/away context |
| Away team | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified | Strong | Strong | Source naming differences | Required for home/away context |
| Match status | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Partially verified / Unknown | Strong | Strong | Invalid-match handling varies | Must exclude friendly and invalid fixtures |
| Home goals | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified | Strong | Strong | Extra-time semantics require care | Base match scoring input |
| Away goals | Match | Yes | TheStatsAPI | Football-Data.co.uk | Direct | Verified | Strong | Strong | Extra-time semantics require care | Base match scoring input |
| Match result | Derived | Yes | Derived | Derived | Derived | Verified | Strong | Strong | Must be based on regular time | Do not use extra-time or penalties to change the base result |
| Regular time result | Match | Yes | TheStatsAPI / Football-Data.co.uk | Derived if needed | Derived | Verified | Strong | Strong | May need derivation from final score | Statistical result must remain the 90-minute result |
| Extra time indicator | Match | Yes | Unknown | Unknown | Direct / Derived | Unknown | Weak | Weak | Not verified across sources | Retain separately when available |
| Penalty shootout indicator | Match | Yes | Unknown | Unknown | Direct / Derived | Unknown | Weak | Weak | Not verified across sources | Retain separately when available |
| Penalty shootout winner | Match | No | Unknown | Unknown | Direct / Derived | Unknown | Weak | Weak | Not verified across sources | Only relevant when penalties occur |
| Last N matches | Derived | Yes | Derived | Derived | Derived | Verified | Strong | Strong | Requires enough historical depth | Configurable sample size |
| Wins | Derived | Yes | Derived | Derived | Derived | Verified | Strong | Strong | Depends on match coverage | Form and H2H aggregate input |
| Draws | Derived | Yes | Derived | Derived | Derived | Verified | Strong | Strong | Depends on match coverage | Form and H2H aggregate input |
| Losses | Derived | Yes | Derived | Derived | Derived | Verified | Strong | Strong | Depends on match coverage | Form and H2H aggregate input |
| Goals scored | Derived | Yes | Derived | Derived | Derived | Verified | Strong | Strong | Must exclude shootout goals | Form and H2H aggregate input |
| Goals conceded | Derived | Yes | Derived | Derived | Derived | Verified | Strong | Strong | Must exclude shootout goals | Form and H2H aggregate input |
| Yellow cards | Derived / Match | Yes | TheStatsAPI | Football-Data.co.uk / Football-Bet-Data | Direct or derived | Verified / Partially verified | Strong in TheStatsAPI | Strong in TheStatsAPI; weaker elsewhere | Card markets are separate from card stats | Prefer direct card stats where verified |
| Red cards | Derived / Match | Yes | TheStatsAPI | Football-Data.co.uk / Football-Bet-Data | Direct or derived | Verified / Partially verified | Strong in TheStatsAPI | Strong in TheStatsAPI; weaker elsewhere | Card markets are separate from card stats | Prefer direct card stats where verified |
| League position | Standings | Yes | TheStatsAPI | Unknown | Direct / Derived | Verified | Strong | Strong | Cup formats may not have standings | Source standings preferred when available |
| Historical H2H | Derived | Yes | Derived | Derived | Derived | Verified | Strong if match history exists | Depends on competition filter | Requires team normalization and competition scoping | Configurable by competition and historical period |
| 1X2 | Odds | Yes | TheStatsAPI | UK Odds API / Odds-API.io / Football-Bet-Data | Direct | Verified | Strong | Strong | Semantics vary by provider | Core market |
| Double Chance | Odds | Yes | TheStatsAPI | UK Odds API / Football-Bet-Data | Direct | Verified / Partially verified | Strong | Strong | Needs line semantics confirmation | Core market |
| Goals Over/Under | Odds | Yes | TheStatsAPI | UK Odds API / Football-Bet-Data / Odds-API.io | Direct | Verified / Partially verified | Strong | Strong | Historical odds not always equal opening odds | Core market |
| Most Cards | Odds | Yes | UK Odds API | Unknown | Direct | Partially verified | Unknown to partial | Depends on bookmaker/league coverage | Must not be conflated with card event stats | Selected cards market |
| Cards Over/Under | Odds | Yes | UK Odds API | Unknown | Direct | Partially verified | Unknown to partial | Depends on bookmaker/league coverage | Must not be conflated with card event stats | Selected cards market |
| Both Teams To Score | Odds | No | TheStatsAPI / Odds-API.io / UK Odds API / Football-Bet-Data | Any verified odds source | Direct | Verified / Partially verified | Strong | Strong | Secondary/post-MVP market, not core MVP | Post-MVP only |
| Opening odds | Odds | Yes | Football-Data.co.uk / TheStatsAPI | Unknown | Direct | Partially verified | Strong in two sources | Strong in two sources | Semantics differ by provider; historical odds are not equivalent | Critical requirement for the project |

## 12. Unresolved Requirements

The following requirements remain unresolved before provider selection:

- A provider with verified H2H coverage that fits the full MVP scope.
- A provider with verified cards betting markets that clearly distinguish Most Cards from Cards Over/Under.
- A provider with unambiguous opening odds semantics across the relevant markets.
- A provider with verified historical odds retrieval for all core MVP markets.
- A provider with verified CSV availability for the required non-odds data, if CSV is still needed.
- Clear commercial-use terms across the entire required data set.

## 13. Validation Notes

- Every required data element has been mapped.
- Derived statistics are separated from source-provided statistics.
- Opening odds are treated separately from generic historical odds.
- Card statistics are not conflated with card betting markets.
- H2H is treated as derivable from match history, while sufficient historical coverage remains a provider-selection concern.
- No source capability has been inferred without evidence.
- No definitive provider has been selected.

Status: Completed

Phase: Source Mapping

Next Step: Provider Selection
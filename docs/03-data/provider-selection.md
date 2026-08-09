# Provider Selection

## 1. Purpose

This document evaluates the candidate providers identified in Source Research and Source Mapping and records the final MVP provider strategy for the historical football statistics and betting analytics project.

The phase is limited to provider evaluation and selection. It does not define the data model, ingestion, APIs, migrations, or application code.

## 2. Scope And Evidence Rules

The project requirements used for this phase are the ones already defined in the repository:

- historical data only
- official matches only
- friendly matches excluded
- configurable last N matches
- H2H support for same competition and mixed competitions
- historical betting odds as a mandatory requirement (bookmaker, market, timestamp)
- explicit Opening Odds as desirable when reliably available, but not a mandatory MVP requirement
- Most Cards and Cards Over/Under as MVP markets
- BTTS as secondary/post-MVP

The MVP Competition Scope is defined as: Premier League, La Liga, Bundesliga, Serie A, and UEFA Champions League.

### 2.1 Opening Odds Product Requirement Decision

Explicit Opening Odds are NOT a mandatory MVP requirement.

The project must prioritize historical betting odds rather than requiring an explicit opening price for every bookmaker and every market.

**Mandatory odds requirements**

- Historical odds associated with match, bookmaker, market, and timestamp.
- Bookmaker identification must be preserved.
- Market identification must be preserved.
- Temporal context (timestamp) must be preserved where the provider supplies it.

**Optional / desirable**

- Explicit Opening Odds: the earliest bookmaker price explicitly labeled as the opening line by the provider.
- Explicit Closing Odds: the last bookmaker price before kickoff, explicitly labeled as the closing line.

Both are desirable when the provider reliably supplies and labels them. Neither is a mandatory MVP requirement.

**Definitions**

- Historical Odds: an odds observation associated with match + market + bookmaker + timestamp.
- Opening Odds: the explicitly identified opening price for a specific bookmaker and market, when the provider documents and labels it as such.
- Closing Odds: the explicitly identified last pre-match price, when the provider documents and labels it as such.
- First available snapshot: the earliest captured record. Must NOT be automatically treated as Opening Odds unless the provider explicitly documents that behavior.

**Rationale**

1. Odds vary between bookmakers for the same match and market.
2. Odds vary over time for the same bookmaker and market.
3. A single universal opening price does not exist across all bookmakers.
4. Historical odds with bookmaker, market, and timestamp provide the data needed for statistical and market analysis.
5. Explicit Opening Odds remain useful when reliably provided and should be stored when available.
6. The system must never silently infer opening prices without explicit provider semantics.
7. Requiring explicit Opening Odds across all five markets and both providers would unnecessarily constrain provider selection without a proportional increase in analytical value at the MVP stage.

Evidence classification in this document:

- Verified: explicitly documented by the provider's current official documentation.
- Partially verified: documented, but semantics, coverage, or completeness are not fully confirmed.
- Unknown / Requires verification: not clearly documented.

## 3. Evaluation Summary

The candidate set from Source Research was evaluated as follows:

- TheStatsAPI: strongest football stats provider, strongest verified historical-odds source, and best fit for the match/standings/statistics layer.
- UK Odds API: strongest verified source for the missing MVP betting markets, especially Double Chance and cards markets, with historical snapshots and timestamps verified.
- Football-Data.co.uk: strong free historical archive, but not sufficient as the primary MVP provider because structured API support and market semantics are not fully verified.
- Odds-API.io: strong odds API and SDK documentation, but it is primarily oriented toward real-time odds rather than the project's historical-first MVP.
- Football-Bet-Data: useful historical and H2H-oriented product, but too much of the required MVP surface remains unverified for a primary selection.

## 4. MVP Competition Scope

The initial MVP Competition Scope is intentionally small and representative. It is limited to the competitions below so that the project can validate historical match coverage, standings, H2H, and betting-market availability without attempting to support the full football universe in the MVP.

| Competition | Country/Region | Type | Reason for inclusion | Expected analytical value | Provider considerations |
|---|---|---|---|---|---|
| Premier League | England | Domestic league | High-volume top-tier league with strong statistical value and clear league-table structure | Supports recent form, standings, cards, H2H, and odds analysis on a dense fixture set | Requires provider verification for historical match depth, cards, standings, odds, and opening odds |
| La Liga | Spain | Domestic league | Top-tier European league with enough historical depth to exercise cross-season analysis | Useful for comparing league styles, team form, and market behavior across a major competition | Requires provider verification for historical match depth, cards, standings, odds, and opening odds |
| Bundesliga | Germany | Domestic league | Top-tier league with strong historical continuity and clear statistical structure | Useful for validating match history, standings, and betting-market coverage in another major domestic context | Requires provider verification for historical match depth, cards, standings, odds, and opening odds |
| Serie A | Italy | Domestic league | Top-tier league with long-running historical coverage and distinct statistical patterns | Adds another high-value league for H2H, form, standings, and odds comparisons | Requires provider verification for historical match depth, cards, standings, odds, and opening odds |
| UEFA Champions League | Europe | International competition | Representative cross-border competition that exercises group-stage and mixed-competition analysis | Useful for validating mixed competition H2H, competition context, and betting-market coverage beyond domestic leagues | Requires provider verification for match history, group-stage context, standings where applicable, odds, and opening odds |

This is the MVP target scope only. It is not a permanent limitation. Additional competitions can be added later without changing the core project architecture.

### 4.1 Scope Rationale

The selected scope balances analytical value and manageability:

- it includes multiple top-tier domestic leagues so the MVP can test repeated statistics and market behavior across different competitions;
- it includes one international competition so the MVP can validate non-domestic context and mixed-competition H2H behavior;
- it stays small enough that provider validation remains practical before implementation;
- it avoids assuming that a large provider catalog should automatically become the MVP scope.

### 4.2 Excluded Categories

The following categories are excluded from the MVP scope only:

- Friendlies
- Youth competitions
- Reserve-team competitions
- Lower-tier competitions without sufficient data coverage
- Competitions without the required betting-market coverage
- Competitions whose historical data cannot be reliably obtained

These exclusions do not permanently remove the categories from the architecture. They are scope decisions for the MVP only.

### 4.3 Relation To Provider Selection

The MVP Competition Scope is the reference set for the next Provider Selection validation step.

For each selected competition, the provider evaluation must confirm:

- match-history availability;
- historical depth;
- cards;
- standings;
- H2H feasibility;
- historical odds with bookmaker, market, and timestamp;
- betting-market availability;
- licensing considerations.

The MVP Competition Scope is now confirmed. Provider coverage has been validated against the five selected competitions.

### 4.4 Champions League Validation Requirements

The UEFA Champions League requires specific validation beyond domestic leagues:

- historical match coverage across multiple group stages and knockout rounds;
- competition and season identification for group-stage and knockout contexts;
- standings or equivalent group-stage information where applicable;
- cards;
- odds and required betting markets;
- H2H derivability across teams from different domestic leagues.

League-style standings do not apply identically to the Champions League. Provider support for the competition structure must be confirmed separately.

## 5. Candidate Evaluation

### 5.1 TheStatsAPI

Verified from current official documentation:

- fixtures, results, standings, match stats, team data, player data, and odds are provided through a JSON REST API.
- match statistics include cards, goals, xG, possession, shots, passes, and related events.
- competition coverage is documented at 150 competitions by default, with up to 1,196 on request.
- historical match data goes back 10 years.
- opening and last-seen odds are explicitly documented for supported matches.
- covered bookmaker set includes Bet365, Pinnacle, Paddy Power, Betfair Sportsbook, and Kambi.
- paid plans allow commercial usage.
- pricing is public and starts at $50/month.

Partially verified or limited:

- Double Chance is not explicitly confirmed in the reviewed official pages.
- Most Cards and Cards Over/Under are not explicitly confirmed as opening-odds sources, even where the market families themselves are documented elsewhere.
- CSV access was not verified.
- historical odds availability varies by match, competition, bookmaker, and market.
- exact market semantics are not uniform across all supported odds pages.

Assessment:

- Best verified source for the football stats layer.
- Best verified source for opening odds.
- Not sufficient by itself for the full MVP because the required cards betting markets and Double Chance are not explicitly verified.

### 5.2 UK Odds API

Verified from current official documentation:

- football events, odds, best odds, arbitrage, market catalog, and historical odds snapshots are documented.
- a market catalog is exposed through stable keys and groups.
- Double Chance is explicitly documented in the market catalog.
- cards markets are explicitly documented, including Most Cards, Total Cards, Total Cards 3-Way, Total Home Team Cards, Total Away Team Cards, and booking/sending-off markets.
- Total Cards Over/Under is explicitly documented in the arbitrage market catalog.
- historical snapshots include capture timestamps via X-Data-Captured-At and the history endpoints expose capture times and historical snapshots.
- supported plans and request limits are documented.
- rate-limit and caching headers are documented.

Partially verified or limited:

- true opening odds are not explicitly defined as opening prices in the reviewed official pages.
- historical snapshots and odds timelines are not equivalent to explicitly documented opening odds.
- the docs show pre-match odds and historical snapshots, but the first available snapshot must not be treated as the opening price without further verification.
- historical depth for the required MVP competitions is not fully quantified in the reviewed documentation.
- commercial-use terms were not fully verified beyond the published terms and plan pages.

Assessment:

- Best verified source for the missing betting-market layer, especially Double Chance and cards markets.
- Strong technical API documentation with stable market keys and historical snapshots.
- Not sufficient by itself for the MVP because true opening odds are not explicitly documented as opening prices.

### 5.3 Football-Data.co.uk

Verified from current official documentation:

- historical football results and betting odds are available in computer-ready Excel/CSV format.
- the archive covers many seasons of results, odds, and match statistics.
- the site explicitly references opening odds alerts and closing odds tracking content.
- the archive is free.

Partially verified or limited:

- exact structured API support was not verified.
- exact historical depth varies by league and competition.
- standings were not explicitly verified in the reviewed documentation.
- H2H was not explicitly verified as a provider capability.
- cards betting markets were not explicitly verified.
- commercial-use terms were not clearly verified.

Assessment:

- Useful historical archive and a strong fallback source for CSV/Excel consumption.
- Not a primary MVP provider because the provider surface is not verified enough for the required market coverage and structured access.

### 5.4 Odds-API.io

Verified from current official documentation:

- REST JSON API, WebSocket feed, and an official Python SDK are documented.
- paid plans and request limits are documented.
- historical data is mentioned.
- the service documents many markets and a large bookmaker set.

Partially verified or limited:

- the product is primarily oriented toward real-time odds.
- opening odds semantics are not clearly verified.
- football match statistics, standings, H2H, yellow cards, and red cards are not verified as required MVP data.
- commercial-use terms and redistribution limits were verified in the terms page, but those terms are restrictive and are not a good fit for a broad historical portfolio use case without review.

Assessment:

- Good odds infrastructure, but not the best fit for this historical football MVP.
- Not selected.

### 5.5 Football-Bet-Data

Verified from current official documentation:

- historical coverage back to 1998 across 65+ leagues is documented.
- fixtures/results and H2H features are documented.
- Excel exports are documented.
- betting markets are documented.

Partially verified or limited:

- exact match statistics required by the MVP are not fully enumerated.
- opening odds semantics are not clearly defined.
- cards betting markets are not clearly verified.
- standings were not explicitly confirmed.
- commercial-use terms were not clearly verified.

Assessment:

- Useful historical football product, but too many MVP-critical capabilities remain unverified.
- Not selected.

## 6. Strategy Evaluation

### Strategy A: Single provider

Candidate considered: TheStatsAPI alone.

Coverage:

- Strong for match data, standings, cards statistics, H2H derivation, and opening odds.
- Strong for 1X2, BTTS, totals, Asian handicap, corners, and other football odds pages.
- Not explicitly verified for Double Chance and the required cards betting markets.

Complexity:

- Lowest operational complexity.

Cost:

- Moderate monthly subscription.

Data consistency:

- High, because one provider reduces reconciliation work.

Historical completeness:

- Good, but still market-dependent and not verified for all required betting markets.

Licensing:

- Commercial usage is documented for paid plans.

Maintenance burden:

- Low.

Risk of provider dependency:

- High.

Verdict:

- Rejected for the MVP because it does not explicitly verify the full required betting-market set, especially Double Chance and cards markets.

### Strategy B: Sports data + odds provider

Candidate considered: TheStatsAPI + UK Odds API.

Coverage:

- TheStatsAPI covers the football stats layer, standings, cards statistics, and opening/last-seen odds for supported matches.
- UK Odds API covers the missing betting markets, including Double Chance and cards markets, plus historical snapshots and a stable market catalog.

Complexity:

- Moderate.

Cost:

- Higher than a single-provider setup, but still the smallest viable combination that covers the documented gaps.

Data consistency:

- Good, but normalization is needed across provider identifiers and market naming.

Historical completeness:

- Better than any single provider among the reviewed candidates.

Licensing:

- TheStatsAPI paid plans allow commercial use.
- UK Odds API commercial terms require review against the intended use case, but the published plan and terms pages are available.

Maintenance burden:

- Moderate.

Risk of provider dependency:

- Lower than a single-provider strategy, but still material.

Verdict:

- Recommended as the current provisional provider strategy and the smallest viable provider combination for the MVP.

### Strategy C: Other combination

Candidates considered:

- Football-Data.co.uk + UK Odds API
- Football-Data.co.uk + TheStatsAPI
- Odds-API.io + TheStatsAPI

Verdict:

- Rejected.
- These combinations either leave the stats layer under-verified, leave opening odds ambiguous, or add complexity without closing the critical gaps more cleanly than Strategy B.

## 7. Historical Provider Coverage Validation

This section records the validated coverage of both provisional providers against the five defined MVP competitions. Evidence is drawn from the current official documentation of each provider.

### 7.1 Evidence Sources

- TheStatsAPI: official coverage table at thestatsapi.com/coverage (retrieved 2026-08-09); official standings API docs; official match stats API docs; official odds API docs; official terms of service.
- UK Odds API: official league coverage at ukoddsapi.com/league-coverage (retrieved 2026-08-09); official market coverage at ukoddsapi.com/market-coverage; official plans and pricing docs; official API reference.

### 7.2 TheStatsAPI Competition Coverage

The following data comes directly from the official coverage table. The table columns shown by the provider are: Seasons, Results, Events, Match Stats, and Odds.

For the purposes of this project, the columns are interpreted as:

- Results: match results and goals
- Events: minute-by-minute events including goals, cards, and substitutions
- Match Stats: possession, shots, passes, corners, fouls, cards per match
- Odds: pre-match odds from covered bookmakers

The standings endpoint supports group-stage tables and is explicitly documented for the Champions League (verified from thestatsapi.com/football/standings FAQ).

Opening odds: the provider explicitly documents opening and last-seen prices where captured, per the historical odds docs and the odds API FAQ. Availability depends on competition, bookmaker, and market. It is not guaranteed for every match or every competition. This interpretation is maintained from the prior source research.

| Competition | Seasons documented | Season range | Results | Events | Match Stats | Standings | Odds | Opening odds | Notes |
|---|---|---|---|---|---|---|---|---|---|
| Premier League | 9 | 18/19–26/27 | Verified | Verified | Verified | Verified | Verified | Partially verified | Opening and last-seen where captured; not guaranteed per match |
| La Liga | 7 | 20/21–26/27 | Verified | Verified | Verified | Verified | Verified | Partially verified | Opening and last-seen where captured; not guaranteed per match |
| Bundesliga | 7 | 20/21–26/27 | Verified | Verified | Verified | Verified | Verified | Partially verified | Opening and last-seen where captured; not guaranteed per match |
| Serie A | 7 | 20/21–26/27 | Verified | Verified | Verified | Verified | Verified | Partially verified | Opening and last-seen where captured; not guaranteed per match |
| UEFA Champions League | 7 | 20/21–26/27 | Verified | Verified | Verified | Verified (group-stage per-group) | Verified | Partially verified | Group-stage standings returned per group; knockout rounds have no standings |

Card statistics are documented per match (cards field within match stats and events). Card statistics are NOT the same as card betting markets. Card betting markets (Most Cards, Cards Over/Under) are not listed in the odds markets page for this provider.

Documented odds markets (verified from official odds API docs): 1X2, Asian handicap, Over/Under, BTTS, Draw No Bet, Corners. Double Chance is not listed. Most Cards and Cards Over/Under are not listed.

H2H: historical match data is retrievable per competition and date range. Same-competition and mixed-competition H2H are derivable from the match history. The historical depth varies by competition but is at least 7 seasons for all five MVP competitions.

### 7.3 UK Odds API Competition Coverage

The following data comes from the official league coverage page (346 competitions listed) and the official market catalog page.

All five MVP competitions are confirmed in the supported leagues list:

- Champions League: listed as a top competition
- Premier League: listed as a top competition (England)
- Bundesliga: listed as a top competition (Germany)
- Serie A: listed as a top competition (Italy)
- La Liga: listed as a top competition (Spain)

Historical odds require the Pro plan or above (confirmed from plans and pricing docs). Historical odds are NOT available on the Free or Starter tier.

Double Chance, Most Cards, Total Cards Over/Under: verified as available in the market catalog (core or full packages; Most Cards is full-only).

Opening odds: the provider does NOT explicitly define or document opening odds. Historical snapshots with capture timestamps are documented. The first available snapshot for a fixture is not defined by the provider as an opening price.

Match statistics (results, goals, cards as event data, standings): NOT documented as a product capability. UK Odds API is an odds-only product.

| Competition | Competition listed | Historical odds | Match results | Cards | Standings | 1X2 | Double Chance | Goals O/U | Most Cards | Cards O/U | Opening odds | Plan required | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Premier League | Verified | Verified (Pro+) | Not covered | Not covered | Not covered | Verified | Verified | Verified | Verified | Verified | Requires verification | Pro (£149/month) | Opening odds not explicitly documented; Most Cards is full-only |
| La Liga | Verified | Verified (Pro+) | Not covered | Not covered | Not covered | Verified | Verified | Verified | Verified | Verified | Requires verification | Pro (£149/month) | Same limitations as Premier League |
| Bundesliga | Verified | Verified (Pro+) | Not covered | Not covered | Not covered | Verified | Verified | Verified | Verified | Verified | Requires verification | Pro (£149/month) | Same limitations as Premier League |
| Serie A | Verified | Verified (Pro+) | Not covered | Not covered | Not covered | Verified | Verified | Verified | Verified | Verified | Requires verification | Pro (£149/month) | Same limitations as Premier League |
| UEFA Champions League | Verified | Verified (Pro+) | Not covered | Not covered | Not covered | Verified | Verified | Verified | Verified | Verified | Requires verification | Pro (£149/month) | Same limitations as Premier League |

Historical depth for UK Odds API is not publicly documented per competition. The provider documents historical snapshot capture endpoints but does not state how many seasons of historical odds are available for each competition.

### 7.4 Consolidated Coverage Matrix

This matrix combines both providers for each competition and dimension.

| Competition | Provider | Historical Matches | Seasons | Results/Goals | Cards (statistics) | Standings | 1X2 | Double Chance | Goals O/U | Most Cards | Cards O/U | Opening Odds | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Premier League | TheStatsAPI | Verified | 9 (18/19–26/27) | Verified | Verified | Verified | Verified | Not documented | Verified | Not documented | Not documented | Partially verified | Partial | Opening/last-seen where captured; Double Chance, Most Cards, Cards O/U not listed in odds markets |
| Premier League | UK Odds API | Not covered | Not publicly documented | Not covered | Not covered | Not covered | Verified | Verified | Verified | Verified | Verified | Requires verification | Partial | Historical odds on Pro plan; opening odds not explicitly documented; first snapshot ≠ opening price |
| La Liga | TheStatsAPI | Verified | 7 (20/21–26/27) | Verified | Verified | Verified | Verified | Not documented | Verified | Not documented | Not documented | Partially verified | Partial | Same profile as Premier League |
| La Liga | UK Odds API | Not covered | Not publicly documented | Not covered | Not covered | Not covered | Verified | Verified | Verified | Verified | Verified | Requires verification | Partial | Same profile as Premier League |
| Bundesliga | TheStatsAPI | Verified | 7 (20/21–26/27) | Verified | Verified | Verified | Verified | Not documented | Verified | Not documented | Not documented | Partially verified | Partial | Same profile as Premier League |
| Bundesliga | UK Odds API | Not covered | Not publicly documented | Not covered | Not covered | Not covered | Verified | Verified | Verified | Verified | Verified | Requires verification | Partial | Same profile as Premier League |
| Serie A | TheStatsAPI | Verified | 7 (20/21–26/27) | Verified | Verified | Verified | Verified | Not documented | Verified | Not documented | Not documented | Partially verified | Partial | Same profile as Premier League |
| Serie A | UK Odds API | Not covered | Not publicly documented | Not covered | Not covered | Not covered | Verified | Verified | Verified | Verified | Verified | Requires verification | Partial | Same profile as Premier League |
| UEFA Champions League | TheStatsAPI | Verified | 7 (20/21–26/27) | Verified | Verified | Verified (per-group stage) | Verified | Not documented | Verified | Not documented | Not documented | Partially verified | Partial | Group standings per group; knockout rounds have no standings equivalent |
| UEFA Champions League | UK Odds API | Not covered | Not publicly documented | Not covered | Not covered | Not covered | Verified | Verified | Verified | Verified | Verified | Requires verification | Partial | Same profile as Premier League |

### 7.5 Coverage Gaps Identified

#### TheStatsAPI gaps

- Double Chance is not listed in any documented odds market for this provider.
- Most Cards is not listed in any documented odds market for this provider.
- Cards Over/Under is not listed in any documented odds market for this provider.
- Opening odds are partially verified: available where captured, but not guaranteed for every match, competition, or market.
- CSV access is not documented.

#### UK Odds API gaps

- Match results, goals, cards as event data, and standings are not product capabilities of this provider.
- Opening odds are not explicitly defined or documented by this provider.
- Historical odds depth by competition is not publicly documented.
- Historical odds require the Pro plan (£149/month).
- Most Cards is a full-package market (requires package=full, which requires Pro or above).

#### Combined strategy gaps

- Opening odds for the Double Chance, Most Cards, and Cards Over/Under markets remain unresolved. TheStatsAPI does not list these markets. UK Odds API does not define opening prices.
- Historical odds depth on UK Odds API by competition is not publicly documented.
- Commercial/licensing terms require verification for both providers in the context of portfolio/demo and future commercial use.

### 7.6 H2H Feasibility

- TheStatsAPI provides at least 7–9 seasons of historical match data for all five MVP competitions.
- Match data is retrievable by competition, which allows same-competition H2H to be computed.
- Historical data covers multiple competitions, allowing mixed-competition H2H to be computed from the match history.
- H2H is a derived project output, not a provider-native feature.
- Conclusion: historical match coverage on TheStatsAPI is sufficient to derive same-competition and mixed-competition H2H for the five MVP competitions, subject to the project's match-level data quality and normalization requirements.

### 7.7 Licensing Summary

#### TheStatsAPI (from official terms of service, last updated April 1, 2026)

- Usage in own applications, websites, and internal tools: explicitly allowed.
- Commercial use in own products: explicitly allowed on paid plans.
- Redistribution of raw data to third parties: explicitly prohibited.
- Resale or sublicensing of data: explicitly prohibited.
- Bulk republication as a standalone dataset or feed: explicitly prohibited.
- Competing product using the data as a data source: explicitly prohibited.
- Caching: permitted only to the extent reasonably necessary to operate the application.
- Portfolio/demo use within own application: appears permitted, but is not explicitly confirmed for public-facing portfolio projects. Requires contact with the provider to confirm before deployment.

#### UK Odds API (from official plans and pricing docs)

- Historical odds: Pro plan required (£149/month).
- Advanced markets (full package including Most Cards): Pro plan required.
- Arbitrage endpoints: Business plan required (£359/month).
- Commercial terms beyond plan gating: not explicitly documented in the reviewed pages. UK Odds API terms are not referenced in the coverage, pricing, or market docs.
- Commercial/licensing terms: Requires legal/licensing verification.

## 8. Critical Requirements Status

### Verified

- Premier League, La Liga, Bundesliga, Serie A, and UEFA Champions League are all present in TheStatsAPI coverage (7–9 seasons per competition).
- Match results, goals, cards as match statistics, standings, and events are verified for all five competitions on TheStatsAPI.
- Group-stage standings for the UEFA Champions League are explicitly supported by TheStatsAPI.
- 1X2 and Goals Over/Under markets are verified for all five competitions on both providers.
- Double Chance, Most Cards, and Cards Over/Under market availability is verified on UK Odds API.
- H2H is derivable from match history on TheStatsAPI for all five competitions.
- Historical odds (not opening odds) for all five competitions are verified on UK Odds API at Pro plan level.
- TheStatsAPI paid plans allow use within own applications and products for commercial purposes.

### Partially verified

- Opening odds on TheStatsAPI: documented as available where captured; not guaranteed for every match, competition, or market.
- Historical odds depth on UK Odds API: competitions are listed but seasons available are not publicly quantified.

### Not documented

- Double Chance on TheStatsAPI: not listed in any documented odds market.
- Most Cards on TheStatsAPI: not listed in any documented odds market.
- Cards Over/Under on TheStatsAPI: not listed in any documented odds market.
- Opening odds on UK Odds API: the provider does not define or document opening prices.
- Match results, goals, cards, and standings on UK Odds API: not a product capability.

### Requires verification

- Opening odds for Double Chance, Most Cards, and Cards Over/Under remain unresolved across both providers.
- UK Odds API commercial/licensing terms beyond plan gating require review.
- TheStatsAPI portfolio/demo use in a public-facing project requires confirmation from the provider.

## 9. Recommendation

### Primary provider

Name: TheStatsAPI

Purpose: core football statistics provider for matches, standings, cards statistics, teams, and historical odds where explicitly documented.

Why selected:

- it is the strongest verified match-data provider in the candidate set
- it provides historical odds with opening and last-seen prices where captured
- it covers the stats layer needed for recent form, standings, and H2H derivation

Coverage:

- fixtures, results, standings, teams, players, match statistics, and odds
- cards as statistics
- historical odds with bookmaker identification and temporal context
- opening and last-seen prices where captured (desirable, not mandatory)

Important limitations:

- Double Chance is not listed in the documented odds markets
- Most Cards and Cards Over/Under are not listed in the documented odds markets
- historical odds availability varies by match, bookmaker, and market
- CSV access was not verified

### Secondary provider

Name: UK Odds API

Purpose: betting-market provider for Double Chance and cards markets that are not explicitly verified on TheStatsAPI.

Why selected:

- it explicitly documents Double Chance and cards market families
- it exposes stable market keys, event markets, and historical odds snapshots
- it is the smallest provider in the reviewed set that closes the betting-market gap most directly

Coverage:

- football events and odds with bookmaker identification and temporal context
- market catalog with Double Chance and cards markets
- historical odds snapshots with capture timestamps (satisfies the historical odds + timestamp requirement)
- batch odds and arbitrage support

Important limitations:

- explicit Opening Odds are not defined by this provider (acceptable: historical odds with timestamp satisfy the MVP requirement)
- historical odds depth by competition is not publicly quantified per season
- match results, goals, cards as event data, and standings are not product capabilities

### Provider selection conclusion

The smallest viable provider combination for the MVP is TheStatsAPI plus UK Odds API.

#### Mandatory MVP requirements

- Historical sports data (matches, results, goals, cards, standings): TheStatsAPI, verified for all five competitions.
- Historical betting odds with bookmaker, market, and temporal context: UK Odds API (Pro plan), verified for all five competitions.
- Required MVP markets (1X2, Double Chance, Goals Over/Under, Most Cards, Cards Over/Under): UK Odds API, market availability verified.
- Sufficient competition coverage (Premier League, La Liga, Bundesliga, Serie A, UEFA Champions League): both providers verified.

#### Optional capabilities

- Explicit Opening Odds: desirable when reliably provided; TheStatsAPI provides opening and last-seen prices where captured. Not a mandatory MVP requirement.
- Explicit Closing Odds: desirable when reliably provided; documented on TheStatsAPI where captured. Not a mandatory MVP requirement.

Opening Odds must never be inferred from the first available historical snapshot unless the provider explicitly defines that behavior.

## 10. Provider Selection Blockers And Limitations

### 10.1 Opening Odds — Closed

Explicit Opening Odds are not a mandatory MVP requirement.

- Historical Odds with bookmaker, market, and timestamp: mandatory.
- Explicit Opening Odds: desirable when reliably provided; not mandatory.
- First historical snapshot must NOT be silently treated as Opening Odds.

### 10.2 UK Odds API Historical Odds Depth — Known Limitation, Not A Blocker

Historical odds depth by competition is not publicly documented per season. This must be confirmed with the provider before production ingestion begins, but it does not prevent the provider selection decision.

### 10.3 TheStatsAPI Licensing — Viable With Restrictions, Not A Blocker

The Betting Analytics official page explicitly documents database backfill as an intended use case and confirms commercial use for analytics tools on all paid plans. The provider is classified as **viable with restrictions**.

Before production ingestion begins, the following should be confirmed with the provider (support@thestatsapi.com):

1. Persistent PostgreSQL archive qualifies as "reasonably necessary" storage under the TOS.
2. Attribution requirements — when and how attribution is required.
3. Cross-provider combination — storing data from both providers in a shared internal database.

These are clarification questions, not evidence of prohibition.

### 10.4 UK Odds API Terms Of Service Not Published — Known Risk, Managed

UK Odds API does not publish a Terms of Service. All data usage rights beyond API access are unverified.

This is a known risk that must be resolved before production ingestion or any redistribution of their data. It does not prevent the provider selection decision because:

- the provider explicitly markets their API to developers building betting products and analytics tools;
- the risk is of an unknown restriction, not evidence of an actual prohibition;
- the project will confirm terms before any data is persisted or redistributed.

The project must contact UK Odds API at ukoddsapi.com/contact before implementation begins.

### 10.5 Cross-Provider Data Combination — Known Risk, Managed

Neither provider explicitly addresses or prohibits combining data from multiple providers. This must be confirmed with both providers before building a combined database. No existing terms prohibit it.

## 11. Provider Strategy Evaluation After Coverage Validation

### Confirmed strengths

- TheStatsAPI provides verified historical match data, results, goals, card statistics, standings, and events for all five MVP competitions over 7–9 seasons.
- H2H is derivable from the historical match data for all five competitions.
- Opening odds and last-seen odds are documented on TheStatsAPI where captured.
- 1X2 and Goals Over/Under are verified on both providers for all five competitions.
- UK Odds API provides Double Chance, Most Cards, and Cards Over/Under in its market catalog.
- UK Odds API supports all five MVP competitions in its coverage list.

### Remaining gaps

- Double Chance historical odds are not listed in TheStatsAPI's documented odds markets; UK Odds API covers the market but historical odds depth is not publicly quantified per competition.
- Most Cards and Cards Over/Under historical odds depth on UK Odds API is not publicly quantified per competition.
- Explicit Opening Odds for any specific market are not guaranteed across all competitions or matches on either provider. This is acceptable under the revised requirement: historical odds with bookmaker, market, and timestamp are mandatory; explicit opening prices are optional.
- Commercial/licensing terms require additional verification for both providers.

### Critical blockers

No critical blocker remains that prevents the provider selection decision from being finalized.

The licensing uncertainties and depth-verification items are pre-implementation requirements, not provider selection blockers.

## 13. Final Provider Responsibility Matrix

| Capability | TheStatsAPI | UK Odds API | MVP Requirement | Final Status |
|---|---|---|---|---|
| Historical matches | Verified (7–9 seasons) | Not covered | Mandatory | Verified via TheStatsAPI |
| Results / goals | Verified | Not covered | Mandatory | Verified via TheStatsAPI |
| Cards (statistics) | Verified | Not covered | Mandatory | Verified via TheStatsAPI |
| Standings / stage info | Verified (domestic); verified per-group (UCL) | Not covered | Mandatory | Verified via TheStatsAPI |
| H2H source data | Verified (match history provides the raw material) | Not covered | Mandatory (derived) | Derivable from TheStatsAPI match history |
| 1X2 | Verified | Verified | Mandatory | Verified via both providers |
| Double Chance | Not documented | Verified | Mandatory | Verified via UK Odds API |
| Goals Over/Under | Verified | Verified | Mandatory | Verified via both providers |
| Most Cards | Not documented | Verified | Mandatory | Verified via UK Odds API |
| Cards Over/Under | Not documented | Verified | Mandatory | Verified via UK Odds API |
| Historical Odds | Partially verified (bookmaker + timestamp + market) | Verified (Pro+) | Mandatory | Covered by both providers in their respective domains |
| Opening Odds | Partially verified (where captured) | Not defined | Optional / desirable | Partially available via TheStatsAPI; not mandatory |
| Closing Odds | Partially verified (where captured) | Not defined | Optional / desirable | Partially available via TheStatsAPI; not mandatory |
| BTTS | Verified | Verified | Secondary / post-MVP | Not required for MVP |

## 14. Final Limitations

The following are known limitations of the selected strategy. They are documented as limitations, not blockers.

1. **Double Chance, Most Cards, and Cards Over/Under historical odds depth on UK Odds API** — market availability is verified; historical depth per competition is not publicly quantified. Must be confirmed before production ingestion.

2. **Opening Odds are not universally available** — TheStatsAPI provides opening and last-seen prices where captured, but availability varies by match, bookmaker, and market. UK Odds API does not define explicit opening prices. This is acceptable under the revised MVP requirement.

3. **UK Odds API Terms of Service not published** — all data usage rights beyond API access are unverified. The project must obtain and review their terms before any data is persisted or redistributed.

4. **TheStatsAPI storage clause** — the "reasonably necessary" language requires confirmation before large-scale historical ingestion begins. The Betting Analytics documentation is strong supportive evidence for the intended use case.

5. **Cross-provider combination** — neither provider explicitly permits or restricts combining their data with another provider's data. Must be confirmed before building a combined database.

6. **Attribution requirements** — TheStatsAPI TOS references attribution without specifying conditions. Must be clarified before public-facing deployment.

7. **UCL structure differs from domestic leagues** — group-stage standings return per-group rows; knockout stages have no standings equivalent. The data model must handle this difference.

## 12. Commercial And Licensing Validation

This section records the results of the commercial and licensing investigation for both provisional providers. Each item previously marked "Requires clarification" or "Not documented" is addressed individually below.

**Evidence sources:**
- TheStatsAPI Terms of Service: thestatsapi.com/terms (last updated April 1, 2026, retrieved 2026-08-09)
- TheStatsAPI Betting Analytics use-case page and FAQ: thestatsapi.com/use-cases/football-betting-analytics-api (retrieved 2026-08-09)
- TheStatsAPI main pricing FAQ: thestatsapi.com/football-api (retrieved 2026-08-09)
- UK Odds API plans and pricing: docs.ukoddsapi.com/getting-started/plans-and-pricing and ukoddsapi.com (retrieved 2026-08-09)
- UK Odds API Terms of Service: ukoddsapi.com/terms — HTTP 404; not publicly available
- UK Odds API Privacy Policy: ukoddsapi.com/privacy — HTTP 404; not publicly available
- UK Odds API FAQ: ukoddsapi.com/faq — HTTP 404; not publicly available
- UK Odds API contact page: ukoddsapi.com/contact — available; no licensing information present

### 12.1 Critical Distinction

API availability ≠ data licensing. A paid subscription grants access to the API. It does not automatically grant rights to store, transform, analyze, or redistribute data. These distinctions are evaluated below using only official documentation.

### 12.2 TheStatsAPI Licensing Analysis

**Source: thestatsapi.com/terms (last updated April 1, 2026) and thestatsapi.com/use-cases/football-betting-analytics-api (retrieved 2026-08-09)**

**Rights grant (TOS):** "a limited, non-exclusive, non-transferable, revocable licence to access and use the data provided through the API within your own applications and products."

#### Resolved items

**Commercial use in analytics and betting tools**

The Betting Analytics FAQ page contains the following official statement:

> "Can I use this data in a commercial betting analytics product? Yes. All plans support commercial use. There are no separate licensing fees for using the data in analytics tools, prediction platforms, or tipster services. Your plan's request limits are the only constraint."

*Source: thestatsapi.com/use-cases/football-betting-analytics-api (official provider FAQ)*

**Resolution:** Commercial use in analytics tools, prediction platforms, and tipster services is explicitly permitted on all paid plans with no additional licensing fees. This resolves the commercial-use uncertainty.

**Database backfill and historical storage intent**

The same official Betting Analytics page contains the following documentation and code example:

> "Use this to backfill your database with historical results. Paginate through all results for a competition to build a comprehensive dataset. This is how you populate your training data. Fetch all matches for a competition across all seasons and you have decades of structured results ready for analysis."

The example code explicitly shows loading data into a pandas DataFrame and building a persistent dataset. The page is titled "Football Stats API for Betting Analytics" and is authored by the provider, not a third party.

*Source: thestatsapi.com/use-cases/football-betting-analytics-api (official provider documentation and code example)*

**Resolution:** The provider explicitly documents and endorses the use case of backfilling a database with historical results for analysis. This is strong evidence that persistent historical storage for analytical purposes is within the intended scope of the licence. However, this page is marketing documentation, not a formal amendment to the TOS. The TOS still contains "Cache or store the data beyond what is reasonably necessary to operate your application." The project should interpret the database backfill documentation as supportive evidence and contact the provider to confirm that a persistent historical archive for internal analytics is within the permitted scope before large-scale ingestion.

**Status: Partially verified — supportive official evidence exists; provider confirmation recommended before production ingestion.**

**Internal use for betting analytics**

TOS explicitly permits use in "internal tools." The Betting Analytics page explicitly targets this use case. No restriction on private internal analytical use is stated.

**Resolution:** Internal use for betting analytics is partially verified as permitted.

**Data transformation and derived statistics**

The TOS grants a licence "to access and use the data... within your own applications and products." The Betting Analytics page describes "build features," "train your model," "calculate closing line value," and "backfill your database with historical results." These all imply data transformation and derived statistics.

**Resolution:** Data transformation and calculation of derived statistics for use within own applications are implied by the documented use cases. Not explicitly restricted. Treating derived statistics as a product of own analysis (not as redistribution of raw data) is consistent with the permitted use described.

**Status: Partially verified — consistent with documented use cases; not explicitly addressed in TOS.**

**Attribution**

TOS states: "Remove, obscure, or misrepresent the source of the data where attribution is required." This implies attribution may be required in some contexts but does not specify when or how.

**Resolution:** Attribution conditions are not explicitly defined in the official documentation. Attribution requirements must be clarified before public-facing deployment.

**Status: Requires provider clarification — conditions not specified.**

**Retention**

TOS does not specify a retention period beyond the storage clause. On subscription termination, the TOS states data access ends immediately but does not require deletion of previously stored data.

**Resolution:** No explicit retention restriction was found. However, the storage clause ambiguity means retention rights are tied to the storage clarification question.

**Status: Requires provider clarification — tied to storage rights clarification.**

**Cross-provider combination**

The TOS does not mention cross-provider data combination. This is not explicitly prohibited and not explicitly permitted.

**Resolution:** Cannot be confirmed from official documentation alone. Must be clarified with the provider.

**Status: Requires provider clarification.**

**Redistribution of raw data**

TOS explicitly prohibits: resell, sublicense, or commercially redistribute the raw data; redistribute or republish the data in bulk as a standalone dataset, feed, or database.

**Resolution:** Raw data redistribution is explicitly restricted. The project must not expose raw provider data through a public application or external feed.

**Status: Restricted — explicit TOS prohibition.**

**Redistribution of derived statistics**

TOS prohibits redistribution of raw data but does not explicitly address derived statistics calculated from the data. The Betting Analytics page describes building analytics products that expose results to users, which is consistent with redistribution of derived statistics being permitted.

**Resolution:** Derived statistics redistribution is partially consistent with documented use cases but not explicitly confirmed in the TOS. Displaying derived outputs (such as recent form or H2H records) through an application is materially different from redistributing raw data and is not explicitly prohibited.

**Status: Partially verified — consistent with documented use cases; not explicitly confirmed in TOS.**

#### Summary — TheStatsAPI unresolved questions

After this review, the following items remain unresolved through official documentation and require direct provider clarification:

1. Persistent historical storage in a PostgreSQL database — supportive evidence exists but TOS clause creates residual ambiguity.
2. Attribution conditions — not specified.
3. Cross-provider data combination — not addressed.
4. Retention after termination — not specified.

These can be resolved in a single email to support@thestatsapi.com before implementation begins.

### 12.3 UK Odds API Licensing Analysis

**Source: ukoddsapi.com and docs.ukoddsapi.com (retrieved 2026-08-09)**

No Terms of Service, Privacy Policy, or FAQ are publicly accessible for UK Odds API. The URLs ukoddsapi.com/terms, ukoddsapi.com/privacy, and ukoddsapi.com/faq all return HTTP 404. The contact page (ukoddsapi.com/contact) contains no licensing information. No data usage policy is embedded in the API documentation or the pricing page.

**All data usage and licensing questions for UK Odds API remain unresolved due to the absence of published terms.** The marketing targets developers building "betting products," "arbitrage tools," and "value bet detectors," but marketing intent does not constitute a legal data usage grant.

The following items cannot be resolved without contacting the provider directly:

- Persistent storage of historical odds in own database
- Caching and retention
- Data transformation and normalized storage
- Derived statistics (implied probabilities, market comparisons, relationships between odds and outcomes)
- Cross-provider data combination
- Internal vs public vs commercial use distinctions
- Raw odds redistribution restrictions
- Derived statistics redistribution
- Attribution requirements
- Retention period

**UK Odds API must be contacted directly to obtain their data usage terms before any persistent storage or analytical processing of their data begins.**

The contact address is available at ukoddsapi.com/contact.

### 12.4 Storage Model Evaluation

The intended workflow is:

```
Provider API
    ↓
Historical raw/normalized data
    ↓
PostgreSQL database (persistent)
    ↓
Derived statistics
    ↓
Analytics application
```

**TheStatsAPI:** The official Betting Analytics documentation explicitly describes and demonstrates backfilling a database with historical results. This is strong supportive evidence that the storage model is within the intended scope. The TOS storage clause creates residual ambiguity that should be resolved with the provider before production ingestion, but this is no longer considered a critical blocker given the explicit official documentation.

**UK Odds API:** No storage terms are published. Persistent storage rights are unknown and cannot be assumed. This remains an unresolved item that requires direct provider contact.

### 12.5 Use Case Classification

| Use case | TheStatsAPI | UK Odds API |
|---|---|---|
| Internal / private analytics | Partially verified (internal tools explicitly permitted; betting analytics documented as use case) | Requires provider clarification |
| Public application | Partially verified (own end-user-facing applications explicitly permitted; raw data redistribution prohibited) | Requires provider clarification |
| Commercial application | Verified for analytics/prediction/tipster tools on paid plans (explicit FAQ statement) | Requires provider clarification |

**Note:** For TheStatsAPI, "commercial" specifically means use in analytics tools, prediction platforms, and tipster services. Commercial redistribution of raw data remains prohibited.

### 12.6 Licensing Matrix

| Requirement | TheStatsAPI | UK Odds API | Status | Evidence / Notes |
|---|---|---|---|---|
| API access | Verified (paid plans) | Verified (paid plans) | Verified | TOS; UK Odds API pricing page |
| Historical data access | Verified (all plans) | Verified (Pro+ only) | Verified | TOS + pricing FAQ; UK Odds API plans page |
| Persistent storage / database backfill | Partially verified | Not documented | Partially verified / Requires provider clarification | TheStatsAPI Betting Analytics page explicitly documents database backfill as the intended workflow. TOS storage clause creates residual ambiguity. UK Odds API: no terms. |
| Caching | Partially verified (limited) | Not documented | Requires provider clarification | TOS: "reasonably necessary." Persistent archive exceeds typical cache semantics. UK Odds API: no terms. |
| Data transformation | Partially verified | Not documented | Partially verified / Requires provider clarification | TheStatsAPI use cases imply transformation; not explicitly addressed in TOS. UK Odds API: no terms. |
| Derived statistics | Partially verified | Not documented | Partially verified / Requires provider clarification | TheStatsAPI Betting Analytics page describes building models and derived outputs. Not explicitly confirmed in TOS. UK Odds API: no terms. |
| H2H calculations | Partially verified | Not documented | Partially verified / Requires provider clarification | H2H as a derived project statistic is consistent with the documented analytics use case. UK Odds API: no terms. |
| Odds analysis | Partially verified | Not documented | Partially verified / Requires provider clarification | TheStatsAPI documents odds use for CLV, model validation, and analytics. UK Odds API: no terms. |
| Cross-provider combination | Not documented | Not documented | Requires provider clarification | Neither provider explicitly addresses or restricts this. Cannot be confirmed without provider contact. |
| Internal use | Partially verified | Not documented | Partially verified / Requires provider clarification | TOS permits internal tools. Betting analytics explicitly documented as use case. UK Odds API: no terms. |
| Commercial use | Verified (analytics/prediction on paid plans) | Not documented | Partially verified | TheStatsAPI FAQ explicitly confirms commercial use for analytics, prediction, tipster services. UK Odds API: no formal terms. |
| Redistribution of raw data | Restricted | Not documented | Restricted / Requires provider clarification | TheStatsAPI TOS explicitly prohibits bulk redistribution. UK Odds API: no terms. |
| Redistribution of derived statistics | Partially verified | Not documented | Partially verified / Requires provider clarification | TheStatsAPI use cases imply end-user-facing derived outputs are permitted; TOS does not explicitly address. UK Odds API: no terms. |
| Attribution | Requires provider clarification | Not documented | Requires provider clarification | TheStatsAPI TOS references attribution "where required" without specifying conditions. UK Odds API: no terms. |
| Rate limits / quotas | Verified | Verified | Verified | TheStatsAPI: Starter 100K/month, 120/min. UK Odds API Pro: 5K/hour. Sufficient for batch historical ingestion if managed carefully. |
| Retention restrictions | Requires provider clarification | Not documented | Requires provider clarification | TheStatsAPI: no explicit retention period. TOS storage clause applies. UK Odds API: no terms. |

### 12.7 MVP Decision

**Classification: Viable with restrictions — requires provider clarification before implementation**

**TheStatsAPI:** The provider explicitly documents and supports the project's intended use case: database backfill, historical analytics, betting model construction, and commercial analytics tools. Commercial use on paid plans is explicitly confirmed. The TOS storage clause creates residual ambiguity that should be resolved before production ingestion, but the official Betting Analytics documentation provides strong supportive evidence. The remaining unresolved items (storage confirmation, attribution, cross-provider combination) can be resolved with a single provider contact. TheStatsAPI is viable for the MVP subject to confirming these points.

**UK Odds API:** No Terms of Service are published. All data usage rights beyond API access are unverified. The provider cannot be classified as viable until terms are obtained. The project must contact UK Odds API before any persistent storage or analytical processing of their data begins.

**Overall provider strategy decision:** TheStatsAPI + UK Odds API remains viable as a provider strategy. The technical requirements are satisfied. The remaining licensing uncertainties are resolvable by contacting both providers directly. The strategy is viable with restrictions — not blocked — because the unresolved items are clarification questions, not evidence of prohibition.

The following questions must be addressed with each provider before implementation:

**For TheStatsAPI (contact: support@thestatsapi.com):**
1. Confirm that building a persistent PostgreSQL database of historical match data for internal analytics constitutes "reasonably necessary" storage under the TOS.
2. Confirm attribution requirements and when they apply.
3. Confirm whether combining TheStatsAPI data with data from UK Odds API in a shared internal database is permitted.

**For UK Odds API (contact: ukoddsapi.com/contact):**
1. Request published Terms of Service or data usage policy.
2. Confirm permission to persistently store historical odds in an internal PostgreSQL database.
3. Confirm whether redistribution of derived statistics (not raw odds) through a private analytics application is permitted.
4. Confirm attribution requirements.

## 15. Documentation Synchronization Checklist

The following files must be synchronized after this branch is merged:

- README.md: update the project status, add the selected providers, and advance the roadmap.
- docs/project-status.md: mark Provider Selection as Completed and set next phase to Data Model.
- CHANGELOG.md: record the provider selection decision.
- docs/decision-log.md: copy the final provider decision record from §16.

No synchronization changes are applied in this task.

## 16. Final Provider Decision Record

### Provider strategy

Primary provider: TheStatsAPI

Secondary provider: UK Odds API

### Division of responsibilities

TheStatsAPI is responsible for the entire sports and statistical data layer:

- historical football matches, results, goals, cards, and match statistics
- standings (domestic leagues and group-stage tables for the Champions League)
- H2H source data (historical match records from which H2H is derived internally)
- historical odds with bookmaker and temporal context for 1X2, Goals Over/Under, and other markets documented by the provider
- optional opening and last-seen odds where captured

UK Odds API is responsible for the betting-market layer that TheStatsAPI does not cover:

- historical odds for Double Chance, Most Cards, and Cards Over/Under
- market catalog with stable market keys
- bookmaker identification and capture timestamps

### Decision

Completed

### Reason

All mandatory MVP technical requirements are satisfied or verified by the two-provider combination. The five MVP competitions are confirmed in both providers. The five required betting markets are covered across the two providers. Historical odds with bookmaker, market, and temporal context are available. H2H is derivable from the historical match data. Opening Odds are explicitly treated as optional. Licensing constraints are documented; they are pre-implementation requirements, not selection blockers. The provider strategy is defensible from both technical and commercial standpoints.

### Known restrictions that must be resolved before implementation

1. Obtain UK Odds API data usage terms before any persistent storage or redistribution of their data.
2. Confirm TheStatsAPI storage rights for a persistent historical archive before large-scale ingestion.
3. Confirm cross-provider data combination with both providers.
4. Confirm attribution requirements with both providers.
5. Confirm UK Odds API historical odds depth per competition before implementation.

### Revisit conditions

- if either provider's terms prohibit the intended storage or analytical use
- if UK Odds API historical depth is insufficient for the MVP historical analysis window
- if cross-provider combination is explicitly restricted by either provider

### Next phase

Data Model

The Data Model phase will define:

- entities and relationships
- provider and source identifiers
- match, competition, and season representation
- bookmaker and market representation
- historical odds representation including bookmaker, market, and timestamp
- source-to-internal mapping and provenance tracking

Status: Completed

Phase: Provider Selection

Next Step: Data Model
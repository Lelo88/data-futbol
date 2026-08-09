# Source Research

## 1. Purpose

This document records the research performed to identify external data sources that may satisfy the requirements defined in [data-definition.md](data-definition.md).

It separates verified capabilities from partially verified capabilities and unknown or unverified capabilities so that source selection can be handled in a later phase.

The research below is based on the current official source documentation and public site content available at the time of writing.

## 2. Research Classification

- Verified: the source documentation explicitly states the capability.
- Partially verified: the source documentation suggests the capability, but the exact semantics, coverage, or completeness are not fully confirmed.
- Unknown/unverified: the source documentation does not clearly confirm the capability.

## 3. Source Research

### 3.1 Football-Data.co.uk

#### Source overview

Football-Data.co.uk is a free football betting portal that provides historical results and odds. The site emphasizes computer-ready data for quantitative analysis and explicitly references Excel and CSV downloads.

#### Data formats

- Verified: Excel and CSV downloads.
- Partially verified: the site also presents historical data and betting articles, but no structured API documentation was verified in the available source material.

#### Historical depth

- Partially verified: the site states that it provides historical results and odds across many years, but the exact depth varies by league and was not fully quantified in the available documentation.

#### Competition coverage

- Partially verified: the site exposes main leagues and extra leagues, plus an archive of historical data. The exact competition list varies by area of the site and was not normalized in the available documentation.

#### Match/result data

- Verified: historical results are explicitly provided.

#### Match statistics

- Partially verified: the site references match statistics, but the currently reviewed documentation does not enumerate the full set of statistical fields required by the project.

#### Standings

- Unknown/unverified: standings were not explicitly confirmed in the reviewed documentation.

#### H2H availability

- Unknown/unverified: head-to-head data was not explicitly confirmed in the reviewed documentation.

#### Betting markets

- Verified: historical odds are available.
- Partially verified: the site explicitly references opening odds alerts and closing odds bet tracker content, but the exact data semantics for per-record market availability were not fully confirmed.

#### Opening odds availability and exact semantics

- Partially verified: opening odds are explicitly referenced, but the exact source semantics, row-level representation, and whether the data is bookmaker-specific or aggregated were not fully verified from the available documentation.

#### Closing odds availability

- Partially verified: closing odds are explicitly referenced, but the exact representation in the downloadable data was not verified.

#### Cards markets

- Unknown/unverified: cards markets were not explicitly confirmed in the reviewed documentation.

#### API/CSV access

- Verified: CSV and Excel access are explicitly documented.
- Unknown/unverified: an official structured API was not verified in the reviewed material.

#### Pricing

- Verified: the data archive is described as free.

#### Usage limits

- Unknown/unverified: usage limits for the historical data archive were not verified in the reviewed documentation.

#### Licensing/commercial-use considerations

- Unknown/unverified: commercial-use terms for the free archive were not clearly verified in the reviewed documentation.

#### Python integration considerations

- Verified: CSV and Excel downloads can be consumed directly from Python tooling such as pandas.
- Unknown/unverified: no official Python SDK was verified.

#### Known limitations

- No official structured API was verified from the reviewed documentation.
- Exact historical depth and competition-by-competition coverage vary and were not fully normalized.
- Standings, H2H, and card-specific market availability remain unverified.

#### Capability classification

- Verified capabilities
  - Historical results and odds archive.
  - Excel and CSV downloads.
  - Free access to the archive.
- Partially verified capabilities
  - Opening odds tracking.
  - Closing odds references.
  - Historical depth across many years.
  - Coverage across main and extra leagues.
- Unknown/unverified capabilities
  - Standings.
  - H2H.
  - Cards markets.
  - Official API access.
  - Usage limits.
  - Commercial-use terms.

### 3.2 TheStatsAPI

#### Source overview

TheStatsAPI is a football stats API that provides competitions, teams, matches, standings, player statistics, match statistics, and odds.

#### Data formats

- Verified: JSON REST API.
- Verified: official Python SDK.
- Unknown/unverified: CSV access was not verified in the reviewed documentation.

#### Historical depth

- Verified: the service states that it includes 10 years of historical match data.
- Partially verified: player and team stats are described as available per season with full historical depth, but exact historical depth by dataset was not separately normalized.

#### Competition coverage

- Verified: 150 competitions across 100+ countries are documented by default, with up to 1,196 available on request.

#### Match/result data

- Verified: match schedules and historical results are documented.
- Verified: live and finalized match stats are available for supported fixtures.

#### Match statistics

- Verified: match stats include cards, goals, shots, xG, possession, passes, and minute-by-minute events.

#### Standings

- Verified: standings endpoints are documented.

#### H2H availability

- Unknown/unverified: H2H support was not explicitly confirmed in the reviewed documentation.

#### Betting markets

- Verified: odds data is documented.
- Partially verified: the odds documentation explicitly mentions 1X2, Asian handicap, totals, BTTS, draw no bet, and corners.

#### Opening odds availability and exact semantics

- Partially verified: opening and closing lines are referenced in the odds documentation, but the exact semantics of opening odds per bookmaker versus aggregated values were not verified.

#### Closing odds availability

- Verified: closing lines are explicitly referenced.

#### Cards markets

- Partially verified: cards are available as match statistics, but cards-specific betting markets were not verified in the reviewed documentation.

#### API/CSV access

- Verified: REST JSON API access is documented.
- Verified: official Python SDK is available.
- Unknown/unverified: CSV access was not verified.

#### Pricing

- Verified: pricing plans are documented, starting at $50/month.

#### Usage limits

- Verified: request limits are documented, including 100,000 requests/month and 120 requests/minute on the Starter plan.

#### Licensing/commercial-use considerations

- Unknown/unverified: commercial-use terms were not clearly verified in the reviewed documentation.

#### Python integration considerations

- Verified: the service provides an official Python SDK and Python code snippets.

#### Known limitations

- H2H was not verified in the reviewed documentation.
- CSV access was not verified.
- Cards-specific betting markets were not explicitly documented.
- Live features are present in the product, but the project does not intend to use live data in the MVP.

#### Capability classification

- Verified capabilities
  - JSON REST API.
  - Official Python SDK.
  - Match results and match statistics.
  - Standings.
  - Odds endpoints.
  - 10 years of historical match data.
- Partially verified capabilities
  - Opening and closing lines.
  - Odds markets listed in documentation.
  - Per-season historical depth for player/team stats.
  - Cards as match statistics rather than betting markets.
- Unknown/unverified capabilities
  - H2H.
  - CSV access.
  - Commercial-use terms.

### 3.3 Football-Bet-Data

#### Source overview

Football-Bet-Data is a football statistics, odds, and historical bet data platform focused on leagues, fixtures/results, H2H, and betting analysis tools.

#### Data formats

- Verified: Excel file exports.
- Unknown/unverified: CSV access was not clearly verified in the reviewed documentation.

#### Historical depth

- Verified: the platform states that it covers 65+ leagues dating back to 1998.

#### Competition coverage

- Verified: 65+ leagues are documented, including the Premier League, Bundesliga, Ligue 1, and Serie A.

#### Match/result data

- Verified: fixtures and results are explicitly referenced.

#### Match statistics

- Unknown/unverified: the reviewed documentation does not clearly enumerate the match statistics required by the project.

#### Standings

- Unknown/unverified: standings were not explicitly confirmed in the reviewed documentation.

#### H2H availability

- Verified: head-to-head features are explicitly referenced.

#### Betting markets

- Verified: the platform explicitly references average bookmaker odds and Betfair Exchange odds.
- Verified: the documented markets include Home Win, Away Win, Draw, Both Teams to Score, Double Chance, Over/Under, and Correct Score.

#### Opening odds availability and exact semantics

- Unknown/unverified: the reviewed documentation does not clearly define opening odds semantics.

#### Closing odds availability

- Unknown/unverified: closing odds availability was not explicitly verified in the reviewed documentation.

#### Cards markets

- Unknown/unverified: cards-specific betting markets were not explicitly confirmed in the reviewed documentation.

#### API/CSV access

- Verified: Excel file access and export are documented.
- Unknown/unverified: a public API or CSV download flow was not clearly verified.

#### Pricing

- Partially verified: the platform offers a free basic membership with an upgrade path, but the reviewed documentation does not fully specify pricing tiers.

#### Usage limits

- Unknown/unverified: usage limits were not clearly verified in the reviewed documentation.

#### Licensing/commercial-use considerations

- Unknown/unverified: commercial-use terms were not clearly verified in the reviewed documentation.

#### Python integration considerations

- Partially verified: Excel exports can be consumed from Python, but no official Python SDK or API integration details were verified.

#### Known limitations

- The reviewed documentation emphasizes betting analysis and predictions, which are outside the project MVP.
- Exact market semantics, opening odds semantics, and source export details were not fully verified.
- Standings and detailed match statistics remain unconfirmed.

#### Capability classification

- Verified capabilities
  - Historical coverage since 1998 across 65+ leagues.
  - Fixtures/results.
  - Head-to-head features.
  - Betting markets for 1X2-style outcomes, BTTS, Double Chance, Over/Under, and Correct Score.
  - Excel exports.
- Partially verified capabilities
  - Free basic membership with upgrade path.
  - Consumption of Excel exports from Python workflows.
- Unknown/unverified capabilities
  - Standings.
  - Match statistics.
  - Opening odds semantics.
  - Closing odds availability.
  - Cards markets.
  - CSV access.
  - Usage limits.
  - Commercial-use terms.

### 3.4 Odds-API.io

#### Source overview

Odds-API.io is a sports betting odds API focused on real-time odds, scores, player props, and bookmaker coverage across many sportsbooks.

#### Data formats

- Verified: REST JSON API.
- Verified: WebSocket streaming.
- Verified: official Python SDK.

#### Historical depth

- Partially verified: the site states that it offers historical odds, but the exact historical depth was not verified in the reviewed documentation.

#### Competition coverage

- Verified: 34 sports and 12,000+ leagues are documented.
- Partially verified: football coverage is documented through the football event examples and football-specific API usage.

#### Match/result data

- Unknown/unverified: historical match result coverage was not verified as a primary product capability.

#### Match statistics

- Unknown/unverified: match statistics for goals, cards, or related stat feeds were not clearly verified as required by the project.

#### Standings

- Unknown/unverified: standings were not verified.

#### H2H availability

- Unknown/unverified: H2H was not verified.

#### Betting markets

- Verified: live odds and pre-match odds are documented.
- Verified: the service documents 100+ markets.
- Partially verified: player props and event-level betting data are documented.
- Partially verified: over/under and BTTS are referenced in the available product copy.

#### Opening odds availability and exact semantics

- Unknown/unverified: opening odds semantics were not clearly verified in the reviewed documentation.

#### Closing odds availability

- Unknown/unverified: closing odds availability was not clearly verified in the reviewed documentation.

#### Cards markets

- Unknown/unverified: cards-specific betting markets were not explicitly verified.

#### API/CSV access

- Verified: REST JSON API and WebSocket streaming are documented.
- Unknown/unverified: CSV access was not verified.

#### Pricing

- Verified: free and paid plans are documented.

#### Usage limits

- Verified: the free tier and paid tiers document request limits, including 100 requests/hour on the free plan and 5,000 requests/hour on paid REST plans.

#### Licensing/commercial-use considerations

- Unknown/unverified: commercial-use terms were not clearly verified in the reviewed documentation.

#### Python integration considerations

- Verified: an official Python SDK is documented.

#### Known limitations

- The product is primarily oriented toward real-time odds rather than historical football statistics.
- Historical depth is mentioned but not fully quantified in the reviewed documentation.
- Standings, H2H, and detailed match-statistic feeds were not verified.

#### Capability classification

- Verified capabilities
  - REST JSON API.
  - WebSocket streaming.
  - Official Python SDK.
  - Live and pre-match odds.
  - Large bookmaker and league coverage.
- Partially verified capabilities
  - Historical odds.
  - 100+ markets.
  - Football event coverage.
  - Over/under and BTTS references.
- Unknown/unverified capabilities
  - Results.
  - Goals.
  - Yellow cards.
  - Red cards.
  - Standings.
  - H2H.
  - Opening odds semantics.
  - Closing odds semantics.
  - Cards-specific betting markets.
  - CSV access.
  - Commercial-use terms.

### 3.5 UK Odds API

#### Source overview

UK Odds API is a UK-focused odds API that provides normalized odds from major UK bookmakers through a documented API.

#### Data formats

- Verified: REST JSON API.
- Verified: OpenAPI documentation and API playground.

#### Historical depth

- Partially verified: the product documents historical odds, but the exact historical depth was not verified in the reviewed documentation.

#### Competition coverage

- Verified: league and country coverage are explicitly documented.
- Partially verified: the product emphasizes UK football coverage and a rolling seven-day fixture window.

#### Match/result data

- Unknown/unverified: historical match result data was not verified.

#### Match statistics

- Unknown/unverified: goals, cards, and other match statistics were not verified.

#### Standings

- Unknown/unverified: standings were not verified.

#### H2H availability

- Unknown/unverified: H2H was not verified.

#### Betting markets

- Verified: the product explicitly documents all football markets.
- Partially verified: the product specifically highlights match winner, both teams to score, over/under, cards, correct score, and player props.
- Partially verified: arbitrage comparison is documented.

#### Opening odds availability and exact semantics

- Unknown/unverified: opening odds semantics were not clearly verified in the reviewed documentation.

#### Closing odds availability

- Unknown/unverified: closing odds availability was not clearly verified in the reviewed documentation.

#### Cards markets

- Partially verified: cards are explicitly documented as a market category, but the exact mapping to Most Cards versus Cards Over/Under was not fully verified.

#### API/CSV access

- Verified: documented REST API, API reference, and OpenAPI support.
- Unknown/unverified: CSV access was not verified.

#### Pricing

- Verified: free and paid plans are documented.

#### Usage limits

- Verified: request limits are documented, including 300 requests/month on the free plan, 1,000 requests/hour on Starter, 5,000 requests/hour on Pro, and 20,000 requests/hour on Business.

#### Licensing/commercial-use considerations

- Unknown/unverified: commercial-use terms were not clearly verified in the reviewed documentation.

#### Python integration considerations

- Partially verified: the API is documented and OpenAPI support is available, but no official Python SDK was verified.

#### Known limitations

- The service is UK-focused rather than a broad global football statistics archive.
- Historical depth is mentioned but not quantified in the reviewed documentation.
- Results, standings, and H2H were not verified as available product capabilities.

#### Capability classification

- Verified capabilities
  - REST JSON API.
  - OpenAPI and API playground.
  - Documented market coverage.
  - Documented pricing and usage limits.
- Partially verified capabilities
  - Historical odds.
  - Match winner / BTTS / over-under / cards / correct score / player props markets.
  - Arbitrage endpoint.
  - UK football coverage and rolling fixture window.
- Unknown/unverified capabilities
  - Results.
  - Goals.
  - Yellow cards.
  - Red cards.
  - Standings.
  - H2H.
  - Opening odds semantics.
  - Closing odds semantics.
  - CSV access.
  - Commercial-use terms.

## 4. Comparison Matrix

| Data Requirement | Football-Data.co.uk | TheStatsAPI | Football-Bet-Data | Odds-API.io | UK Odds API |
|---|---|---|---|---|---|
| Results | Verified | Verified | Verified | Not available | Not available |
| Goals | Verified | Verified | Verified | Not available | Not available |
| Yellow cards | Unknown | Verified | Unknown | Not available | Not available |
| Red cards | Unknown | Verified | Unknown | Not available | Not available |
| Standings | Unknown | Verified | Unknown | Not available | Not available |
| H2H | Unknown | Unknown | Verified | Not available | Not available |
| Recent form inputs | Verified | Verified | Verified | Not available | Not available |
| 1X2 odds | Verified | Verified | Verified | Verified | Partially verified |
| Double Chance odds | Unknown | Unknown | Verified | Unknown | Unknown |
| Goals Over/Under odds | Unknown | Verified | Verified | Partially verified | Partially verified |
| Most Cards odds | Unknown | Unknown | Unknown | Unknown | Partially verified |
| Cards Over/Under odds | Unknown | Unknown | Unknown | Unknown | Partially verified |
| Opening odds | Partially verified | Partially verified | Unknown | Unknown | Unknown |
| Historical depth | Partially verified | Verified | Verified | Partially verified | Partially verified |

## 5. Open Questions

- Which source, if any, provides verified H2H coverage that is compatible with the MVP data model?
- Which source, if any, provides verified yellow and red card data at the level required by the project outside TheStatsAPI?
- Which source provides verified Double Chance odds with clearly documented semantics?
- Which source provides verified Most Cards and Cards Over/Under odds with clearly documented semantics?
- Which source provides opening odds with semantics that can be reliably distinguished from closing or snapshot odds?
- Which source provides the best historical depth for the required markets without introducing live-data requirements?
- Which source offers the clearest licensing terms for the project’s intended use?
- Which source offers the simplest Python integration for source-specific normalization?

## 6. Next Step

Source Mapping and Provider Selection.

Status: Completed

Phase: Source Research
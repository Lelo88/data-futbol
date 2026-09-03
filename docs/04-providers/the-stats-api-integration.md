# TheStatsAPI Integration Contract

## 1. Objective

Define the technical boundary for consuming TheStatsAPI as Data-Futbol's primary historical football-statistics provider. This is a design contract for the future implementation; it does not add an HTTP client, ingestion job, scheduler, or schema change.

## 2. Scope

The first implementation is limited to the approved MVP competitions: Premier League, La Liga, Bundesliga, Serie A, and UEFA Champions League. It must support the source data needed to persist competitions, seasons, teams, matches, match events, match statistics used by the approved model, and standings.

TheStatsAPI is not the source of truth for the MVP's Double Chance, Most Cards, or Cards Over/Under markets. UK Odds API remains the secondary odds provider for those markets. TheStatsAPI odds, if later consumed, are optional provider data: an opening price is persisted only when the provider explicitly identifies it as such.

Out of scope: HTTP implementation, automated ingestion, retries in code, scheduling, scraping, analytics, H2H endpoints, UK Odds API implementation, and changes to the approved data model.

## 3. Provider Responsibility

TheStatsAPI is responsible for external football data. Based on the repository's provider-selection evidence, it is the primary source for historical fixtures/results, goals, cards, events, match statistics, teams, and standings for the approved competitions. H2H is calculated later from persisted matches; it is not a provider operation.

The adapter must not expose HTTP response shapes, JSON field names, provider identifiers, or authentication details to domain or persistence code.

## 4. Proposed Architecture

```text
TheStatsAPI HTTP response
        |
        v
TheStatsAPI client (transport, auth, pagination, error translation)
        |
        v
Provider DTOs (external, validated response representations)
        |
        v
TheStatsAPI mapper (normalization and domain commands)
        |
        v
Ingestion application service (transaction orchestration and reconciliation)
        |
        v
SQLAlchemy repositories / persistence models
        |
        v
PostgreSQL
```

The future package layout should preserve these boundaries, for example:

```text
src/data_futbol/
  providers/
    ports.py
    the_stats_api/
      client.py
      dtos.py
      mapper.py
      errors.py
      config.py
  ingestion/
    services.py
  persistence/
    repositories.py
```

Names are illustrative; the implementation must keep provider DTOs out of `persistence.models` and must keep SQLAlchemy models out of the provider adapter.

## 5. Provider Port

The application-facing port should contain only the operations needed for the MVP. Each operation returns provider DTOs, not SQLAlchemy entities:

```python
class FootballStatisticsProvider(Protocol):
    def list_competitions(self) -> Iterable[CompetitionDTO]: ...
    def list_seasons(self, competition_external_id: str) -> Iterable[SeasonDTO]: ...
    def list_teams(self, competition_external_id: str, season_external_id: str) -> Iterable[TeamDTO]: ...
    def list_matches(self, competition_external_id: str, season_external_id: str) -> Iterable[MatchDTO]: ...
    def get_match_events(self, match_external_id: str) -> Iterable[MatchEventDTO]: ...
    def get_match_statistics(self, match_external_id: str) -> MatchStatisticsDTO: ...
    def get_standings(self, competition_external_id: str, season_external_id: str) -> Iterable[StandingDTO]: ...
```

This is a conceptual contract, not executable code. Concrete method names, required identifiers, and whether data arrives through list or detail calls must be reconciled with official API documentation before implementation. Odds do not belong in this initial port unless the implementation task explicitly includes a documented TheStatsAPI odds contract.

## 6. DTO Strategy

DTOs are provider-owned immutable representations of validated external payloads. Each retains the provider `external_id`, source values needed for mapping, and optional raw metadata useful for diagnostics. They do not contain database sessions, internal IDs, or ORM relationships.

The initial DTO set is `CompetitionDTO`, `SeasonDTO`, `TeamDTO`, `MatchDTO`, `MatchEventDTO`, `MatchStatisticsDTO`, and `StandingDTO`. Fields, field names, nullability, pagination envelope, and date formats must be derived only from official response examples or schemas. Unknown or malformed required fields result in an invalid-response error before mapping.

## 7. Mapping Strategy

The mapper has one-way responsibility:

```text
TheStatsAPI DTO -> normalized domain command/value -> repository operation -> persistence model
```

It normalizes provider values into the approved domain vocabulary: competition type, UTC match datetime, match status, regular-time score, extra time/penalty fields, event type, and standing source. It must reject unsupported or ambiguous values rather than silently guessing.

The mapper does not perform HTTP calls. The client does not write to the database. The ingestion application service resolves dependencies in order (competition, season, teams, match, events/statistics, standings), invokes repositories, and owns the transaction boundary.

`MatchStatisticsDTO` must only map information represented by the approved schema or explicitly requested by a future model change. Match-level goals and supported events are persisted; additional statistics such as xG, possession, shots, or passes must not be discarded into invented columns or trigger a schema change in this task.

## 8. External-ID Strategy

`providers` supplies the internal `provider_id` for the seeded `TheStatsAPI` record. Provider identifiers always remain strings at the boundary, even when their external representation is numeric.

For every supported entity, `provider_mappings` records:

```text
provider_id + entity_type + external_id <-> internal entity ID (stored as text)
```

Supported mapping entity types are the existing enum values: competition, season, team, match, bookmaker, market, and selection. This initial statistics ingestion uses competition, season, team, and match. A mapping is created only after the repository has resolved or created the corresponding internal entity and validated that the entity type matches its internal table.

Resolution starts with reverse lookup on `(provider_id, entity_type, external_id)`. If present, its internal ID is authoritative for this provider import. If absent, the ingestion service may reconcile to an existing canonical entity using documented, deterministic rules; otherwise it creates the internal entity and mapping in the same transaction. A conflicting mapping is a reconciliation/mapping error and must never be overwritten by a name match.

The existing unique constraints on `(provider_id, entity_type, internal_id)` and `(provider_id, entity_type, external_id)` prevent one provider from assigning competing IDs. They are not a substitute for application validation of the polymorphic `internal_id`.

## 9. Configuration

The future adapter reads its settings from environment variables, never source control:

| Variable | Required | Meaning |
|---|---:|---|
| `THE_STATS_API_KEY` | yes for live calls | Provider credential; never logged. |
| `THE_STATS_API_BASE_URL` | yes for live calls | Base URL, verified from provider documentation. |
| `THE_STATS_API_TIMEOUT_SECONDS` | no | Per-request timeout; default to be set in implementation. |
| `THE_STATS_API_MAX_RETRIES` | no | Retry cap for recoverable requests; default to be set in implementation. |

Configuration validation must fail fast with a clear local configuration error if a live client is constructed without required values. `.env` remains ignored; `.env.example` contains placeholders only.

## 10. Authentication

The repository does not document TheStatsAPI's concrete authentication scheme, header name, query parameter, or credential format. The client implementation must verify these against official documentation before sending any request. It must redact credentials from logs, exception messages, test snapshots, and telemetry.

## 11. Error Handling

Use a small provider error hierarchy carrying a safe message, optional HTTP status, provider request/correlation ID when available, and a `retryable` classification:

| Error | Retryable | Meaning |
|---|---:|---|
| `ProviderAuthenticationError` | no | Missing/invalid credential or authentication failure. |
| `ProviderAuthorizationError` | no | Credential lacks product/endpoint permission. |
| `ProviderRateLimitError` | yes | Quota or throttling response; honor documented retry advice. |
| `ProviderTimeoutError` | yes | Client timeout. |
| `ProviderNetworkError` | yes | DNS, connection, or transport failure. |
| `ProviderHTTPError` | depends | Unexpected HTTP status; only transient server statuses are retry candidates. |
| `ProviderInvalidResponseError` | no | Invalid JSON, invalid envelope, or missing/invalid required data. |
| `ProviderMappingError` | no | Valid DTO cannot be unambiguously represented in the approved domain. |

The ingestion service can retry recoverable provider errors outside a database transaction. Mapping and persistence errors stop the affected unit of work and retain enough non-secret context to diagnose it.

## 12. HTTP, Retry, Pagination, and Logging Policy

The implementation must use an explicit connect/read timeout; its value is pending provider and operational verification. Retry only idempotent read requests after network failures, timeouts, rate limits, and transient server responses. Use bounded exponential backoff with jitter, honor `Retry-After` only if documented/present, and do not retry authentication, authorization, validation, or most 4xx errors.

Status-code semantics, provider rate-limit headers, pagination mechanism, maximum page size, and partial-response guarantees are not documented in this repository. They must be verified before code selects a policy. The client must fetch all pages before declaring a listing complete; if pagination cannot be completed, it raises a recoverable provider error and the ingestion service must not mark that source scope as complete.

Minimum structured logs: provider name, operation, safe external scope IDs, page/cursor when known, elapsed time, result count, retry attempt, and redacted error class/status. Never log API keys or complete payloads by default. Incomplete required data must raise `ProviderInvalidResponseError`; optional fields may be absent only where the DTO contract permits it.

## 13. Idempotency and Persistence

Repeated imports must converge on one canonical record per external identity:

1. Resolve the provider mapping by external ID.
2. Create or update the domain row using its approved natural/unique key only when reconciliation is unambiguous.
3. Insert the provider mapping atomically with a newly resolved entity.
4. Upsert mutable source fields through repositories without creating duplicate mappings.

The database's provider-mapping unique constraints are the identity guard. Repositories should use PostgreSQL conflict-safe insert/upsert patterns and re-read the mapping on a uniqueness race. A single match import and its mapping changes belong in one transaction; a failed event/statistics/standing unit rolls back its own changes rather than persisting a partial unit.

`match_events` currently has no provider event external-ID mapping type. The first implementation must not claim event-level replay idempotency without a documented stable event identity and an approved model extension. Until then, event replacement/upsert semantics require an explicit follow-up design. This is a real limitation, not a reason to overload match IDs. Similarly, only provider-labelled odds may be stored as `opening` or `closing`; first-observed snapshots remain `snapshot`.

## 14. Testing Strategy

Unit tests (with fixtures and mocked transport, no real credentials) should cover request construction once verified, response parsing, DTO validation, pagination traversal, retry classification/backoff decisions, error translation, UTC/date normalization, status/event mapping, and mapping failures.

Integration tests against an isolated PostgreSQL database should cover provider DTOs through repositories: creation and reverse lookup of provider mappings, repeat import/upsert idempotency, unique-conflict reconciliation, transaction rollback, match dependency ordering, and persistence constraints. Existing data-model tests remain unchanged. Contract fixtures must be sanitized and derived from official examples or recorded authorized responses.

The standard test suite must remain runnable without `THE_STATS_API_KEY`; live-provider tests, if ever added, must be opt-in and excluded by default.

## 15. Information Pending Verification

Before implementation, verify against the official TheStatsAPI documentation and account/plan:

- Exact base URL, authentication mechanism, credential placement, and required headers.
- Endpoint paths, request parameters, response envelopes, identifier formats, and pagination behavior for the port operations.
- Timeout guidance, rate limits, rate-limit headers, retry guidance, and transient-status semantics.
- Exact field semantics for season, kickoff timestamps/time zones, statuses, regular/extra-time/penalty scores, events, cards, and standings/group stages.
- Whether events have stable unique IDs suitable for future event idempotency.
- Which match-statistics fields are present and which must remain out of scope under the current schema.
- Coverage and plan entitlement for the five MVP competitions at the intended historical depth.
- Whether TheStatsAPI odds include documented bookmaker, market, timestamp, and explicit opening/closing semantics for each record consumed.
- Licensing clarifications recorded in provider selection: persistent PostgreSQL archive, attribution, public portfolio/demo use, and combining data with UK Odds API.

## 16. Outside This Contract

This document does not approve schema changes, player entities, new provider-mapping entity types, an event deduplication strategy, odds ingestion, a scheduler, data backfill, or any call to TheStatsAPI. Those belong to separately reviewed implementation tasks.

## 17. Proposed Next Task

Implement the TheStatsAPI read-only client after the pending official contract has been captured: add validated configuration, a transport client, documented DTOs, the provider port implementation, sanitized fixtures, and unit tests for HTTP/error/pagination behavior. Do not add database ingestion in that task. A subsequent task can implement mapper, repositories, and transactionally idempotent competition/season/team/match ingestion.

## Contract Validation

Validation date: 2026-09-02. This section uses only public, official TheStatsAPI material. It is a validation record, not an executable API specification. Where official public pages conflict or omit a detail, the status is **UNCONFIRMED** and no implementation assumption is authorized.

### Official Sources Consulted

- [API reference and plans](https://www.thestatsapi.com/)
- [Football API overview](https://www.thestatsapi.com/football-api), [standings API](https://www.thestatsapi.com/football/standings), and [coverage](https://www.thestatsapi.com/coverage)
- [Football fixtures API](https://www.thestatsapi.com/football/fixtures) and [results API](https://www.thestatsapi.com/football/results)
- [Match statistics API](https://www.thestatsapi.com/football/match-stats) and [official match-data guide](https://www.thestatsapi.com/blog/how-to-get-football-match-data-api)
- [Odds comparison API](https://www.thestatsapi.com/odds-api/odds-comparison) and [football odds API](https://www.thestatsapi.com/odds-api)
- [Coverage](https://www.thestatsapi.com/coverage), [Premier League](https://www.thestatsapi.com/football/league/premier-league), [La Liga](https://www.thestatsapi.com/football/league/la-liga), [Bundesliga](https://www.thestatsapi.com/football/league/bundesliga), [Serie A](https://www.thestatsapi.com/football/league/serie-a), and [UEFA Champions League](https://www.thestatsapi.com/football/league/champions-league) pages
- [Terms of Service](https://www.thestatsapi.com/terms) (last updated 2026-04-01)

### CONFIRMED

#### Authentication and transport

- The API is REST/JSON at the documented base `https://api.thestatsapi.com/api`; every request requires an API key sent as `Authorization: Bearer YOUR_API_KEY`. The official guide also illustrates `Accept: application/json`. Source: [official match-data guide](https://www.thestatsapi.com/blog/how-to-get-football-match-data-api).
- The key is obtained from the account dashboard and must be kept confidential. Source: [official match-data guide](https://www.thestatsapi.com/blog/how-to-get-football-match-data-api), [Terms of Service](https://www.thestatsapi.com/terms).
- `401 Unauthorized` is documented for a missing, invalid, or expired key; `429 Too Many Requests` for a plan-limit excess; and `404 Not Found` for an invalid endpoint or resource identifier. Source: [official match-data guide](https://www.thestatsapi.com/blog/how-to-get-football-match-data-api).

#### Competitions, seasons, matches, standings, and pagination

- Competition routes publicly listed are `GET /api/football/competitions`, `GET /api/football/competitions/{competition_id}`, and `GET /api/football/competitions/{competition_id}/seasons`. The list endpoint is documented as paginated; `page`, `per_page`, and `country` are publicly named parameters. Seasons are returned newest first, and the current season is identified by `is_current` / `current_season_id`. Source: [API reference](https://www.thestatsapi.com/).
- Matches are obtained through `GET /api/football/matches`; the documented filters include `competition_id`, `season`, `team_id`, date range, `status`, `page`, and `per_page` (not every page documents every filter). Official examples show a provider match identifier, competition identifier, competition name, season, status, UTC kickoff, sides, and scores for a finished match. Source: [fixtures API](https://www.thestatsapi.com/football/fixtures), [results API](https://www.thestatsapi.com/football/results), and [official match-data guide](https://www.thestatsapi.com/blog/how-to-get-football-match-data-api).
- Match listings are page-based. Official examples show `meta.page`, `meta.per_page`, `meta.total_pages`, and/or `meta.total`; callers must traverse from page 1 to `total_pages`. Source: [official match-data guide](https://www.thestatsapi.com/blog/how-to-get-football-match-data-api).
- The canonical-looking standings route in the current API reference is `GET /api/football/competitions/{competition_id}/seasons/{season_id}/standings`, optionally filtered by `group`. It returns rows ordered by group and position; linear leagues have a null group, group-stage competitions have `group_label`, and knockout-only competitions return an empty array. Source: [API reference](https://www.thestatsapi.com/).
- A published standings example contains team `id` and `name`, plus `position`, `matches_played`, `wins`, `draws`, `losses`, `goals_for`, `goals_against`, `goal_difference`, and `points`. This is compatible with the current `standings` model. Source: [official Serie A standings example](https://www.thestatsapi.com/football/league/serie-a/standings).

#### Match statistics, events, and odds capability

- `GET /api/football/matches/{match_id}/stats` is documented. Its published response is team-granular and contains `match_id` and home/away statistics including possession, shots, shots on target, corners, and xG where available; the documentation also states passes, fouls, and cards are available. Finalized statistics normally settle within one to two hours after full time. Source: [match statistics API](https://www.thestatsapi.com/football/match-stats).
- The provider publicly advertises goals, cards, substitutions, and minute-by-minute events for covered matches, and that finalized events settle within one to two hours after full time. Source: [API reference](https://www.thestatsapi.com/) and [coverage](https://www.thestatsapi.com/coverage).
- Pre-match odds are obtained through `GET /api/football/matches/{match_id}/odds`; a separate live route is documented as `/football/matches/{match_id}/odds/live`. The documented bookmaker set is Bet365, Pinnacle, Paddy Power, Betfair Sportsbook, and Kambi. Documented market families include 1X2/match odds, totals, BTTS, Asian handicap, draw no bet, and corners; availability varies by match, competition, bookmaker, and market. Source: [odds comparison API](https://www.thestatsapi.com/odds-api/odds-comparison), [football odds API](https://www.thestatsapi.com/odds-api).
- The odds example explicitly models bookmaker → market → selection and shows `opening` and `last_seen` values. It does not provide enough canonical evidence to establish whether `last_seen` is a closing value, a latest pre-kickoff snapshot, or another provider-defined measure. This preserves the existing rule: no inferred opening or closing price. Source: [odds comparison API](https://www.thestatsapi.com/odds-api/odds-comparison).

#### Dates, historical coverage, limits, and licence

- Published match examples use UTC ISO 8601 timestamps ending in `Z` (`kickoff_utc` or `utc_date`). Store the parsed instant as UTC. Source: [fixtures API](https://www.thestatsapi.com/football/fixtures), [official match-data guide](https://www.thestatsapi.com/blog/how-to-get-football-match-data-api).
- Historical match data is confirmed for all five MVP competitions: Premier League (32 seasons, back to 1994), La Liga (30, back to 1996), Bundesliga (30, back to 1996), Serie A (30, back to 1996), and UEFA Champions League (30, back to 1996). The competition pages also state fixtures/results, events, team data, and historical records. This confirms historical match coverage, not uniform availability of every sub-resource, market, or bookmaker for every season. Sources: the five [competition pages](https://www.thestatsapi.com/football/league).
- Published plan pages set request quotas and per-minute limits; one current plan table reports Starter/Growth/Scale as 100,000/500,000/5,000,000 requests per month and 120/300/1,000 requests per minute. Source: [API reference and plans](https://www.thestatsapi.com/).
- An active subscription grants a limited, non-exclusive, non-transferable, revocable licence to use data in the customer's own applications and products. Raw-data resale, sublicensing, bulk republication as a standalone dataset/feed/database, competitive re-offering, and storage beyond what is reasonably necessary are prohibited. Data may be displayed in end-user applications, websites, and internal tools. Source: [Terms of Service](https://www.thestatsapi.com/terms).

### UNCONFIRMED

#### Public-contract gaps

- **UNCONFIRMED:** a stable, authoritative JSON schema. Official pages use conflicting field shapes for the same resource (`id` versus `match_id`; `home_team`/`away_team` versus `home`/`away`; `utc_date` versus `kickoff_utc`; score object versus score nested in sides). No DTO field may be fixed until the provider supplies an account/API-reference schema or an authorized real response.
- **UNCONFIRMED:** exact response field set and identifier for competition and season objects. Routes and relationships are public, but published public examples do not establish their complete JSON payloads.
- **UNCONFIRMED:** a team endpoint path, its parameters, response shape, or an explicit competition/season relationship. The public site advertises team data but the inspected public material does not establish this contract.
- **UNCONFIRMED:** a match-events endpoint, event response schema, event external identifier, player identifier, team identifier, event type values, minute semantics, card-color semantics, or a reliable mapping for goals/yellows/reds/substitutions. Capability advertising is not an endpoint contract.
- **UNCONFIRMED:** team identifiers inside the match-statistics response. The public stats example names teams but does not show team IDs. Its full statistic set and historical availability per competition are also not contractually enumerated.
- **UNCONFIRMED:** pagination semantics for every route, maximum `per_page`, defaults, bounds, and partial-page/error behavior. Page metadata is confirmed for match lists; it is not established for all endpoints.
- **UNCONFIRMED:** error JSON body shape, machine-readable provider error code, request/correlation ID, `Retry-After`, rate-limit headers, retry policy, timeout guidance, and complete HTTP-status taxonomy. Only 401, 404, and 429 meanings are publicly documented.
- **UNCONFIRMED:** a precise rate limit applicable to the selected plan. The official guide still reports 30/60/300 requests per minute for Starter/Growth/Scale, while current plan pages report 120/300/1,000. Header behavior is not published. The account dashboard/support must provide the operative limit.
- **UNCONFIRMED:** odds timestamp(s), bookmaker external IDs, market external IDs, selection external IDs, line representation for all markets, price-history payload, and whether `last_seen` is an explicit close or a proxy. The public example supplies bookmaker names and opening/last-seen prices, but no timestamps or IDs beyond `match_id`.
- **UNCONFIRMED:** availability of odds in all historical seasons of the five MVP competitions. The provider confirms historical matches and says odds vary by match, competition, bookmaker, and market.
- **UNCONFIRMED:** whether a persistent PostgreSQL historical archive is "reasonably necessary", exact attribution requirements, and whether combining these data with UK Odds API is permitted. The Terms require attribution where it is required but do not define when or how.

### Diferencias respecto al diseño actual

- The conceptual port remains correctly separated from HTTP and persistence, and `competition → seasons → matches/stats/standings` is supported. However, its `list_teams(competition_external_id, season_external_id)` and `get_match_events(match_external_id)` operations are not publicly implementable yet because the official public contract does not document their routes/payloads.
- The port's `get_standings(competition_external_id, season_external_id)` matches the current API-reference hierarchy. A second, older-looking public standings example uses query parameters instead. Use the hierarchical route only after confirmation from the authenticated reference or support; do not support both speculatively.
- The external-ID approach remains valid for competition, season, team, and match. Match IDs are confirmed as the cross-resource join key. Event-level idempotency remains blocked: no public stable event ID is documented, and the approved `ProviderEntityType` has no event value.
- The existing `Match` model can store the documented finished scores, UTC kickoff, and supported statuses at a high level. **Possible incompatibility, not corrected:** public documentation does not confirm whether scores are regular-time, after-extra-time, or include penalties, nor does it document the extra-time/penalty fields needed by the model. Do not map those fields until verified.
- The existing `Standing` model supports the documented row fields. Champions League group labels are exposed by the current API reference, but the model has no group/stage column. This is not automatically a migration requirement because standings are already designed as optional snapshots; it is a decision required before persisting grouped historical UCL tables.
- The odds model supports provider, bookmaker, market, selection, opening/closing/snapshot, and timestamp, but the public odds contract does not expose timestamps or external IDs for all of them. Therefore odds ingestion is not ready, and `last_seen` must not automatically be labelled `closing` if the provider describes it as a latest stored/closing-price proxy.
- Public market documentation confirms 1X2 and totals but does not confirm Double Chance, Most Cards, or Cards Over/Under. The existing provider split with UK Odds API remains appropriate.

### Riesgos

- **High:** inconsistent official examples can produce invalid DTOs or incorrect mappings if implementation begins without an authenticated canonical API schema.
- **High:** storing broad historical copies may violate the Terms' "reasonably necessary" storage restriction; seek written provider confirmation before any backfill.
- **High:** events cannot be safely replayed/idempotently persisted under the approved model without a verified event ID plus an approved model/strategy decision.
- **Medium:** official rate-limit values conflict; hard-coded throughput or retry behavior would be unreliable.
- **Medium:** odds lack publicly documented timestamps and complete identity fields, so they cannot yet meet the project's temporal provenance requirement.
- **Medium:** UCL group tables have information not represented in `standings`; flattening them would lose group context.

### Decisiones necesarias antes de implementar

1. Obtain the authenticated canonical API reference or written support confirmation for the exact request/response schemas, current route set, status values, pagination limits, errors, and rate-limit headers.
2. Obtain written licence clarification that the planned historical PostgreSQL retention, attribution, public portfolio/demo use, and combination with UK Odds API are permitted.
3. Decide whether the first read-only client is limited to confirmed competition/season/match/standings/statistics routes, deferring teams and events until their endpoint contracts are provided.
4. Before any event ingestion, approve either a documented stable-event-ID persistence design or a deterministic replacement strategy with its data-loss trade-offs.
5. Decide how grouped UCL standings will be represented; do not flatten or persist them until group-context retention is explicitly approved.
6. Keep TheStatsAPI odds out of the first implementation until timestamps, identifiers, line semantics, and closing/opening semantics are confirmed.

## Final Official Evidence Audit

Validation date: 2026-09-02. This is the final evidence audit for implementation. The evidence threshold for **CONFIRMED** is an authenticated official API reference, an official OpenAPI/Swagger document, an official authenticated response example, or official written provider communication. Public pages can confirm advertised capabilities and examples, but do not close a canonical schema when official pages conflict or omit required fields.

### Evidence access

- **BLOCKED:** no TheStatsAPI credential is configured in the environment, and no authenticated provider panel, authenticated API response, official OpenAPI document, Swagger UI, or official written provider communication is available in the workspace.
- **INTERNAL DECISION:** do not call unauthenticated endpoints, guess a credential location, or promote public snippets to an authenticated contract. This section supersedes public-contract readiness where canonical fields are required.

### CONFIRMED

No provider field, response schema, error body, rate-limit header, or licence interpretation is confirmed by authenticated evidence in this audit.

Public official evidence confirms advertised resource capabilities and includes examples for matches, match statistics, standings, and odds. It does not provide enough consistent, canonical evidence to authorize client or DTO implementation. The public fixtures/results examples conflict with the general football API example (`match_id` versus `id`, `home`/`away` versus `home_team`/`away_team`, and `kickoff_utc` versus `utc_date`). Public standings examples also conflict between a flat hierarchical response and a `competition`/`season`/`table` envelope.

The following constraints are **INTERNAL DECISIONS**, confirmed by the approved project model rather than by the provider: external IDs remain separate from internal IDs; provider DTOs remain separate from persistence models; and opening odds are never inferred from a first observed snapshot.

The only work that can proceed safely before authenticated evidence arrives is documentation and contract-fixture preparation using explicitly labelled placeholders. No provider client, DTO, mapper, or ingestion code may be implemented from the public snippets alone.

### UNCONFIRMED

| Area | Required canonical contract information | Status |
|---|---|---|
| Authentication | Key lifecycle, headers, and authentication-error JSON schema | **UNCONFIRMED** |
| Competitions | Parameters, full schema, external ID, country/type, pagination envelope | **UNCONFIRMED** |
| Seasons | Full schema, external ID, display/season semantics, pagination | **UNCONFIRMED** |
| Teams | Route, parameters, schema, external ID, metadata, competition/season relationship | **BLOCKED** |
| Matches | Canonical names/types for IDs, teams, competition, season, UTC date, status, venue, score, extra time, penalties | **UNCONFIRMED** |
| Statistics | Schema, types/nullability, team identity, historical coverage guarantee | **UNCONFIRMED** |
| Standings | Canonical row schema, grouping semantics, historical snapshots, pagination | **UNCONFIRMED** |
| Events | Route, schema, stable ID, time/type values, team/player identity and card/substitution semantics | **BLOCKED** |
| Odds | IDs, timestamps, line/selection schema, opening/last_seen semantics, coverage | **BLOCKED** |
| Errors | Status matrix, error body, internal codes, request ID, parameter errors | **UNCONFIRMED** |
| Rate limits | Effective plan/trial limit, window, headers, `Retry-After`, excess behavior | **UNCONFIRMED** |
| Retry / timeout | Provider timeout, retry, backoff, 429 and 5xx policy | **UNCONFIRMED** |
| Licensing | PostgreSQL retention, cache/backups, attribution, public exposure, UK Odds API combination | **UNCONFIRMED** |
| Markets | Double Chance, Most Cards, Cards Over/Under availability | **UNCONFIRMED** |

Public official material previously recorded suggests candidate resource categories and routes, including a match timeline, but it contains incompatible examples for match and standings shapes. Those fields and paths therefore remain **UNCONFIRMED** for implementation.

### Contract Matrix

| Component | Status | Official evidence and remaining gap |
|---|---|---|
| competitions | **UNCONFIRMED** | Official reference advertises routes and pagination, but the complete response schema and identifier semantics are absent. |
| seasons | **UNCONFIRMED** | Official reference advertises the competition/season relationship, but the complete response schema and season identifier semantics are absent. |
| teams | **BLOCKED** | Team data is advertised and `/football/teams` appears in use-case navigation, but no official team endpoint contract or response schema was found. |
| matches | **UNCONFIRMED** | Fixtures/results pages provide endpoint examples, fields, and pagination, but official examples conflict on field names and do not define extra-time or penalty semantics. |
| standings | **UNCONFIRMED** | Official pages show both hierarchical grouped standings and a query-parameter table envelope; `group_label` is advertised, but the canonical response is unresolved. |
| statistics | **UNCONFIRMED** | Official match-stats page provides an endpoint and team-level example, but nullability, team IDs, complete field set, and historical guarantees are not fixed. |
| events | **BLOCKED** | Events are advertised, but no stable event ID, endpoint schema, or idempotency contract was found. |
| odds | **BLOCKED** | Official odds pages provide a route, bookmakers, markets, and opening/last-seen examples, but no complete IDs/timestamps/line schema. Public wording calls last-seen the latest stored pre-kickoff price; it must not be treated as `closing` without an explicit canonical definition. |
| errors | **UNCONFIRMED** | Public material mentions 401, 404, and 429, but no complete HTTP matrix or JSON error schema is provided. |
| rate limits | **UNCONFIRMED** | Current official plan pages publish 120/300/1,000 requests per minute, while previously published official material records 30/60/300. Headers and `Retry-After` remain undocumented. |
| licensing/storage | **UNCONFIRMED** | Terms permit use in own applications and public display while restricting raw redistribution, bulk republication, and unnecessary storage; PostgreSQL retention, backups, attribution details, and UK Odds API combination remain unresolved. |

### Final Decision

**BLOCKED BY PROVIDER CONTRACT**

The audit does not support moving to `READY FOR IMPLEMENTATION`. The five read-only resources have public capability evidence, but the canonical field-level contract required for safe DTO/client implementation is not closed. Teams, events, and odds remain blocked outright. Retry and timeout behavior are **INTERNAL DECISION** items only; they are not provider-confirmed requirements.

### INTERNAL DECISION

- The first client, once approved, is read-only and excludes event and odds ingestion.
- Only fields and parameters explicitly present in the authenticated contract may be mapped; unknown optional fields are not domain facts.
- Timeout and bounded retry policy are internal operational decisions, not provider requirements, until provider evidence is supplied.
- `last_seen` must retain its provider meaning and must not become `closing` unless the provider explicitly defines it as closing.
- H2H remains derived from persisted matches.

### BLOCKED

- **Events:** no authenticated schema or stable event ID; event-level identity and idempotency cannot be designed or implemented.
- **Odds:** no authenticated timestamp, identity, line/selection, or opening/last_seen contract; no odds implementation is permitted.
- **Teams:** no authenticated endpoint or schema; team mapping cannot safely be implemented.
- **Competitions, seasons, matches, standings, and statistics:** resource categories are publicly advertised, but code is blocked until canonical field-level schemas resolve conflicting public examples.
- **Historical ingestion:** blocked pending written clarification that the planned PostgreSQL archive, backups, attribution, public demo, and cross-provider combination comply with the Terms.

### Model impact

No database change is authorized. The potential impacts below are decisions, not proven incompatibilities:

1. Extra-time and penalty score semantics are unverified; existing `Match` fields must not be populated by assumption.
2. UCL group context may be returned but has no dedicated `standings` column; do not flatten grouped standings or migrate before a product decision.
3. `ProviderEntityType` has no event type. A future stable event ID requires separately reviewed event-idempotency design and potentially a migration.

### Implementation readiness

| Component | Readiness | Reason |
|---|---|---|
| competitions | **PARTIALLY READY** | Public route/capability is recorded, but canonical authenticated request/response schema and field semantics are unavailable. Client implementation is blocked. |
| seasons | **PARTIALLY READY** | Public route/relationship is recorded, but canonical authenticated request/response schema and field semantics are unavailable. Client implementation is blocked. |
| teams | **BLOCKED** | Endpoint and schema unavailable. |
| matches | **PARTIALLY READY** | Public listing capability and pagination metadata are recorded, but conflicting field names and score semantics block DTO/client implementation. |
| standings | **PARTIALLY READY** | Public route and row concepts are recorded, but canonical schema and grouped-standing persistence decision are unavailable. |
| statistics | **PARTIALLY READY** | Public match-statistics capability is recorded, but canonical schema, nullability, team identity, and coverage are unavailable. |
| events | **BLOCKED** | Endpoint/schema/stable ID unavailable. |
| odds | **BLOCKED** | Identity, timestamps, and semantic contract unavailable. |

### Exact prerequisite and next task

The next task is **not implementation**. Obtain from TheStatsAPI an accepted authenticated source: exported OpenAPI/Swagger, authenticated reference pages with schemas, sanitized official responses for the five read-only resources, and written answers covering event identity, score semantics, rate limits, error payloads, storage/attribution, and UK Odds API combination.

After those artifacts are provided in an approved project location, perform a narrow contract-review task that updates this section. Only if competitions, seasons, teams, matches, standings, and statistics become **READY** may the following task implement their read-only client; events and odds remain deliberately excluded.

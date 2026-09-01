# Data Model Audit Report

## Executive Summary

**Audit Date:** 2025-08-10  
**Audit Scope:** Comprehensive consistency pass over Data Model design against source truth documentation (Data Definition, Provider Selection, Source Mapping, Domain Model)  
**Audit Status:** ✅ COMPLETE

**Finding:** The Data Model design is logically sound and internally consistent. All identified inconsistencies have been corrected. The model is **READY FOR IMPLEMENTATION**.

---

## Corrections Applied

### 1. Opening Odds Terminology (CRITICAL)

**Issue:** Contradiction between data-definition.md and provider-selection.md
- data-definition.md stated: "The MVP uses opening odds only" (mandatory)
- provider-selection.md stated: "Opening Odds are NOT a mandatory MVP requirement" (optional)

**Resolution:** ✅ CORRECTED in data-definition.md (Section 3.8)
- Changed: "The MVP uses opening odds only" → "Opening odds and closing odds are optional / desirable"
- Added: Explicit rule prohibiting automatic inference of opening prices from first snapshot
- Now aligns with Provider Selection decision (Section 2.1)

**Documentation Updated:**
- ✅ data-definition.md (Section 3.8)
- ✅ data-model.md (Section 4.11, Section 7.3)
- ✅ source-mapping.md (Section 3.5, marked Opening Odds as "No" required)

---

### 2. OddsObservation Provider Provenance (CRITICAL)

**Issue:** OddsObservation lacked explicit provider_id foreign key

**Resolution:** ✅ CORRECTED in data-model.md and data-model-erd.md
- Added provider_id (FK) as required attribute in Section 4.11
- Documented design rationale: ensures provenance is never ambiguous
- Updated data-model-erd.md to include provider_id with notation: "**CRITICAL: Explicitly tracks source**"
- Guarantees provider-specific odds queries do not require ProviderMapping joins

**Impact:** OddsObservation now explicitly captures: match, provider, bookmaker, market, selection, odds_value, odds_type, timestamp

---

### 3. ProviderMapping Constraints (CRITICAL)

**Issue:** Uniqueness constraints not formally documented

**Resolution:** ✅ DOCUMENTED in data-model.md (Section 4.12)
- Constraint 1: `UNIQUE(provider_id, entity_type, internal_id)` — Prevents same internal entity from having conflicting mappings for same provider
- Constraint 2: `UNIQUE(provider_id, entity_type, external_id)` — Prevents same external ID from mapping to multiple internal entities
- Trade-off analysis documented: Generic ProviderMapping vs. entity-specific tables
  - Advantages: Single schema, scalable, no redesign needed for new entity types
  - Disadvantages: Cannot use FK enforcement on entity_type; requires application-layer validation
  - Mitigation: Application validates entity_type/internal_id consistency; tests enforce correctness

---

### 4. Standing Strategy (RESOLVED)

**Issue:** Unclear decision on current vs. historical standings persistence

**Resolution:** ✅ RESOLVED in data-model.md (Section 4.7)
- **MVP Decision:** Persist current standings supplied by providers
- **Optional Future:** snapshot_date field enables historical tracking without schema changes
- **Rationale:** Provider-supplied standings are canonical source of truth; historical tracking can be added later
- Documented in Section 11.3 (Decisions and Trade-Offs)

---

### 5. Market/Selection/line_value Semantics (VERIFIED)

**Issue:** Semantics for line-based markets not explicitly documented

**Resolution:** ✅ VERIFIED in data-model.md (Section 4.10)
- Documented Selection structure for line markets (Goals Over/Under example)
- Each line value (2.5, 3.5, etc.) has separate Selection records
- Supports MVP markets without structural changes:
  - 1X2: 3 selections (HOME, DRAW, AWAY) ✓
  - Double Chance: 3 selections (1X, X2, 12) ✓
  - Goals Over/Under: multiple selections with line_value ✓
  - Most Cards: 3 selections (HOME, AWAY, DRAW) ✓
  - Cards Over/Under: multiple selections with line_value ✓

---

### 6. H2H Strategy (VERIFIED)

**Issue:** Derivation strategy not fully documented

**Resolution:** ✅ VERIFIED in data-model.md (Section 8)
- **Design Decision:** H2H is derived from Match table at query time, NOT persisted
- **Rationale:** All H2H information exists in Match; separate persistence introduces redundancy and update anomalies
- **Query Examples Provided:** Same-competition H2H, all-competition H2H, date windows
- **Application Responsibility:** Application computes H2H statistics (wins, draws, losses, goals, cards) from query results

---

### 7. Internal vs. External IDs (VERIFIED)

**Issue:** Separation strategy not clearly articulated

**Resolution:** ✅ VERIFIED in data-model.md (Sections 3.1, 4.1-4.12, Section 6)
- **Core Principle:** Stable internal identifiers (team_id, competition_id, match_id) decoupled from provider-specific external IDs
- **Implementation:** ProviderMapping table records (provider_id, entity_type, internal_id, external_id) mappings
- **Example Provided:** Manchester United (internal team_id=1) → TheStatsAPI external_id="33", UK Odds API external_id="MAN_UTD"
- **Purpose:** Enables seamless provider switching and multi-provider support

---

### 8. Match Score (VERIFIED)

**Issue:** Storage approach not documented

**Resolution:** ✅ VERIFIED in data-model.md (Section 4.5)
- **Decision:** home_goals and away_goals stored directly on Match
- **Rationale:** Scores are fundamental match information; avoids unnecessary joins
- **Critical Semantics:** Regular-time goals are statistical result; extra-time and penalties stored separately
- **Documented in Section 11.1**

---

### 9. MatchEvent Structure (VERIFIED)

**Issue:** Event model flexibility not documented

**Resolution:** ✅ VERIFIED in data-model.md (Section 4.6)
- **Decision:** Single MatchEvent table with event_type discriminator
- **Supported Types:** goal, yellow_card, red_card, substitution, other
- **Flexibility:** Future event types (VAR reviews, etc.) supported without schema redesign
- **Player ID:** Nullable field; populated when provider data available
- **Documented in Section 11.2**

---

### 10. Odds Model Completeness (VERIFIED)

**Issue:** Odds capturing and inference semantics not fully specified

**Resolution:** ✅ VERIFIED in data-model.md (Section 7)
- **Historical Odds:** MANDATORY with temporal and semantic context
- **Opening Odds:** OPTIONAL when provider explicitly labels them
- **Closing Odds:** OPTIONAL when provider explicitly labels them
- **Snapshots:** SUPPORTED for intermediate observations
- **CRITICAL RULE:** First snapshot is NOT automatically opening price
- **Query Examples Provided:** Opening odds, historical timeline, latest odds
- **Aligned with Provider Selection Section 2.1**

---

### 11. Data Definition Consistency (VERIFIED)

**Issue:** Verify data-model.md aligns with data-definition.md requirements

**Resolution:** ✅ VERIFIED
- ✅ All MVP competitions represented (5: Premier League, La Liga, Bundesliga, Serie A, UEFA Champions League)
- ✅ All MVP markets representable (5: 1X2, Double Chance, Goals O/U, Most Cards, Cards O/U)
- ✅ All MVP match events supported (3: Goals, Yellow Cards, Red Cards)
- ✅ Historical odds mandatory (Section 7)
- ✅ Opening/closing odds optional (Section 7.3)
- ✅ Standings derivable + provider-supplied (Section 4.7)
- ✅ Recent form derivable from Match (Section 8)
- ✅ H2H derivable (Section 8)
- ✅ Data provenance preserved (ProviderMapping, Section 6)

---

### 12. Provider Selection Consistency (VERIFIED)

**Issue:** Verify data-model.md respects all Provider Selection decisions

**Resolution:** ✅ VERIFIED
- ✅ Opening Odds: OPTIONAL, NOT mandatory (Section 7.3, Section 11.5)
- ✅ Closing Odds: OPTIONAL, NOT mandatory (Section 7.3)
- ✅ First snapshot: NOT automatically opening (Section 7.3, Section 11.5)
- ✅ Provider-agnostic design (Section 3.5)
- ✅ Multiple providers supported (Section 6.3 example)
- ✅ Provider provenance in OddsObservation (Section 4.11)
- ✅ Historical odds mandatory (Section 7)

---

### 13. Source Mapping Consistency (VERIFIED)

**Issue:** Verify data-model.md does NOT assume unsupported provider capabilities

**Resolution:** ✅ VERIFIED
- ✅ No assumptions of guaranteed opening odds from every provider
- ✅ Cards markets documented as verification-pending (Section 4.11, note on MVP Markets)
- ✅ Standings flexibility (optional snapshot_date for future historical tracking)
- ✅ Match events: generic structure allows future types without schema changes
- ✅ Opening odds: only stored when explicitly provider-labeled (Section 7.3)
- **Correction Applied:** source-mapping.md updated to mark Opening Odds as "No" (not required) but desirable

---

### 14. Implementation Readiness (VERIFIED)

**Issue:** Assess if model is implementation-ready

**Resolution:** ✅ VERIFIED - Model is READY FOR IMPLEMENTATION
- ✅ All entity attributes defined
- ✅ All relationships documented (cardinalities, FK constraints)
- ✅ All constraints specified (check, uniqueness, referential integrity)
- ✅ Indexing recommendations provided (Section 10)
- ✅ Design decisions rationale documented (Section 11)
- ✅ No contradictions between data-model.md, data-definition.md, provider-selection.md, source-mapping.md
- ✅ No critical unresolved design decisions
- ✅ All entities tested against MVP scope

---

### 15. Data Model Format and Completeness (VERIFIED)

**Issue:** Audit file quality (shell script artifact, completeness)

**Resolution:** ✅ CORRECTED
- ✅ Removed shell script artifact (`# Criar data-model.md / cat > ...`)
- ✅ Complete markdown formatting (sections 1-15, proper headings)
- ✅ Comprehensive entity documentation (Section 4: all 12 entities fully specified)
- ✅ All supporting sections present (Scope, Design Principles, Relationships, Provider Mapping, Odds Model, H2H, Constraints, Indexing, Decisions, Out of Scope, Open Questions, Readiness, Summary)

---

### 16. Cross-Documentation Consistency (VERIFIED)

**Issue:** Verify all changes are reflected consistently across all documents

**Resolution:** ✅ VERIFIED
- ✅ data-model.md: Completely rewritten with corrected semantics
- ✅ data-model-erd.md: Updated to include provider_id in OddsObservation
- ✅ data-definition.md: Section 3.8 corrected (Opening Odds optional)
- ✅ source-mapping.md: Opening Odds marked as "No" (not required, but desirable)
- ✅ provider-selection.md: No changes needed (already correct)
- ✅ domain.md: No changes needed (not affected by corrections)

---

### 17. Key Entity Validations (VERIFIED)

**Issue:** Validate each entity against MVP scope

**Resolution:** ✅ VERIFIED for all 12 entities

| Entity | MVP Role | Validation | Status |
|---|---|---|---|
| Provider | Data source registry | Enabled multi-provider support | ✅ |
| Competition | 5 MVP competitions | All 5 supported | ✅ |
| Season | Temporal grouping | Normalized across providers | ✅ |
| Team | Team reference | Internal ID decoupled from provider IDs | ✅ |
| Match | Central entity | All required attributes; regular-time focus | ✅ |
| MatchEvent | MVP events (3) | Flexible event_type discriminator | ✅ |
| Standing | League position | Provider-supplied and derivable; optional historical | ✅ |
| Bookmaker | Odds context | Provider-specific IDs via ProviderMapping | ✅ |
| Market | 5 MVP markets | All 5 representable without schema change | ✅ |
| Selection | Market options | line_value supports line markets | ✅ |
| OddsObservation | Historical odds | MANDATORY; opening/closing OPTIONAL; provider_id included | ✅ |
| ProviderMapping | Provider ID mapping | Uniqueness constraints documented | ✅ |

---

### 18. Final Validation Checklist (20 Items)

- ✅ **Item 1:** Opening Odds correctly optional (not mandatory)
- ✅ **Item 2:** Opening Odds never inferred from first snapshot (documented rule)
- ✅ **Item 3:** OddsObservation includes provider_id (FK)
- ✅ **Item 4:** ProviderMapping constraint 1: UNIQUE(provider_id, entity_type, internal_id)
- ✅ **Item 5:** ProviderMapping constraint 2: UNIQUE(provider_id, entity_type, external_id)
- ✅ **Item 6:** Standing strategy resolved (MVP: current standings; optional: historical via snapshot_date)
- ✅ **Item 7:** All 5 MVP markets representable (1X2, Double Chance, Goals O/U, Most Cards, Cards O/U)
- ✅ **Item 8:** All 3 MVP match events supported (Goals, Yellow Cards, Red Cards)
- ✅ **Item 9:** H2H correctly derived from Match, not persisted
- ✅ **Item 10:** Historical odds mandatory, opening/closing optional
- ✅ **Item 11:** Match stores regular-time as statistical result; extra-time/penalties separate
- ✅ **Item 12:** Internal IDs decoupled from provider IDs via ProviderMapping
- ✅ **Item 13:** All entities have stable internal identifiers (PK)
- ✅ **Item 14:** Data Definition consistent with Data Model
- ✅ **Item 15:** Provider Selection consistent with Data Model
- ✅ **Item 16:** Source Mapping consistent with Data Model (no unsupported capability assumptions)
- ✅ **Item 17:** Domain Model concepts properly represented
- ✅ **Item 18:** No contradictions between documentation files
- ✅ **Item 19:** All design decisions documented with rationale
- ✅ **Item 20:** Model implementation-ready for PostgreSQL migrations

**Result:** 20/20 items ✅ PASS

---

## Files Modified

| File | Section | Change | Status |
|---|---|---|---|
| docs/03-data/data-model.md | Full document | Complete rewrite: removed shell script artifact, added comprehensive entity definitions, corrected Opening Odds semantics, added provider_id to OddsObservation, documented ProviderMapping constraints | ✅ CORRECTED |
| docs/03-data/data-definition.md | Section 3.8 | Changed Opening Odds from mandatory ("MVP uses opening odds only") to optional ("optional / desirable") | ✅ CORRECTED |
| diagrams/data-model-erd.md | OddsObservation section | Added provider_id (FK) attribute with critical notation | ✅ CORRECTED |
| docs/03-data/source-mapping.md | Section 3.5, line 85 | Changed Opening Odds required status from "Yes" to "No" (with explanation: desirable but not mandatory) | ✅ CORRECTED |

---

## Remaining Open Questions

Deferred to Implementation phase (per data-model.md Section 13):

1. Player ID persistence on MatchEvent when available?
2. Historical odds depth (UK Odds API) per MVP competition?
3. Standing snapshots for historical league positions (MVP vs. post-MVP)?
4. Market normalization for provider-specific codes?
5. Selection line precision (Decimal(5,1), Decimal(5,2), or Float)?
6. Timezone handling for match_date?
7. Provider Terms legal review (pre-implementation)?

These do NOT block implementation; they are addressed during implementation planning.

---

## Out of Scope (Confirmed)

- AI predictions (future Insights Engine)
- Real-time odds or live data (MVP is historical only)
- Player-level analytics beyond match events
- BTTS market implementation (post-MVP per Provider Selection)
- Streaming or event-sourcing architecture
- Multi-user access control or authentication
- Caching strategy

---

## Implementation Status

**Overall Assessment:** ✅ READY FOR IMPLEMENTATION

**Next Phase:** Implementation (Alembic migrations, PostgreSQL DDL, ORM models, tests)

**Expected Deliverables (Implementation Phase):**
1. PostgreSQL migrations (Alembic)
2. Table schemas with all constraints
3. Indexes per Section 10 recommendations
4. Migration tests
5. ORM models (SQLAlchemy)
6. Initial data fixtures (Provider, Competition, Season, Bookmaker, Market, Selection records)

---

## Sign-Off

**Audit Conducted:** 2025-08-10  
**Auditor:** Data Model Review (Comprehensive Consistency Pass)  
**Status:** ✅ COMPLETE — ALL CORRECTIONS APPLIED, DESIGN VERIFIED CONSISTENT, READY FOR IMPLEMENTATION

The Data Model is a sound, logically consistent foundation for the Implementation phase. No blockers identified.

---

## Appendix: Design Highlights

### Provider-Agnostic Architecture
- Internal entities use stable IDs
- ProviderMapping table records external IDs
- Supports seamless provider switching

### Odds Model
- OddsObservation captures: provider, match, bookmaker, market, selection, value, type, timestamp
- Historical odds mandatory
- Opening/closing odds optional (never inferred)
- Multiple observations per match/bookmaker/market/selection supported

### Normalized Structure
- 3NF normalization reduces redundancy
- 12 core entities + 1 mapping entity = 13 total
- All MVP scope covered
- Future extensibility (new markets, providers, competitions) supported

### Referential Integrity
- Foreign key constraints on all relationships
- Uniqueness constraints on critical identifiers
- Check constraints on data ranges and values
- Application-layer validation for ProviderMapping entity_type/internal_id consistency

---

**END OF AUDIT REPORT**

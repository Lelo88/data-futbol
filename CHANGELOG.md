# Changelog

## [Unreleased]

### Added

- Project documentation and planning foundation
- Project restart and direction change toward historical football analytics
- Data Definition for required historical football data and MVP betting markets
- Source Research for candidate external data sources
- Source Mapping for required data elements and candidate source alignment
- Provider Selection documentation: finalized provider-selection.md with MVP competition scope, coverage matrices, provider responsibility matrix, and licensing validations (pre-implementation clarifications recorded). - PostgreSQL 16 data model implementation with Alembic migration, SQLAlchemy persistence metadata, Docker workflow, and integration tests.
- TheStatsAPI integration contract documenting the provider port, DTO boundary, mapping and external-ID strategy, configuration, error policy, idempotency, and implementation test plan.
- Official TheStatsAPI contract validation, including confirmed public endpoints/capabilities and documented blockers caused by missing or contradictory public-schema, event, odds, rate-limit, and licensing details.
- Authenticated-contract closure record: no authenticated source was available, so provider implementation remains blocked pending canonical schemas and licensing clarification.
- Final official evidence audit: public documentation was rechecked; capability evidence improved, but canonical schemas, event/odds identity, operational limits, and licensing clarifications remain insufficient for implementation.

### Changed

- Python became the preferred primary language instead of Go
- Real-time data requirements were removed from the MVP scope
- AI predictions were excluded from the MVP scope
- The project domain and MVP scope were defined around historical football analysis and decision support

## [0.1.0] - Repository Initialization

### Added

- Initial repository structure
- Documentation folders

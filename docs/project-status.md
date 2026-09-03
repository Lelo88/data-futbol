# Project Status

> Living document that summarizes the current state of the project.

---

# Current Phase

Provider Integration — Authenticated Contract Closure

Status:

⛔ Blocked pending provider evidence

The approved data model has been implemented as a PostgreSQL 16 Alembic migration with SQLAlchemy persistence metadata and integration tests. The final official evidence audit remains blocked because no canonical authenticated schema, provider evidence for teams/events/odds, or written licensing clarification was available. Details are recorded in `docs/04-providers/the-stats-api-integration.md`.

---

# Repository

Repository:

football-analytics

Branch strategy:

main
develop
feature/*
docs/*
fix/*
refactor/*
chore/*

---

# Vision

Current objective:

Build a football analytics platform focused on historical statistics and decision support.

The platform is NOT intended to:

- Predict matches
- Recommend bets
- Consume live data

Instead it aims to:

- Centralize football statistics
- Generate statistical summaries
- Produce analytical insights
- Compare historical frequencies against bookmaker implied probabilities

---

# Product Definition

Current MVP

✔ Team comparison

✔ Historical statistics

✔ League standings

✔ Head-to-head

✔ Goals

✔ Yellow cards

✔ Red cards

✔ Opening bookmaker odds

✔ Statistical summaries

Not included

✖ AI predictions

✖ Live matches

✖ Live odds

✖ Authentication

✖ Multi-user support

---

# Architecture Decisions

Current direction:

Python

PostgreSQL

Docker

Jupyter (only for exploration)

Dash or Streamlit (to be decided)

SQLAlchemy

Alembic

Pandas

Architecture:

Modular

Domain-oriented

Pipeline-based

---

# Documentation Status

Current focus: obtain the provider's canonical authenticated contract and written licensing clarifications. No TheStatsAPI client is authorized until those blockers are resolved.

| Phase | Status |
|-------|--------|
| Project Definition | Completed |
| Domain Definition | Completed |
| Data Definition | Completed |
| Source Research | Completed |
| Source Mapping | Completed |
| Provider Selection | Completed |
| Data Model | Completed |
| Provider Integration — Technical Design | Completed |
| Provider Integration — Official Contract Validation | Completed with blockers |
| Provider Integration — Authenticated Contract Closure | Blocked after final official evidence audit |
| Ingestion | Pending |
| Statistical Engine | Pending |
| Insights Engine | Pending |

---

# Specifications

Not started.

---

# Implementation

Data Model persistence layer completed: PostgreSQL schema, Alembic migration, Docker PostgreSQL 16 workflow, SQLAlchemy metadata, and integration tests.

---

# Next Milestone

Obtain canonical authenticated TheStatsAPI schemas, official sanitized examples, and written licensing clarification; then re-review contract readiness before approving any read-only client. The final public audit remains `BLOCKED BY PROVIDER CONTRACT`.

---

# Current Roadmap

1. Project Definition
2. Domain Definition
3. Data Definition
4. Source Research
5. Source Mapping
6. Provider Selection
7. Data Model
8. Ingestion
9. Statistical Engine
10. Insights Engine

---

# Decisions Taken

## 2026-08

- The project was restarted from scratch.
- Project Definition was completed.
- Domain Definition was completed.
- Data Definition was completed.
- Source Research was completed.
- Source Mapping was completed.
- Go was discarded as the primary language.
- Python became the preferred language.
- The project shifted from backend-oriented to data analytics oriented.
- Live data ingestion was removed.
- AI predictions were postponed.
- Historical statistics became the foundation of the platform.
- Insights will be generated from statistics rather than raw data.
- A Decision Engine will interpret statistical evidence.
- The project will be documentation-first.

---

# Open Questions

- Final dashboard technology.
- Initial data provider.
- Probability model for future versions.

---

# Last Updated

2026-09-02

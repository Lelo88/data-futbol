# Project Status

> Living document that summarizes the current state of the project.

---

# Current Phase

Source Research

Status:

✅ Completed

Source Research is complete. Candidate external data sources were researched and documented for historical coverage, data capabilities, betting markets, odds availability, formats, pricing, usage limits, licensing considerations, and integration considerations. Several capabilities remain Unknown or Partially verified, and no definitive provider has been selected.

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

Current focus: source mapping after the completed data definition and source research phases.

| Phase | Status |
|-------|--------|
| Project Definition | Completed |
| Domain Definition | Completed |
| Data Definition | Completed |
| Source Research | Completed |
| Source Mapping | Pending |
| Provider Selection | Pending |
| Data Model | Pending |
| Ingestion | Pending |
| Statistical Engine | Pending |
| Insights Engine | Pending |

---

# Specifications

Not started.

---

# Implementation

Not started.

---

# Next Milestone

Complete all project documentation before writing production code.

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
- Domain Definition is currently being finalized.
- Data Definition was completed.
- Source Research was completed.
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

2026-08-09
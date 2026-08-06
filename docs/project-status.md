# Project Status

> Living document that summarizes the current state of the project.

---

# Current Phase

Project Definition

Status:

🟡 Documentation in progress

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

| Document | Status |
|----------|--------|
| README | ⏳ |
| Project Vision | ⏳ |
| Domain | Pending |
| Statistical Questions | Pending |
| Data Sources | Pending |
| Architecture | Pending |
| Roadmap | Pending |
| Decision Log | Pending |
| Glossary | Pending |

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

1. Project Vision
2. Domain
3. Statistical Questions
4. Data Sources
5. Stack Decision
6. Architecture
7. Roadmap
8. Specs
9. Checklists
10. Python implementation

---

# Decisions Taken

## 2026-08

- The project was restarted from scratch.
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

2026-08-05
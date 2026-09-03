# ⚽ Data-Futbol

> Transform historical football data into actionable insights.

Football Analytics is a data analytics platform focused on collecting, organizing, analyzing, and visualizing historical football statistics.

The goal of the project is to reduce the time required to perform pre-match analysis by centralizing relevant statistical information and transforming raw data into meaningful insights.

The platform is designed to support informed decision-making through historical evidence rather than predictions.

---

# 🚧 Project Status

Current phase:

> Provider Integration technical design completed

The PostgreSQL schema, Alembic migration, SQLAlchemy persistence metadata, and database integration tests are available. The TheStatsAPI integration contract is documented; provider HTTP implementation and ingestion remain pending verification of the official API contract and licensing clarifications.

---

# 🎯 Goals

The MVP aims to provide:

- Historical team comparison
- Recent form analysis
- League standings
- Head-to-head statistics
- Goals scored and conceded
- Yellow and red cards
- Opening bookmaker odds (when available)
- Statistical summaries
- Decision-support insights

---

# 🏗 Project Principles

The project follows several fundamental principles:

- Documentation First
- Clean Architecture
- Clean Code
- Modular Design
- Reproducible Analysis
- Transparent Statistics
- Extensible Components

---

# 📚 Documentation

Project documentation is available under the `/docs` directory.

Current documentation includes:

- Project Vision
- Project Status
- Project History
- Data Definition
- Source Research
- Source Mapping
- Provider Selection
- TheStatsAPI Integration Contract
- Domain Model
- Statistical Questions
- Glossary

Additional documentation will include:

- Data Model
- Ingestion
- Statistical Engine
- Insights Engine
- Architecture
- Development Workflow
- Quality Standards

---

# 📁 Repository Structure

```text
football-analytics/

.github/
docs/
specs/
checklists/
diagrams/

src/
tests/

README.md
CHANGELOG.md
LICENSE
CONTRIBUTING.md
```

---

# 🛣 Development Roadmap

The project will be developed incrementally following these phases:

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

# 🛠 Planned Technology Stack

The current technical direction includes:

- Python 3.12+
- PostgreSQL 16
- SQLAlchemy
- Alembic
- Pandas
- Docker

## Database setup

Copy `.env.example` to `.env` (or export `DATABASE_URL`), then start PostgreSQL and apply the migration:

```sh
docker compose up -d postgres
python -m pip install -e '.[dev]'
alembic upgrade head
pytest
```

The initial migration seeds the supported providers (TheStatsAPI and UK Odds API), MVP competitions, and the five approved MVP market definitions. It does not call provider APIs or ingest provider data.

Additional technologies will be evaluated as the project evolves.

---

# 🤝 Contributing

This project is currently under active development.

Contribution guidelines will be published after the MVP is completed.

---

# 📄 License

This project is licensed under the MIT License.

---

# ⭐ Vision

> Collect reliable historical data.

> Transform data into statistics.

> Transform statistics into insights.

> Help people make better decisions.

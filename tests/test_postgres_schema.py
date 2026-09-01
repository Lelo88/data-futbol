"""Integration tests for the approved PostgreSQL data model.

Set DATABASE_URL to run them (the Docker Compose defaults are documented in the
README). They intentionally exercise the migrated schema, not ORM constructors.
"""
from __future__ import annotations

import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError


DATABASE_URL = os.getenv("DATABASE_URL")
pytestmark = pytest.mark.integration


@pytest.fixture(scope="session")
def engine():
    if not DATABASE_URL:
        pytest.skip("DATABASE_URL is required for PostgreSQL integration tests")
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", DATABASE_URL)
    command.upgrade(alembic_config, "head")
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        assert connection.execute(text("SELECT count(*) FROM providers")).scalar_one() == 2
        assert connection.execute(text("SELECT count(*) FROM competitions")).scalar_one() == 5
        assert connection.execute(text("SELECT count(*) FROM markets")).scalar_one() == 5
    yield engine
    engine.dispose()


@pytest.fixture(autouse=True)
def clean_database(engine):
    with engine.begin() as connection:
        connection.execute(text("""
            TRUNCATE provider_mappings, odds_observations, selections, markets,
            bookmakers, standings, match_events, matches, seasons, teams,
            competitions, providers RESTART IDENTITY CASCADE
        """))
        connection.execute(text("""
            INSERT INTO providers (name) VALUES ('TheStatsAPI'), ('UK Odds API');
            INSERT INTO markets (code, name) VALUES ('1X2', '1X2'), ('GOALS_OVER_UNDER', 'Goals Over/Under');
        """))


def base_match(connection):
    competition_id = connection.execute(text("""
        INSERT INTO competitions (name, type, country_code)
        VALUES ('Test League', 'domestic_league', 'AR') RETURNING competition_id
    """)).scalar_one()
    season_id = connection.execute(text("""
        INSERT INTO seasons (competition_id, season_year) VALUES (:competition_id, 2026)
        RETURNING season_id
    """), {"competition_id": competition_id}).scalar_one()
    home_team_id = connection.execute(text("INSERT INTO teams (name) VALUES ('Home FC') RETURNING team_id")).scalar_one()
    away_team_id = connection.execute(text("INSERT INTO teams (name) VALUES ('Away FC') RETURNING team_id")).scalar_one()
    match_id = connection.execute(text("""
        INSERT INTO matches (
            competition_id, season_id, home_team_id, away_team_id, match_date,
            match_status, home_goals, away_goals
        ) VALUES (:competition_id, :season_id, :home_team_id, :away_team_id,
                  '2026-08-01 15:00:00+00', 'completed', 1, 0)
        RETURNING match_id
    """), {
        "competition_id": competition_id, "season_id": season_id,
        "home_team_id": home_team_id, "away_team_id": away_team_id,
    }).scalar_one()
    return competition_id, season_id, home_team_id, away_team_id, match_id


def test_migration_creates_required_tables_and_reference_data(engine):
    with engine.connect() as connection:
        tables = set(connection.execute(text("""
            SELECT tablename FROM pg_tables WHERE schemaname = 'public'
        """)).scalars())
        assert {
            "providers", "competitions", "seasons", "teams", "matches", "match_events",
            "standings", "bookmakers", "markets", "selections", "odds_observations",
            "provider_mappings",
        } <= tables
        assert connection.execute(text("SELECT count(*) FROM providers")).scalar_one() == 2
        assert connection.execute(text("SELECT count(*) FROM markets")).scalar_one() == 2


def test_match_integrity_and_event_team_participation(engine):
    with engine.begin() as connection:
        competition_id, season_id, home_team_id, away_team_id, match_id = base_match(connection)
        connection.execute(text("""
            INSERT INTO match_events (match_id, event_type, team_id, minute)
            VALUES (:match_id, 'goal', :home_team_id, 23)
        """), {"match_id": match_id, "home_team_id": home_team_id})
        third_team_id = connection.execute(text("INSERT INTO teams (name) VALUES ('Third FC') RETURNING team_id")).scalar_one()
        other_competition_id = connection.execute(text("""
            INSERT INTO competitions (name, type, country_code)
            VALUES ('Other League', 'domestic_league', 'UY') RETURNING competition_id
        """)).scalar_one()

    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text("""
                INSERT INTO matches (competition_id, season_id, home_team_id, away_team_id, match_date, match_status)
                VALUES (:competition_id, :season_id, :home_team_id, :away_team_id,
                        '2026-08-02 14:00:00+00', 'scheduled')
            """), {"competition_id": other_competition_id, "season_id": season_id,
                   "home_team_id": home_team_id, "away_team_id": away_team_id})

    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text("""
                INSERT INTO matches (competition_id, season_id, home_team_id, away_team_id, match_date, match_status)
                VALUES (:competition_id, :season_id, :home_team_id, :home_team_id,
                        '2026-08-02 15:00:00+00', 'scheduled')
            """), {"competition_id": competition_id, "season_id": season_id, "home_team_id": home_team_id})

    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text("""
                INSERT INTO match_events (match_id, event_type, team_id)
                VALUES (:match_id, 'yellow_card', :third_team_id)
            """), {"match_id": match_id, "third_team_id": third_team_id})


def test_provider_mapping_uniqueness(engine):
    with engine.begin() as connection:
        provider_id = connection.execute(text("SELECT provider_id FROM providers WHERE name = 'TheStatsAPI'")).scalar_one()
        team_id = connection.execute(text("INSERT INTO teams (name) VALUES ('Mapped FC') RETURNING team_id")).scalar_one()
        connection.execute(text("""
            INSERT INTO provider_mappings (provider_id, entity_type, internal_id, external_id)
            VALUES (:provider_id, 'team', :team_id, 'provider-team-1')
        """), {"provider_id": provider_id, "team_id": str(team_id)})

    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text("""
                INSERT INTO provider_mappings (provider_id, entity_type, internal_id, external_id)
                VALUES (:provider_id, 'team', :team_id, 'provider-team-2')
            """), {"provider_id": provider_id, "team_id": str(team_id)})

    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            other_team_id = connection.execute(text("INSERT INTO teams (name) VALUES ('Other Mapped FC') RETURNING team_id")).scalar_one()
            connection.execute(text("""
                INSERT INTO provider_mappings (provider_id, entity_type, internal_id, external_id)
                VALUES (:provider_id, 'team', :team_id, 'provider-team-1')
            """), {"provider_id": provider_id, "team_id": str(other_team_id)})


def test_odds_observation_references_valid_entities_and_selection_market(engine):
    with engine.begin() as connection:
        _, _, _, _, match_id = base_match(connection)
        provider_id = connection.execute(text("SELECT provider_id FROM providers WHERE name = 'UK Odds API'")).scalar_one()
        bookmaker_id = connection.execute(text("INSERT INTO bookmakers (name) VALUES ('Test Book') RETURNING bookmaker_id")).scalar_one()
        market_id = connection.execute(text("SELECT market_id FROM markets WHERE code = '1X2'")).scalar_one()
        other_market_id = connection.execute(text("SELECT market_id FROM markets WHERE code = 'GOALS_OVER_UNDER'")).scalar_one()
        selection_id = connection.execute(text("""
            INSERT INTO selections (market_id, code, name) VALUES (:market_id, 'HOME', 'Home')
            RETURNING selection_id
        """), {"market_id": market_id}).scalar_one()
        connection.execute(text("""
            INSERT INTO odds_observations (
                provider_id, match_id, bookmaker_id, market_id, selection_id,
                odds_value, odds_type, observation_timestamp
            ) VALUES (:provider_id, :match_id, :bookmaker_id, :market_id, :selection_id,
                      1.875, 'snapshot', '2026-07-31 12:00:00+00')
        """), {"provider_id": provider_id, "match_id": match_id, "bookmaker_id": bookmaker_id,
               "market_id": market_id, "selection_id": selection_id})

    with pytest.raises(IntegrityError):
        with engine.begin() as connection:
            connection.execute(text("""
                INSERT INTO odds_observations (
                    provider_id, match_id, bookmaker_id, market_id, selection_id,
                    odds_value, odds_type, observation_timestamp
                ) VALUES (:provider_id, :match_id, :bookmaker_id, :market_id, :selection_id,
                          2.0, 'snapshot', '2026-07-31 12:01:00+00')
            """), {"provider_id": provider_id, "match_id": match_id, "bookmaker_id": bookmaker_id,
                   "market_id": other_market_id, "selection_id": selection_id})

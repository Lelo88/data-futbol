"""implement approved data model

Revision ID: 20260831_01
Revises:
Create Date: 2026-08-31
"""
from alembic import op


revision = "20260831_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TYPE competition_type AS ENUM
            ('domestic_league', 'domestic_cup', 'continental', 'international', 'other');
        CREATE TYPE match_status AS ENUM
            ('scheduled', 'in_progress', 'completed', 'postponed', 'cancelled', 'abandoned');
        CREATE TYPE match_event_type AS ENUM
            ('goal', 'yellow_card', 'red_card', 'substitution', 'other');
        CREATE TYPE standing_source AS ENUM ('provider', 'derived');
        CREATE TYPE odds_observation_type AS ENUM ('opening', 'closing', 'snapshot');
        CREATE TYPE provider_entity_type AS ENUM
            ('competition', 'season', 'team', 'match', 'bookmaker', 'market', 'selection');

        CREATE FUNCTION set_updated_at() RETURNS trigger AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TABLE providers (
            provider_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            base_url TEXT,
            description TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE competitions (
            competition_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type competition_type NOT NULL,
            country_code CHAR(2),
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT competitions_country_code_format CHECK (country_code IS NULL OR country_code ~ '^[A-Z]{2}$')
        );
        CREATE UNIQUE INDEX competitions_name_type_country_key
            ON competitions (name, type, country_code) NULLS NOT DISTINCT;

        CREATE TABLE seasons (
            season_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            competition_id BIGINT NOT NULL REFERENCES competitions(competition_id),
            season_year INTEGER NOT NULL CHECK (season_year BETWEEN 1800 AND 3000),
            display_name VARCHAR(100),
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT seasons_competition_year_key UNIQUE (competition_id, season_year),
            CONSTRAINT seasons_id_competition_key UNIQUE (season_id, competition_id)
        );

        CREATE TABLE teams (
            team_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            short_name VARCHAR(100),
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE matches (
            match_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            competition_id BIGINT NOT NULL REFERENCES competitions(competition_id),
            season_id BIGINT NOT NULL,
            home_team_id BIGINT NOT NULL REFERENCES teams(team_id),
            away_team_id BIGINT NOT NULL REFERENCES teams(team_id),
            match_date TIMESTAMPTZ NOT NULL,
            match_status match_status NOT NULL,
            home_goals INTEGER CHECK (home_goals IS NULL OR home_goals >= 0),
            away_goals INTEGER CHECK (away_goals IS NULL OR away_goals >= 0),
            home_goals_et INTEGER CHECK (home_goals_et IS NULL OR home_goals_et >= 0),
            away_goals_et INTEGER CHECK (away_goals_et IS NULL OR away_goals_et >= 0),
            extra_time_played BOOLEAN NOT NULL DEFAULT FALSE,
            penalty_shootout_played BOOLEAN NOT NULL DEFAULT FALSE,
            home_penalties INTEGER CHECK (home_penalties IS NULL OR home_penalties >= 0),
            away_penalties INTEGER CHECK (away_penalties IS NULL OR away_penalties >= 0),
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT matches_distinct_teams CHECK (home_team_id <> away_team_id),
            CONSTRAINT matches_extra_time_scores CHECK (
                NOT extra_time_played OR (home_goals_et IS NOT NULL AND away_goals_et IS NOT NULL)
            ),
            CONSTRAINT matches_penalty_scores CHECK (
                NOT penalty_shootout_played OR (home_penalties IS NOT NULL AND away_penalties IS NOT NULL)
            ),
            CONSTRAINT matches_season_competition_fk FOREIGN KEY (season_id, competition_id)
                REFERENCES seasons(season_id, competition_id)
        );

        CREATE TABLE match_events (
            event_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            match_id BIGINT NOT NULL REFERENCES matches(match_id),
            event_type match_event_type NOT NULL,
            team_id BIGINT NOT NULL REFERENCES teams(team_id),
            player_id BIGINT,
            minute INTEGER CHECK (minute IS NULL OR minute >= 0),
            extra_time_minute BOOLEAN,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE FUNCTION ensure_event_team_participates() RETURNS trigger AS $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM matches
                WHERE match_id = NEW.match_id
                  AND NEW.team_id IN (home_team_id, away_team_id)
            ) THEN
                RAISE EXCEPTION 'match event team must participate in its match'
                    USING ERRCODE = '23514';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        CREATE TRIGGER match_events_team_participation
            BEFORE INSERT OR UPDATE OF match_id, team_id ON match_events
            FOR EACH ROW EXECUTE FUNCTION ensure_event_team_participates();

        CREATE TABLE standings (
            standing_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            competition_id BIGINT NOT NULL REFERENCES competitions(competition_id),
            season_id BIGINT NOT NULL,
            team_id BIGINT NOT NULL REFERENCES teams(team_id),
            position INTEGER NOT NULL CHECK (position > 0),
            played INTEGER NOT NULL CHECK (played >= 0),
            wins INTEGER NOT NULL CHECK (wins >= 0),
            draws INTEGER NOT NULL CHECK (draws >= 0),
            losses INTEGER NOT NULL CHECK (losses >= 0),
            goals_for INTEGER NOT NULL CHECK (goals_for >= 0),
            goals_against INTEGER NOT NULL CHECK (goals_against >= 0),
            goal_difference INTEGER NOT NULL,
            points INTEGER NOT NULL CHECK (points >= 0),
            source standing_source NOT NULL,
            snapshot_date TIMESTAMPTZ,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT standings_record_consistency CHECK (
                played = wins + draws + losses AND goal_difference = goals_for - goals_against
            ),
            CONSTRAINT standings_season_competition_fk FOREIGN KEY (season_id, competition_id)
                REFERENCES seasons(season_id, competition_id)
        );
        CREATE UNIQUE INDEX standings_current_snapshot_key
            ON standings (competition_id, season_id, team_id, source) WHERE snapshot_date IS NULL;
        CREATE UNIQUE INDEX standings_historical_snapshot_key
            ON standings (competition_id, season_id, team_id, source, snapshot_date) WHERE snapshot_date IS NOT NULL;

        CREATE TABLE bookmakers (
            bookmaker_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE markets (
            market_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            code VARCHAR(64) NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE selections (
            selection_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            market_id BIGINT NOT NULL REFERENCES markets(market_id),
            code VARCHAR(100) NOT NULL,
            name VARCHAR(255) NOT NULL,
            line_value NUMERIC(6, 2),
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT selections_market_code_key UNIQUE (market_id, code),
            CONSTRAINT selections_id_market_key UNIQUE (selection_id, market_id)
        );

        CREATE TABLE odds_observations (
            observation_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            provider_id BIGINT NOT NULL REFERENCES providers(provider_id),
            match_id BIGINT NOT NULL REFERENCES matches(match_id),
            bookmaker_id BIGINT NOT NULL REFERENCES bookmakers(bookmaker_id),
            market_id BIGINT NOT NULL REFERENCES markets(market_id),
            selection_id BIGINT NOT NULL,
            odds_value NUMERIC(8, 3) NOT NULL CHECK (odds_value > 0),
            odds_type odds_observation_type NOT NULL,
            observation_timestamp TIMESTAMPTZ NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT odds_observations_selection_market_fk FOREIGN KEY (selection_id, market_id)
                REFERENCES selections(selection_id, market_id)
        );

        CREATE TABLE provider_mappings (
            mapping_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            provider_id BIGINT NOT NULL REFERENCES providers(provider_id),
            entity_type provider_entity_type NOT NULL,
            internal_id TEXT NOT NULL,
            external_id TEXT NOT NULL,
            external_url TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT provider_mappings_provider_entity_internal_key UNIQUE (provider_id, entity_type, internal_id),
            CONSTRAINT provider_mappings_provider_entity_external_key UNIQUE (provider_id, entity_type, external_id)
        );

        CREATE INDEX matches_home_team_date_idx ON matches (home_team_id, match_date DESC);
        CREATE INDEX matches_away_team_date_idx ON matches (away_team_id, match_date DESC);
        CREATE INDEX matches_h2h_idx ON matches (home_team_id, away_team_id, match_date DESC);
        CREATE INDEX matches_competition_season_date_idx ON matches (competition_id, season_id, match_date DESC);
        CREATE INDEX matches_date_idx ON matches (match_date DESC);
        CREATE INDEX match_events_match_idx ON match_events (match_id);
        CREATE INDEX standings_competition_season_team_idx ON standings (competition_id, season_id, team_id);
        CREATE INDEX odds_observations_match_bookmaker_market_idx ON odds_observations (match_id, bookmaker_id, market_id);
        CREATE INDEX odds_observations_bookmaker_idx ON odds_observations (bookmaker_id);
        CREATE INDEX odds_observations_market_idx ON odds_observations (market_id);
        CREATE INDEX odds_observations_timestamp_idx ON odds_observations (observation_timestamp DESC);
        CREATE INDEX provider_mappings_external_lookup_idx ON provider_mappings (provider_id, entity_type, external_id);

        CREATE TRIGGER providers_updated_at BEFORE UPDATE ON providers FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER competitions_updated_at BEFORE UPDATE ON competitions FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER seasons_updated_at BEFORE UPDATE ON seasons FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER teams_updated_at BEFORE UPDATE ON teams FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER matches_updated_at BEFORE UPDATE ON matches FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER match_events_updated_at BEFORE UPDATE ON match_events FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER standings_updated_at BEFORE UPDATE ON standings FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER bookmakers_updated_at BEFORE UPDATE ON bookmakers FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER markets_updated_at BEFORE UPDATE ON markets FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER selections_updated_at BEFORE UPDATE ON selections FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER odds_observations_updated_at BEFORE UPDATE ON odds_observations FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        CREATE TRIGGER provider_mappings_updated_at BEFORE UPDATE ON provider_mappings FOR EACH ROW EXECUTE FUNCTION set_updated_at();

        INSERT INTO providers (name, description) VALUES
            ('TheStatsAPI', 'Primary provider for historical football statistics.'),
            ('UK Odds API', 'Secondary provider for betting-market odds.');
        INSERT INTO competitions (name, type, country_code) VALUES
            ('Premier League', 'domestic_league', 'GB'),
            ('La Liga', 'domestic_league', 'ES'),
            ('Bundesliga', 'domestic_league', 'DE'),
            ('Serie A', 'domestic_league', 'IT'),
            ('UEFA Champions League', 'continental', NULL);
        INSERT INTO markets (code, name, description) VALUES
            ('1X2', '1X2', 'Home, draw, or away result.'),
            ('DOUBLE_CHANCE', 'Double Chance', '1X, X2, or 12.'),
            ('GOALS_OVER_UNDER', 'Goals Over/Under', 'Total-goals line market.'),
            ('MOST_CARDS', 'Most Cards', 'Team receiving the most cards.'),
            ('CARDS_OVER_UNDER', 'Cards Over/Under', 'Total-cards line market.');
    """)


def downgrade() -> None:
    op.execute("""
        DROP TABLE provider_mappings;
        DROP TABLE odds_observations;
        DROP TABLE selections;
        DROP TABLE markets;
        DROP TABLE bookmakers;
        DROP TABLE standings;
        DROP TRIGGER match_events_team_participation ON match_events;
        DROP TABLE match_events;
        DROP TABLE matches;
        DROP TABLE teams;
        DROP TABLE seasons;
        DROP INDEX competitions_name_type_country_key;
        DROP TABLE competitions;
        DROP TABLE providers;
        DROP FUNCTION ensure_event_team_participates();
        DROP FUNCTION set_updated_at();
        DROP TYPE provider_entity_type;
        DROP TYPE odds_observation_type;
        DROP TYPE standing_source;
        DROP TYPE match_event_type;
        DROP TYPE match_status;
        DROP TYPE competition_type;
    """)

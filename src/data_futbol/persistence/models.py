"""ORM metadata mirroring the PostgreSQL data-model migration.

Provider payloads and ingestion mappers deliberately do not belong here.
"""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import (
    BigInteger, CheckConstraint, DateTime, Enum, ForeignKey, ForeignKeyConstraint,
    Integer, Numeric, String, Text, UniqueConstraint, text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CompetitionType(StrEnum):
    DOMESTIC_LEAGUE = "domestic_league"
    DOMESTIC_CUP = "domestic_cup"
    CONTINENTAL = "continental"
    INTERNATIONAL = "international"
    OTHER = "other"


class MatchStatus(StrEnum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"
    ABANDONED = "abandoned"


class EventType(StrEnum):
    GOAL = "goal"
    YELLOW_CARD = "yellow_card"
    RED_CARD = "red_card"
    SUBSTITUTION = "substitution"
    OTHER = "other"


class OddsType(StrEnum):
    OPENING = "opening"
    CLOSING = "closing"
    SNAPSHOT = "snapshot"


class StandingSource(StrEnum):
    PROVIDER = "provider"
    DERIVED = "derived"


class ProviderEntityType(StrEnum):
    COMPETITION = "competition"
    SEASON = "season"
    TEAM = "team"
    MATCH = "match"
    BOOKMAKER = "bookmaker"
    MARKET = "market"
    SELECTION = "selection"


class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)


class Provider(Timestamped, Base):
    __tablename__ = "providers"
    provider_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    base_url: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)


class Competition(Timestamped, Base):
    __tablename__ = "competitions"
    competition_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[CompetitionType] = mapped_column(Enum(CompetitionType, name="competition_type"), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(2))


class Season(Timestamped, Base):
    __tablename__ = "seasons"
    __table_args__ = (UniqueConstraint("competition_id", "season_year"), UniqueConstraint("season_id", "competition_id"))
    season_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.competition_id"), nullable=False)
    season_year: Mapped[int] = mapped_column(Integer, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(100))


class Team(Timestamped, Base):
    __tablename__ = "teams"
    team_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    short_name: Mapped[str | None] = mapped_column(String(100))


class Match(Timestamped, Base):
    __tablename__ = "matches"
    __table_args__ = (
        ForeignKeyConstraint(["season_id", "competition_id"], ["seasons.season_id", "seasons.competition_id"]),
        CheckConstraint("home_team_id <> away_team_id", name="matches_distinct_teams"),
    )
    match_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.competition_id"), nullable=False)
    season_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.team_id"), nullable=False)
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.team_id"), nullable=False)
    match_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    match_status: Mapped[MatchStatus] = mapped_column(Enum(MatchStatus, name="match_status"), nullable=False)
    home_goals: Mapped[int | None] = mapped_column(Integer)
    away_goals: Mapped[int | None] = mapped_column(Integer)
    home_goals_et: Mapped[int | None] = mapped_column(Integer)
    away_goals_et: Mapped[int | None] = mapped_column(Integer)
    extra_time_played: Mapped[bool] = mapped_column(nullable=False, server_default=text("false"))
    penalty_shootout_played: Mapped[bool] = mapped_column(nullable=False, server_default=text("false"))
    home_penalties: Mapped[int | None] = mapped_column(Integer)
    away_penalties: Mapped[int | None] = mapped_column(Integer)


class MatchEvent(Timestamped, Base):
    __tablename__ = "match_events"
    event_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.match_id"), nullable=False)
    event_type: Mapped[EventType] = mapped_column(Enum(EventType, name="match_event_type"), nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.team_id"), nullable=False)
    # Player is deliberately not a domain entity in the approved MVP model.
    player_id: Mapped[int | None] = mapped_column(BigInteger)
    minute: Mapped[int | None] = mapped_column(Integer)
    extra_time_minute: Mapped[bool | None]


class Standing(Timestamped, Base):
    __tablename__ = "standings"
    __table_args__ = (
        ForeignKeyConstraint(["season_id", "competition_id"], ["seasons.season_id", "seasons.competition_id"]),
        CheckConstraint("position > 0", name="standings_positive_position"),
        CheckConstraint("played = wins + draws + losses", name="standings_played_consistency"),
        CheckConstraint("goal_difference = goals_for - goals_against", name="standings_goal_difference_consistency"),
    )
    standing_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey("competitions.competition_id"), nullable=False)
    season_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.team_id"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    played: Mapped[int] = mapped_column(Integer, nullable=False)
    wins: Mapped[int] = mapped_column(Integer, nullable=False)
    draws: Mapped[int] = mapped_column(Integer, nullable=False)
    losses: Mapped[int] = mapped_column(Integer, nullable=False)
    goals_for: Mapped[int] = mapped_column(Integer, nullable=False)
    goals_against: Mapped[int] = mapped_column(Integer, nullable=False)
    goal_difference: Mapped[int] = mapped_column(Integer, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[StandingSource] = mapped_column(Enum(StandingSource, name="standing_source"), nullable=False)
    snapshot_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Bookmaker(Timestamped, Base):
    __tablename__ = "bookmakers"
    bookmaker_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)


class Market(Timestamped, Base):
    __tablename__ = "markets"
    market_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class Selection(Timestamped, Base):
    __tablename__ = "selections"
    __table_args__ = (UniqueConstraint("market_id", "code"), UniqueConstraint("selection_id", "market_id"))
    selection_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    market_id: Mapped[int] = mapped_column(ForeignKey("markets.market_id"), nullable=False)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    line_value: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))


class OddsObservation(Timestamped, Base):
    __tablename__ = "odds_observations"
    __table_args__ = (
        ForeignKeyConstraint(["selection_id", "market_id"], ["selections.selection_id", "selections.market_id"]),
        CheckConstraint("odds_value > 0", name="odds_observations_positive_value"),
    )
    observation_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.provider_id"), nullable=False)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.match_id"), nullable=False)
    bookmaker_id: Mapped[int] = mapped_column(ForeignKey("bookmakers.bookmaker_id"), nullable=False)
    market_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    selection_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    odds_value: Mapped[Decimal] = mapped_column(Numeric(8, 3), nullable=False)
    odds_type: Mapped[OddsType] = mapped_column(Enum(OddsType, name="odds_observation_type"), nullable=False)
    observation_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ProviderMapping(Timestamped, Base):
    __tablename__ = "provider_mappings"
    __table_args__ = (
        UniqueConstraint("provider_id", "entity_type", "internal_id"),
        UniqueConstraint("provider_id", "entity_type", "external_id"),
    )
    mapping_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.provider_id"), nullable=False)
    entity_type: Mapped[ProviderEntityType] = mapped_column(Enum(ProviderEntityType, name="provider_entity_type"), nullable=False)
    internal_id: Mapped[str] = mapped_column(Text, nullable=False)
    external_id: Mapped[str] = mapped_column(Text, nullable=False)
    external_url: Mapped[str | None] = mapped_column(Text)

.PHONY: db-up db-down migrate test

db-up:
	docker compose up -d postgres

db-down:
	docker compose down

migrate:
	alembic upgrade head

test:
	pytest

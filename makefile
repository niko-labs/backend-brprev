docker-up:
	docker-compose -f ./.infra/docker/docker-compose.yaml --env-file ./.env up -d --build

docker-down:
	docker-compose -f ./.infra/docker/docker-compose.yaml --env-file ./.env down --remove-orphans --volumes

docker-db-up:
	docker-compose -f ./.infra/docker/docker-compose.yaml --env-file ./.env up -d db
	
docker-db-down:
	docker-compose -f ./.infra/docker/docker-compose.yaml --env-file ./.env down db


migration-create:
	@cd ./.infra/migracoes && alembic revision --autogenerate -m $(name)

migration-upgrade:
	@cd ./.infra/migracoes && alembic upgrade head

migration-downgrade:
	@cd ./.infra/migracoes && alembic downgrade -1

migration-history:
	@cd ./.infra/migracoes && alembic history


run-tests:
	@pytest



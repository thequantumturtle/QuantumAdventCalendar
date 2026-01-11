# Makefile shortcuts for local Docker workflows
.PHONY: up down test-local

up:
	docker-compose up -d --build

down:
	docker-compose down -v

test-local: up
	bash ./scripts/test-local.sh

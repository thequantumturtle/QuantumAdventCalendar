# Makefile shortcuts for local Docker workflows
.PHONY: up down test-local

up:
	docker-compose up -d --build

down:
	docker-compose down -v

test-local: up
	bash ./scripts/test-local.sh

ci-local: up
	@echo "Running Docker-first CI checks..."
	@echo "Running backend tests..."
	@docker-compose exec -T backend pytest -q || (echo "Backend tests failed"; docker-compose down -v; exit 1)
	@echo "Building frontend..."
	@docker-compose exec -T frontend sh -c "npm run build" || (echo "Frontend build failed"; docker-compose down -v; exit 1)
	@echo "ci-local completed."

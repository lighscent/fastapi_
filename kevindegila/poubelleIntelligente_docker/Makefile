# ============================
#        COMMANDES DEV
# ============================

dev:
    docker compose -f docker-compose.dev.yml up --build

dev-down:
    docker compose -f docker-compose.dev.yml down

dev-restart:
    docker compose -f docker-compose.dev.yml down
    docker compose -f docker-compose.dev.yml up --build

# ============================
#       COMMANDES PROD
# ============================

prod:
    docker compose -f docker-compose.prod.yml up --build -d

prod-down:
    docker compose -f docker-compose.prod.yml down

prod-restart:
    docker compose -f docker-compose.prod.yml down
    docker compose -f docker-compose.prod.yml up --build -d

# ============================
#        OUTILS PRATIQUES
# ============================

logs:
    docker compose logs -f

ps:
    docker compose ps

clean:
    docker system prune -f

rebuild:
    docker compose -f docker-compose.dev.yml build --no-cache


ok:
	@echo "All commands are set up. Use 'make dev', 'make prod', etc. to manage the application."

@REM D‚marrage de d‚v avec Docker

@echo off

cd kevindegila/poubelleIntelligente_docker

if "%1"=="dev" (
    docker compose -f docker-compose.dev.yml up --build
    exit /b
)

if "%1"=="dev-down" (
    docker compose -f docker-compose.dev.yml down
    exit /b
)

if "%1"=="dev-restart" (
    docker compose -f docker-compose.dev.yml down
    docker compose -f docker-compose.dev.yml up --build
    exit /b
)

if "%1"=="prod" (
    docker compose -f docker-compose.prod.yml up --build -d
    exit /b
)

if "%1"=="prod-down" (
    docker compose -f docker-compose.prod.yml down
    exit /b
)

if "%1"=="prod-restart" (
    docker compose -f docker-compose.prod.yml down
    docker compose -f docker-compose.prod.yml up --build -d
    exit /b
)

if "%1"=="logs" (
    docker compose logs -f
    exit /b
)

if "%1"=="clean" (
    docker system prune -f
    exit /b
)

if "%1"=="ok1" (
    echo Ok1
    exit /b
)

if "%1"=="ok2" (
    echo Ok2
    exit /b
)

echo Commande inconnue.
echo.
echo Commandes disponibles :
echo   start dev
echo   start dev-down
echo   start dev-restart
echo   start prod
echo   start prod-down
echo   start prod-restart
echo   start logs
echo   start clean
echo   start ok
echo.
echo Docker-desktop doit ˆtre d‚marr‚ avant d'ex‚cuter ce script.

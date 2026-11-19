@echo off
TITLE Clarity Website - Dev Launch
setlocal

set DOCKER_BUILDKIT=1
set COMPOSE_DOCKER_CLI_BUILD=1

echo ============================================================
echo   CLARITY WEBSITE - DEV ENVIRONMENT
echo ============================================================
echo.
echo URL: http://localhost:8007
echo Note: Code is volume-mounted; code edits reload live.
echo Run "launch.bat --build" only when requirements change.
echo.

if "%1"=="--build" (
    echo [INFO] Rebuilding with BuildKit cache...
    docker compose -f docker-compose.dev.yml up --build
) else if "%1"=="-b" (
    echo [INFO] Rebuilding with BuildKit cache...
    docker compose -f docker-compose.dev.yml up --build
) else (
    echo [INFO] Starting containers (using cached image)...
    docker compose -f docker-compose.dev.yml up
)

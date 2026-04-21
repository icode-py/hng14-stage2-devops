#!/bin/bash
set -e

echo "🚀 Starting rolling update deployment..."

# Use 'docker compose' (without hyphen) for newer Docker versions
DOCKER_COMPOSE="docker compose"

# Pull latest images
$DOCKER_COMPOSE pull

# For API and Frontend (services with ports), we need special handling
# For Worker (no ports), standard rolling update works

echo "Updating worker..."
$DOCKER_COMPOSE up -d --no-deps --scale worker=2 --no-recreate worker
sleep 5
$DOCKER_COMPOSE up -d --no-deps --scale worker=1 --no-recreate worker
echo "✅ Worker updated"

echo "Updating api..."
# For API, stop old one first since port 8000 is fixed
$DOCKER_COMPOSE stop api
$DOCKER_COMPOSE up -d --no-deps api
echo "✅ API updated"

echo "Updating frontend..."
# For frontend, stop old one first since port 3000 is fixed
$DOCKER_COMPOSE stop frontend
$DOCKER_COMPOSE up -d --no-deps frontend
echo "✅ Frontend updated"

# Verify all services are healthy
echo "Waiting for services to be healthy..."
sleep 10

if $DOCKER_COMPOSE ps | grep -q "unhealthy"; then
    echo "❌ Some services are unhealthy"
    $DOCKER_COMPOSE ps
    exit 1
fi

echo "🎉 Rolling update complete!"
$DOCKER_COMPOSE ps
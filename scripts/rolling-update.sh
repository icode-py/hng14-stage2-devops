#!/bin/bash
set -e

echo "🚀 Starting rolling update deployment..."

# Use 'docker compose' (without hyphen) for newer Docker versions
DOCKER_COMPOSE="docker compose"

# Pull latest images
$DOCKER_COMPOSE pull

# Update each service with health check verification
for SERVICE in api worker frontend; do
    echo "Updating $SERVICE..."
    
    # Get current container ID
    OLD_CONTAINER=$($DOCKER_COMPOSE ps -q $SERVICE)
    
    # Start new container
    $DOCKER_COMPOSE up -d --no-deps --scale $SERVICE=2 --no-recreate $SERVICE
    
    # Wait for new container to be healthy
    echo "Waiting for new $SERVICE container to be healthy..."
    for i in {1..60}; do
        NEW_CONTAINER=$($DOCKER_COMPOSE ps -q $SERVICE | grep -v $OLD_CONTAINER | head -1)
        HEALTH=$(docker inspect --format='{{.State.Health.Status}}' $NEW_CONTAINER 2>/dev/null || echo "starting")
        if [ "$HEALTH" = "healthy" ]; then
            echo "✅ New $SERVICE container is healthy"
            break
        fi
        if [ $i -eq 60 ]; then
            echo "❌ New $SERVICE container failed health check, aborting..."
            docker stop $NEW_CONTAINER
            docker rm $NEW_CONTAINER
            exit 1
        fi
        sleep 1
    done
    
    # Stop old container
    if [ -n "$OLD_CONTAINER" ]; then
        docker stop $OLD_CONTAINER
        docker rm $OLD_CONTAINER
    fi
    
    # Scale back to 1
    $DOCKER_COMPOSE up -d --no-deps --scale $SERVICE=1 --no-recreate $SERVICE
    
    echo "✅ $SERVICE updated successfully"
done

echo "🎉 Rolling update complete!"
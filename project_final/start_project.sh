#!/bin/bash

echo "🚀 Starting Data Engineering Project..."
echo "======================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if ports are available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use. Please free up port $1 first."
        exit 1
    fi
}

echo "🔍 Checking port availability..."
check_port 3000  # Dagster
check_port 8080  # Kafka UI
check_port 9092  # Kafka
check_port 5432  # PostgreSQL

echo "✅ Ports are available"

# Start services
echo "🐳 Starting Docker services..."
docker compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service status
echo "📊 Checking service status..."
docker compose ps

echo ""
echo "🎉 Project started successfully!"
echo ""
echo "📱 Access points:"
echo "   Dagster UI: http://localhost:3000"
echo "   Kafka UI:   http://localhost:8080"
echo "   PostgreSQL: localhost:5432"
echo ""
echo "📋 Useful commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart:       docker-compose restart"
echo ""
echo "🔍 To monitor the pipeline:"
echo "   1. Open Dagster UI at http://localhost:3000"
echo "   2. Navigate to Assets"
echo "   3. Click 'Materialize' to run the pipeline manually"
echo ""
echo "📚 For more information, see README.md"

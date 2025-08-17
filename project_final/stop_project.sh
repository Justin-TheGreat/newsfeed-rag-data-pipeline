#!/bin/bash

echo "🛑 Stopping Data Engineering Project..."
echo "======================================"

# Stop all services
echo "🐳 Stopping Docker services..."
docker compose down

echo "🧹 Cleaning up..."
docker system prune -f

echo ""
echo "✅ Project stopped successfully!"
echo ""
echo "💡 To start again, run: ./start_project.sh"

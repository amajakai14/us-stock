#!/bin/bash

# US Stock Data Collection System - Development Setup Script

echo "🚀 Setting up US Stock Data Collection System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Build and start services
echo "📦 Building and starting services..."
docker-compose up -d --build

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Initialize sample data
echo "📊 Initializing sample data..."
docker-compose exec -T backend python init_sample_data.py

# Check if services are healthy
echo "🔍 Checking service health..."

# Check backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend is not responding"
fi

# Check frontend (it might take longer to start)
echo "⏳ Waiting for frontend to start..."
sleep 15

if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is healthy"
else
    echo "⚠️ Frontend might still be starting (this is normal)"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📱 Access your applications:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "🔧 Development commands:"
echo "   View logs: docker-compose logs -f [backend|frontend|postgres]"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo ""
echo "📚 Next steps:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Browse the company discovery interface"
echo "   3. Select some companies for tracking"
echo "   4. Check the API documentation at http://localhost:8000/docs"
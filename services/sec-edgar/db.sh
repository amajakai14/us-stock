#!/bin/bash

# US Stock Data Collection Database Management Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/docker-compose.db.yml"

function show_help() {
    echo "US Stock Data Collection Database Management"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start     Start PostgreSQL database"
    echo "  stop      Stop PostgreSQL database"
    echo "  restart   Restart PostgreSQL database"
    echo "  status    Show database status"
    echo "  logs      Show database logs"
    echo "  connect   Connect to database with psql"
    echo "  reset     Reset database (delete all data)"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start          # Start the database"
    echo "  $0 logs           # View logs"
    echo "  $0 connect        # Connect with psql"
}

function start_db() {
    echo "🚀 Starting PostgreSQL database..."
    docker-compose -f "$COMPOSE_FILE" up -d
    echo "✅ Database started successfully!"
    echo "📊 Database is available at: postgresql://postgres:postgres@localhost:5432/us_stock_data"
    echo ""
    echo "⏳ Waiting for database to be ready..."
    sleep 5

    # Check if database is ready
    if docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U postgres -d us_stock_data > /dev/null 2>&1; then
        echo "✅ Database is ready for connections!"
    else
        echo "⏳ Database is still starting up..."
        echo "Run '$0 status' to check readiness"
    fi
}

function stop_db() {
    echo "🛑 Stopping PostgreSQL database..."
    docker-compose -f "$COMPOSE_FILE" down
    echo "✅ Database stopped successfully!"
}

function restart_db() {
    echo "🔄 Restarting PostgreSQL database..."
    stop_db
    sleep 2
    start_db
}

function show_status() {
    echo "📊 PostgreSQL Database Status:"
    echo ""

    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        echo "✅ Database is running"

        # Check health
        if docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U postgres -d us_stock_data > /dev/null 2>&1; then
            echo "✅ Database is healthy and ready for connections"
        else
            echo "⏳ Database is running but not ready yet"
        fi

        echo ""
        echo "📋 Container Details:"
        docker-compose -f "$COMPOSE_FILE" ps
    else
        echo "❌ Database is not running"
    fi

    echo ""
    echo "🔗 Connection String:"
    echo "   postgresql://postgres:postgres@localhost:5432/us_stock_data"
}

function show_logs() {
    echo "📋 PostgreSQL Database Logs:"
    echo ""
    docker-compose -f "$COMPOSE_FILE" logs -f postgres
}

function connect_db() {
    echo "🔌 Connecting to PostgreSQL database..."
    docker-compose -f "$COMPOSE_FILE" exec postgres psql -U postgres -d us_stock_data
}

function reset_db() {
    echo "⚠️  This will delete ALL data in the database!"
    read -p "Are you sure you want to continue? (yes/no): " confirm

    if [ "$confirm" = "yes" ]; then
        echo "🗑️  Resetting database..."
        stop_db
        docker volume rm us-stock-data-collection_postgres_data 2>/dev/null || true
        echo "✅ Database reset successfully!"
        echo ""
        echo "💡 Run '$0 start' to create a fresh database"
    else
        echo "❌ Database reset cancelled"
    fi
}

# Parse command
case "${1:-help}" in
    start)
        start_db
        ;;
    stop)
        stop_db
        ;;
    restart)
        restart_db
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    connect)
        connect_db
        ;;
    reset)
        reset_db
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
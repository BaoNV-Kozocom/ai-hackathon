#!/bin/bash

# Start all services in parallel
echo "Starting all services..."
echo "================================"

# Start Laravel backend in background
echo "Starting Laravel backend..."
php artisan serve &
BACKEND_PID=$!

# Start frontend dev server in background
echo "Starting frontend dev server..."
npm run dev &
FRONTEND_PID=$!

# Start Python app in background
echo "Starting Python app..."
cd python && python app.py &
PYTHON_PID=$!

echo "================================"
echo "All services started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Python PID: $PYTHON_PID"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for Ctrl+C
trap "echo 'Stopping all services...'; kill $BACKEND_PID $FRONTEND_PID $PYTHON_PID 2>/dev/null; exit" INT

# Keep script running
wait

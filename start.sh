#!/bin/bash

echo "========================================"
echo "  Skills Gap Analysis - Single URL Setup"
echo "========================================"
echo ""
echo "Building frontend..."
cd frontend
npm install
npm run build
echo ""
echo "Frontend build completed!"
echo ""
echo "Starting backend server on http://localhost:8000"
echo "Frontend + Backend running together!"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

cd ../backend
python app.py

@echo off
echo ========================================
echo   Skills Gap Analysis - Hybrid Setup
echo ========================================
echo.

echo Starting Node.js Assessment Service (Port 5000)...
cd backend
start "Node.js Assessment Service" cmd /k "npm install && node server.js"
echo.

echo Starting Python Backend (Port 8000)...
start "Python Backend" cmd /k "pip install -r requirements.txt && python app.py"
echo.

echo Starting Frontend (Port 3000)...
cd ../frontend
start "Frontend" cmd /k "npm install && npm start"
echo.

echo ========================================
echo All services are starting...
echo Frontend will open in your default browser.
echo ========================================
pause

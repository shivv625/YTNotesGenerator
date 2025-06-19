@echo off
echo Starting YouTube Notes Generator...
echo.

echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python -c \"import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)\""

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo Servers are starting...
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:5173
echo.
echo Press any key to exit this window...
pause > nul 
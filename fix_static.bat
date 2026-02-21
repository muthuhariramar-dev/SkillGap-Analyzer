@echo off
echo ========================================
echo   Complete Static File Fix
echo ========================================
echo.

echo 1. Checking React build files...
cd frontend
if not exist "build\static\css" (
    echo ERROR: CSS directory not found
    echo Building React app...
    npm run build
) else (
    echo CSS directory found
)

if not exist "build\static\js" (
    echo ERROR: JS directory not found
    echo Building React app...
    npm run build
) else (
    echo JS directory found
)

echo.
echo 2. Listing static files...
echo CSS files:
dir "build\static\css\*.css" /b
echo.
echo JS files:
dir "build\static\js\*.js" /b
echo.

echo 3. Starting Flask backend with fixed static serving...
cd ..\backend

echo.
echo Starting server...
python -c "
import os
from flask import Flask, send_from_directory

app = Flask(__name__)

BUILD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))
STATIC_DIR = os.path.join(BUILD_DIR, 'static')

print(f'BUILD_DIR: {BUILD_DIR}')
print(f'STATIC_DIR: {STATIC_DIR}')

@app.route('/static/<path:filename>')
def serve_static(filename):
    try:
        file_path = os.path.join(STATIC_DIR, filename)
        print(f'Serving: {filename} from {file_path}')
        if os.path.exists(file_path):
            return send_from_directory(STATIC_DIR, filename)
        else:
            return f'File not found: {filename}', 404
    except Exception as e:
        return f'Error: {str(e)}', 500

@app.route('/')
def serve_index():
    return send_from_directory(BUILD_DIR, 'index.html')

@app.route('/<path:path>')
def serve_react(path):
    try:
        file_path = os.path.join(BUILD_DIR, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_from_directory(BUILD_DIR, path)
        else:
            return send_from_directory(BUILD_DIR, 'index.html')
    except:
        return send_from_directory(BUILD_DIR, 'index.html')

if __name__ == '__main__':
    print('Starting Flask server...')
    print('Static files will be served from:', STATIC_DIR)
    app.run(host='0.0.0.0', port=8000, debug=True)
"

pause

import os
from flask import Flask, send_from_directory, jsonify

app = Flask(__name__)

# Build directory
BUILD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Skills-Gap-Analysis-with-Generative-AI-main', 'frontend', 'build'))
STATIC_DIR = os.path.join(BUILD_DIR, 'static')

print(f'BUILD_DIR: {BUILD_DIR}')
print(f'STATIC_DIR: {STATIC_DIR}')
print(f'BUILD_DIR exists: {os.path.exists(BUILD_DIR)}')
print(f'STATIC_DIR exists: {os.path.exists(STATIC_DIR)}')

# List static files
if os.path.exists(STATIC_DIR):
    print('Available static files:')
    for root, dirs, files in os.walk(STATIC_DIR):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), STATIC_DIR)
            print(f'  {rel_path}')

@app.route('/static/<path:filename>')
def serve_static(filename):
    try:
        static_dir = os.path.join(BUILD_DIR, 'static')
        file_path = os.path.join(static_dir, filename)
        
        print(f"=== STATIC REQUEST ===")
        print(f"Filename: {filename}")
        print(f"BUILD_DIR: {BUILD_DIR}")
        print(f"Static dir: {static_dir}")
        print(f"Full path: {file_path}")
        print(f"Exists: {os.path.exists(file_path)}")
        
        if os.path.exists(file_path):
            print(f"✅ Found and serving: {filename}")
            response = send_from_directory(static_dir, filename)
            # Add cache control headers to prevent browser caching
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            print(f"❌ Not found: {filename}")
            return jsonify({"error": f"File not found: {filename}"}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/')
def serve_index():
    try:
        return send_from_directory(BUILD_DIR, 'index.html')
    except Exception as e:
        return f'Error: {str(e)}', 500

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

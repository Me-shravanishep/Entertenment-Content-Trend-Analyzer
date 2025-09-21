import os
import sys
import subprocess
import threading
import time
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_backend():
    print("Starting Backend Server...")
    from backend.app import create_app
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def run_frontend():
    print("Starting Frontend Dashboard...")
    time.sleep(3)
    script_path = project_root / "frontend" / "streamlit_app.py"
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        str(script_path), 
        "--server.port", "8501"
    ])

def main():
    print("Entertainment Content Trend Analyzer")
    print("=" * 50)
    
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('data/exports', exist_ok=True)
    
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\nShutting down application...")
        sys.exit(0)

if __name__ == "__main__":
    main()
Entertainment Trend Analyzer — Setup Guide (Windows)

Overview:
- Backend: Flask API on http://127.0.0.1:5000
- Frontend: Streamlit app on http://127.0.0.1:8501
- Storage: SQLite at `data/trends.db`
- Mock data: YouTube/Instagram services return demo data by default (no API keys required). Real APIs use env keys.

Prerequisites:
- Python 3.10–3.13 installed and on PATH (py -V)
- PowerShell (default on Windows)

1) Clone and open project:
- Ensure the working folder is `entertainment-trend-analyzer/` that contains `run.py`.

2) Create and activate a virtual environment:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Upgrade pip and install dependencies:
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4) Initialize environment variables:
- Copy `.env.example` to `.env` and edit values as needed.
```powershell
Copy-Item .env.example .env
```
- Optional: Set `YOUTUBE_API_KEY` and `INSTAGRAM_ACCESS_TOKEN` for live data. Mock data works without them.

5) First run (creates data folders/DB automatically):
```powershell
python run.py
```
- Open Streamlit: http://127.0.0.1:8501
- Backend health: http://127.0.0.1:5000/api/health

6) Project structure (key paths):
- `backend/app.py`: Flask app factory and routes registration
- `backend/routes/*`: API endpoints (data and analytics)
- `backend/services/*`: Platform collectors (mocked)
- `backend/utils/*`: DB and helpers
- `frontend/streamlit_app.py`: Streamlit UI
- `config/settings.py`: Loads `.env` and validates config
- `data/`: SQLite DB and exports

7) Running tests (optional quick checks):
```powershell
python test_backend.py
python test_full_system.py
```

Troubleshooting:
- Port in use: If 5000 or 8501 are busy, stop other apps or change ports.
	- Change backend port by editing `run.py` (Flask `app.run(port=5000)`).
	- Change frontend port via `--server.port` in `run.py` Streamlit command.
- Activate venv error: Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in an elevated PowerShell once, then re-activate.
- Missing packages: Re-run `pip install -r requirements.txt` inside the activated venv.
- Backend Disconnected in UI: Ensure `python run.py` is running; check `http://127.0.0.1:5000/api/health` returns 200.
- TextBlob extra data: TextBlob works out of the box here; if you later use advanced features needing corpora, install `textblob-data`.

Environment variables (.env):
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Default `sqlite:///data/trends.db`
- `YOUTUBE_API_KEY`: Optional for real YouTube API
- `INSTAGRAM_ACCESS_TOKEN`: Optional for real Instagram API
- `MCP_ENABLED`, `MCP_MODEL`, `MCP_CONTEXT_SIZE`: MCP tuning

Uninstall/reset (optional):
```powershell
Deactivate; Remove-Item -Recurse -Force .\.venv
Remove-Item -Recurse -Force .\data
```

Quick Start:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```


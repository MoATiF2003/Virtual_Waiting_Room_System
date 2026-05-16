# Virtual Waiting Room (VWR)

A simple FastAPI-based virtual waiting room prototype with a browser dashboard.
It admits users into a limited-capacity session manager and places excess requests into a waiting queue.

## Features

- FastAPI backend with HTML dashboard served via `Jinja2Templates`
- Active session management with automatic expiration after 5 minutes
- Waiting queue using `collections.deque`
- Automatic queue processing on startup
- Real-time dashboard updates every 5 seconds
- Simple form-based user access request flow

## Architecture

- `main.py`: FastAPI app definition, static file mounting, template rendering, and endpoint definitions.
- `models/gateway.py`: Central gateway logic for admitting users, queue processing, and dashboard aggregation.
- `models/session_manager.py`: Manages active sessions and removes expired users.
- `models/waiting_queue.py`: Holds queued users and admits them when capacity frees up.
- `models/user.py`: User object with session timing and state.
- `frontend/index.html`: Dashboard UI for submitting a user ID and viewing system status.
- `static/style.css`: Basic dashboard styling.

## How it works

1. A user submits an access request via the dashboard form.
2. `Gateway.request_access()` either admits the user immediately or places them in the waiting queue.
3. The session manager tracks active users and expires them after 5 minutes.
4. The gateway auto-processes the queue every 10 seconds and admits up to 2 queued users when capacity is available.
5. The dashboard polls `/dashboard-data` every 5 seconds to show current active users and waiting queue details.

## Requirements

- Python 3.8+
- `fastapi`
- `uvicorn`
- `jinja2`
- `python-multipart`

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Running the app

From the `VWR` folder:

```powershell
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000` in your browser.

## API Endpoints

- `GET /` - Dashboard page
- `POST /request-access` - Submit a user ID for access
- `GET /status/{user_id}` - Check a user’s current status
- `GET /dashboard-data` - Retrieve dashboard data for active users and queued users

## Default configuration

- `Gateway(max_capacity=10, admit_rate=2, session_timeout=5)` in `main.py`
- Queue processing interval: 10 seconds
- Dashboard refresh interval: 5 seconds

## Project structure

```
VWR/
  main.py
  README.md
  requirements.txt
  frontend/
    index.html
  static/
    style.css
  models/
    gateway.py
    session_manager.py
    user.py
    waiting_queue.py
```

## Notes

- This implementation is intended as a prototype/demo and does not include persistence or authentication.
- User IDs are stored in memory only for the current process lifetime.
- The waiting queue and active session logic are designed for simple simulation, not production use.

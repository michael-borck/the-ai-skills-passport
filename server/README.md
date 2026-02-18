# AI Skills Passport - Progress Tracker

Minimal FastAPI server for tracking experience completions.

## Setup

```bash
cd server
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Or with auto-reload for development:
```bash
uvicorn app:app --host 0.0.0.0 --port 5050 --reload
```

## Interactive Docs

Open **http://localhost:5050/docs** for Swagger UI - test endpoints directly in the browser.

## Endpoints

### POST /complete
Record a completion.

```bash
curl -X POST http://localhost:5050/complete \
  -H "Content-Type: application/json" \
  -d '{"uid": "staff123", "experience": "is-this-ai"}'
```

### GET /progress/{uid}
Get user's progress and badges.

```bash
curl http://localhost:5050/progress/staff123
```

Response:
```json
{
  "uid": "staff123",
  "completions": {
    "is-this-ai": "2026-02-18T10:30:00"
  },
  "completed_count": 1,
  "total_experiences": 5,
  "badges": [
    {"id": "explorer", "emoji": "🧪", "name": "Explorer", "requirement": 1}
  ]
}
```

## Valid Experiences

- `is-this-ai`
- `what-would-you-do`
- `rules-of-engagement`
- `ai-proof-assessments`
- `teaching-with-ai`

## Production

For internal Curtin network:
1. Run on your desktop machine
2. Find your IP: `ipconfig` (Windows) or `ifconfig` (Mac)
3. Access at `http://YOUR_IP:5050`
4. Update SPA completion URLs to point to this server

# Progress Tracker API

The progress tracker is a lightweight FastAPI server (`server/app.py`) that records experience completions and manages AI in 5 subscriptions. It uses SQLite for storage and provides interactive API documentation via Swagger UI.

## Quick Start

```bash
cd server
pip install -r requirements.txt
python app.py
```

The server starts on port **5050**. Open [http://localhost:5050/docs](http://localhost:5050/docs) for interactive Swagger UI documentation.

## Configuration

| Setting | Value |
|---|---|
| Port | 5050 |
| Database | `server/completions.db` (SQLite, created automatically) |
| CORS | All origins allowed (for SPA cross-origin requests) |

## Endpoints

### Health Check

```
GET /health
```

Returns server status. Useful for monitoring and SPA connectivity checks.

**Response:**
```json
{
  "status": "ok",
  "service": "ai-skills-passport"
}
```

---

### Record Completion

```
POST /complete
```

Records that a user has completed an experience. If the user has already completed the experience, the record is updated (upsert).

**Request body:**
```json
{
  "uid": "string",
  "experience": "is-this-ai"
}
```

| Field | Type | Description |
|---|---|---|
| `uid` | string | Blackboard UID passed via URL variable substitution |
| `experience` | enum | One of the valid experience slugs (see below) |

**Valid experience slugs:**
- `is-this-ai`
- `what-would-you-do`
- `rules-of-engagement`
- `ai-proof-assessments`
- `teaching-with-ai`
- `working-with-copilot`
- `researching-with-ai`

**Response:**
```json
{
  "success": true,
  "uid": "borckm",
  "experience": "is-this-ai"
}
```

---

### Get Progress

```
GET /progress/{uid}
```

Returns a user's completed experiences and earned badges.

**Path parameters:**

| Parameter | Type | Description |
|---|---|---|
| `uid` | string | Blackboard UID |

**Response:**
```json
{
  "uid": "borckm",
  "completions": {
    "is-this-ai": "2026-03-01T10:30:00",
    "what-would-you-do": "2026-03-02T14:15:00",
    "rules-of-engagement": "2026-03-03T09:00:00"
  },
  "completed_count": 3,
  "total_experiences": 7,
  "badges": [
    {"id": "explorer", "emoji": "🧪", "name": "Explorer", "requirement": 1},
    {"id": "thinker", "emoji": "🧠", "name": "Thinker", "requirement": 3}
  ]
}
```

**Badge tiers:**

| Badge | Emoji | Requirement |
|---|---|---|
| Explorer | 🧪 | 1 experience completed |
| Thinker | 🧠 | 3 experiences completed |
| Builder | 🛠️ | 5 experiences completed |
| Champion | 🏆 | 7 experiences completed (all) |

---

### Subscribe to AI in 5

```
POST /subscribe
```

Subscribes an email address to the AI in 5 weekly micro-challenges.

**Request body:**
```json
{
  "email": "name@curtin.edu.au"
}
```

**Response:**
```json
{
  "success": true,
  "email": "name@curtin.edu.au",
  "status": "subscribed"
}
```

**Error (400):** Returns error if email is invalid (missing `@`).

---

### Unsubscribe from AI in 5

```
POST /unsubscribe
```

Unsubscribes an email (sets `active = 0`; record is retained).

**Request body:**
```json
{
  "email": "name@curtin.edu.au"
}
```

**Response:**
```json
{
  "success": true,
  "email": "name@curtin.edu.au",
  "status": "unsubscribed"
}
```

---

### List Subscribers

```
GET /subscribers
```

Returns the count of active AI in 5 subscribers.

**Response:**
```json
{
  "active_subscribers": 42
}
```

---

### Export Subscribers

```
GET /subscribers/export
```

Downloads active subscribers as a CSV file. Useful for the email sending script.

**Response:** CSV file download with columns `email`, `subscribed_at`.

## Database Schema

The server creates two tables automatically on startup:

### `completions`

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Primary key, auto-increment |
| `uid` | TEXT | Blackboard UID (indexed) |
| `experience` | TEXT | Experience slug |
| `completed_at` | TEXT | ISO 8601 timestamp |

Unique constraint on `(uid, experience)` — one record per user per experience.

### `subscribers`

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER | Primary key, auto-increment |
| `email` | TEXT | Unique |
| `subscribed_at` | TEXT | ISO 8601 timestamp |
| `active` | INTEGER | 1 = subscribed, 0 = unsubscribed |

## Data Governance

**Important:** This server stores Blackboard UIDs which are personally identifiable. Before deploying with real user data, consult [Data Governance](data-governance.md) for the privacy considerations and approval steps required.

## Related Documents

- [Data Governance](data-governance.md) — privacy and data governance considerations
- [SPA Integration Guide](spa-integration-guide.md) — how to connect SPAs to this server
- [Deployment Guide](deployment-guide.md) — build and deploy instructions

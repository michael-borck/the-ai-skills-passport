"""
AI Skills Passport - Progress Tracker & Subscriptions (FastAPI)
Run: uvicorn app:app --host 0.0.0.0 --port 5050 --reload
Docs: http://localhost:5050/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Literal
import sqlite3
import io
import csv
from datetime import datetime
import os

app = FastAPI(
    title="AI Skills Passport",
    description="Track experience completions, badges, and AI in 5 subscriptions",
    version="1.1"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = os.path.join(os.path.dirname(__file__), "completions.db")

EXPERIENCES = ["is-this-ai", "what-would-you-do", "rules-of-engagement", "ai-proof-assessments", "teaching-with-ai"]
BADGES = [
    {"id": "explorer", "emoji": "🧪", "name": "Explorer", "requirement": 1},
    {"id": "thinker", "emoji": "🧠", "name": "Thinker", "requirement": 3},
    {"id": "builder", "emoji": "🛠️", "name": "Builder", "requirement": 5},
]

ExperienceType = Literal["is-this-ai", "what-would-you-do", "rules-of-engagement", "ai-proof-assessments", "teaching-with-ai"]


class CompletionRequest(BaseModel):
    uid: str
    experience: ExperienceType


class SubscribeRequest(BaseModel):
    email: str


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.on_event("startup")
def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT NOT NULL,
                experience TEXT NOT NULL,
                completed_at TEXT NOT NULL,
                UNIQUE(uid, experience)
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_uid ON completions(uid)")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                subscribed_at TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1
            )
        """)
    print(f"✓ Database ready: {DB_PATH}")


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-skills-passport"}


@app.post("/complete")
def record_completion(req: CompletionRequest):
    """Record an experience completion"""
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO completions (uid, experience, completed_at) VALUES (?, ?, ?)",
            (req.uid, req.experience, datetime.utcnow().isoformat())
        )
    return {"success": True, "uid": req.uid, "experience": req.experience}


@app.get("/progress/{uid}")
def get_progress(uid: str):
    """Get user's progress and earned badges"""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT experience, completed_at FROM completions WHERE uid = ?", (uid,)
        ).fetchall()

    completions = {row["experience"]: row["completed_at"] for row in rows}
    completed_count = len(completions)
    earned_badges = [b for b in BADGES if completed_count >= b["requirement"]]

    return {
        "uid": uid,
        "completions": completions,
        "completed_count": completed_count,
        "total_experiences": len(EXPERIENCES),
        "badges": earned_badges,
    }


# ---------------------------------------------------------------------------
# AI in 5 — Subscriptions
# ---------------------------------------------------------------------------


@app.post("/subscribe")
def subscribe(req: SubscribeRequest):
    """Subscribe an email to AI in 5"""
    email = req.email.strip().lower()
    if "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email address")
    with get_db() as conn:
        conn.execute(
            "INSERT INTO subscribers (email, subscribed_at, active) VALUES (?, ?, 1) "
            "ON CONFLICT(email) DO UPDATE SET active = 1",
            (email, datetime.utcnow().isoformat())
        )
    return {"success": True, "email": email, "status": "subscribed"}


@app.post("/unsubscribe")
def unsubscribe(req: SubscribeRequest):
    """Unsubscribe an email from AI in 5"""
    email = req.email.strip().lower()
    with get_db() as conn:
        conn.execute("UPDATE subscribers SET active = 0 WHERE email = ?", (email,))
    return {"success": True, "email": email, "status": "unsubscribed"}


@app.get("/subscribers")
def list_subscribers():
    """List active subscriber count"""
    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) FROM subscribers WHERE active = 1").fetchone()[0]
    return {"active_subscribers": count}


@app.get("/subscribers/export")
def export_subscribers():
    """Export active subscribers as CSV (for send.py)"""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT email, subscribed_at FROM subscribers WHERE active = 1 ORDER BY email"
        ).fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["email", "subscribed_at"])
    for row in rows:
        writer.writerow([row["email"], row["subscribed_at"]])
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=subscribers.csv"}
    )


if __name__ == "__main__":
    import uvicorn
    print("\n🛂 AI Skills Passport - Progress Tracker")
    print("   Docs: http://localhost:5050/docs")
    uvicorn.run(app, host="0.0.0.0", port=5050)

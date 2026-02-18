#!/usr/bin/env python3
"""AI in 5 — Daily micro-challenge emailer.

Reads today's challenge from content-bank.csv and emails all subscribers.

Usage:
    python send.py                  # Send today's challenge
    python send.py --preview        # Preview email without sending
    python send.py --day 3          # Send a specific day's challenge
    python send.py --test me@x.com  # Send only to this address (for testing)

Configuration:
    Copy .env.example to .env and fill in your SMTP credentials.
"""

import argparse
import csv
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_env(env_path=None):
    """Load .env file (simple key=value parser, no dependencies)."""
    if env_path is None:
        env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            value = value.strip().strip("'\"")
            os.environ.setdefault(key.strip(), value)


def get_config():
    """Read configuration from environment variables."""
    load_env()
    return {
        "smtp_host": os.environ.get("SMTP_HOST", "smtp.gmail.com"),
        "smtp_port": int(os.environ.get("SMTP_PORT", "587")),
        "smtp_user": os.environ.get("SMTP_USER", ""),
        "smtp_pass": os.environ.get("SMTP_PASS", ""),
        "from_name": os.environ.get("FROM_NAME", "AI Skills Passport"),
        "from_email": os.environ.get("FROM_EMAIL", ""),
        "reply_to": os.environ.get("REPLY_TO", ""),
    }


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

THEME_EMOJI = {
    "Tools": "\U0001f527",      # 🔧
    "Prompts": "\U0001f4ac",    # 💬
    "Ethics": "\u2696\ufe0f",   # ⚖️
    "Practice": "\U0001f6e0\ufe0f",  # 🛠️
    "Share": "\U0001f91d",      # 🤝
}

THEME_COLOUR = {
    "Tools": "#4F46E5",
    "Prompts": "#EA580C",
    "Ethics": "#DB2777",
    "Practice": "#16A34A",
    "Share": "#CA8A04",
}


def load_content_bank(path=None):
    """Load challenges from content-bank.csv."""
    if path is None:
        path = Path(__file__).parent / "content-bank.csv"
    challenges = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("day_number"):
                challenges.append(row)
    return challenges


def load_subscribers(path=None):
    """Load email addresses from subscribers.csv.

    Expects at minimum a column called 'email'. Ignores other columns,
    so a Blackboard group export (which has name, username, email) works.
    """
    if path is None:
        path = Path(__file__).parent / "subscribers.csv"
    emails = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        # Be flexible about column naming
        for row in reader:
            email = (
                row.get("email")
                or row.get("Email")
                or row.get("Email Address")
                or row.get("email_address")
                or ""
            ).strip()
            if email and "@" in email:
                emails.append(email)
    return emails


def get_today_challenge(challenges, day_override=None):
    """Pick today's challenge.

    Uses a start-date approach: day 1 = the first Monday on or after the
    start date stored in .env (AI5_START_DATE). Falls back to cycling
    through challenges based on weekday if no start date is set.
    """
    if day_override is not None:
        for c in challenges:
            if int(c["day_number"]) == day_override:
                return c
        print(f"Error: No challenge found for day {day_override}")
        sys.exit(1)

    load_env()
    start_date_str = os.environ.get("AI5_START_DATE", "")
    today = datetime.now().date()

    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        # Count weekdays since start
        delta = today - start_date
        weekdays_elapsed = sum(
            1 for i in range(delta.days + 1)
            if (start_date + __import__("datetime").timedelta(days=i)).weekday() < 5
        )
        day_num = ((weekdays_elapsed - 1) % len(challenges)) + 1
    else:
        # Simple fallback: cycle by weekday (Mon=1, Tue=2, ... Fri=5)
        weekday = today.weekday()  # 0=Mon
        if weekday >= 5:
            print("It's the weekend — no challenge today.")
            sys.exit(0)
        day_num = weekday + 1

    for c in challenges:
        if int(c["day_number"]) == day_num:
            return c

    print(f"Error: No challenge for day_number={day_num}")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Email formatting
# ---------------------------------------------------------------------------

def build_email_html(challenge):
    """Build an HTML email for the challenge."""
    theme = challenge["theme"]
    emoji = THEME_EMOJI.get(theme, "⚡")
    colour = THEME_COLOUR.get(theme, "#4F46E5")
    subject_line = challenge["subject"]
    body = challenge["body"]
    link = challenge.get("link", "").strip()
    day = challenge["day_number"]
    weekday = challenge["weekday"]

    link_html = ""
    if link:
        link_html = f'''
        <div style="margin-top: 16px;">
          <a href="{link}" style="display: inline-block; background: {colour}; color: white;
             text-decoration: none; padding: 10px 20px; border-radius: 6px;
             font-weight: bold; font-size: 14px;">Try it now &rarr;</a>
        </div>'''

    return f'''<!DOCTYPE html>
<html>
<body style="margin: 0; padding: 0; background: #F1F5F9; font-family: Georgia, 'Times New Roman', serif;">
  <div style="max-width: 560px; margin: 20px auto; background: white; border-radius: 12px; overflow: hidden;">

    <!-- Header -->
    <div style="background: linear-gradient(135deg, {colour}, #7C3AED); padding: 24px; text-align: center; color: white;">
      <div style="font-size: 2rem;">{emoji}</div>
      <div style="font-size: 1.4rem; font-weight: bold; letter-spacing: 1px;">AI in 5</div>
      <div style="font-size: 0.85rem; opacity: 0.85; margin-top: 4px;">{weekday} &middot; {theme}</div>
    </div>

    <!-- Challenge -->
    <div style="padding: 28px 24px;">
      <h2 style="margin: 0 0 16px 0; color: #1E293B; font-size: 1.3rem; font-weight: normal;">{subject_line}</h2>
      <p style="margin: 0; font-size: 1.05rem; line-height: 1.7; color: #333;">{body}</p>
      {link_html}
    </div>

    <!-- Footer -->
    <div style="padding: 16px 24px; background: #F8FAFC; border-top: 1px solid #E2E8F0; text-align: center;">
      <p style="margin: 0; font-size: 0.8rem; color: #94A3B8;">
        Day {day} &middot; AI Skills Passport &middot; School of Marketing and Management &middot; Curtin University
      </p>
    </div>

  </div>
</body>
</html>'''


def build_email_text(challenge):
    """Build a plain-text fallback."""
    theme = challenge["theme"]
    subject_line = challenge["subject"]
    body = challenge["body"]
    link = challenge.get("link", "").strip()
    day = challenge["day_number"]
    weekday = challenge["weekday"]

    text = f"AI in 5 — {weekday} ({theme})\n"
    text += "=" * 40 + "\n\n"
    text += f"{subject_line}\n\n"
    text += f"{body}\n"
    if link:
        text += f"\nTry it: {link}\n"
    text += f"\n---\nDay {day} | AI Skills Passport | SoMM, Curtin University\n"
    return text


# ---------------------------------------------------------------------------
# Sending
# ---------------------------------------------------------------------------

def send_email(config, to_addresses, challenge):
    """Send the challenge email via SMTP."""
    subject = f"AI in 5: {challenge['subject']}"

    with smtplib.SMTP(config["smtp_host"], config["smtp_port"]) as server:
        server.starttls()
        server.login(config["smtp_user"], config["smtp_pass"])

        for addr in to_addresses:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{config['from_name']} <{config['from_email']}>"
            msg["To"] = addr
            if config["reply_to"]:
                msg["Reply-To"] = config["reply_to"]

            msg.attach(MIMEText(build_email_text(challenge), "plain"))
            msg.attach(MIMEText(build_email_html(challenge), "html"))

            server.send_message(msg)
            print(f"  Sent to {addr}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI in 5 daily emailer")
    parser.add_argument("--preview", action="store_true", help="Preview email without sending")
    parser.add_argument("--day", type=int, help="Send a specific day number")
    parser.add_argument("--test", metavar="EMAIL", help="Send only to this address")
    parser.add_argument("--content", metavar="PATH", help="Path to content-bank.csv")
    parser.add_argument("--subscribers", metavar="PATH", help="Path to subscribers.csv")
    args = parser.parse_args()

    challenges = load_content_bank(args.content)
    challenge = get_today_challenge(challenges, day_override=args.day)

    print(f"Challenge: Day {challenge['day_number']} ({challenge['weekday']}) — {challenge['subject']}")
    print()

    if args.preview:
        print(build_email_text(challenge))
        # Also write HTML preview
        preview_path = Path(__file__).parent / "preview.html"
        with open(preview_path, "w") as f:
            f.write(build_email_html(challenge))
        print(f"HTML preview written to {preview_path}")
        return

    config = get_config()
    if not config["smtp_user"] or not config["smtp_pass"]:
        print("Error: SMTP credentials not configured. Copy .env.example to .env and fill in your details.")
        sys.exit(1)

    if args.test:
        recipients = [args.test]
    else:
        recipients = load_subscribers(args.subscribers)
        if not recipients:
            print("Error: No subscribers found. Export the group list from Blackboard as subscribers.csv")
            sys.exit(1)

    print(f"Sending to {len(recipients)} recipient(s)...")
    send_email(config, recipients, challenge)
    print("Done!")


if __name__ == "__main__":
    main()

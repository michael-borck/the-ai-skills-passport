# CLAUDE.md — The AI Skills Passport

## Project Overview

The AI Skills Passport is a professional development initiative for the School of Marketing and Management (SoMM), Curtin University. It builds AI literacy across teaching academics, researchers, and administrative staff.

The project lead is Michael Borck, AI Facilitator for SoMM. He is the sole developer. The initiative was endorsed by school leadership (Head of School Julia) in late 2025.

## Architecture

### 1. Blackboard (LMS) — "The Shell"

Blackboard is intentionally minimal — just authentication, announcements, and a launch point. All real UX happens in SPAs.

- Blackboard Classic/Original Organisation site
- **6 sidebar items:** The Arrivals Hall, AI in 5, AI Toolkit, My Passport, Contact, About
- The Arrivals Hall is the hub — contains links to everything else
- "AI in 5" is renamed Announcements — daily micro-challenges emailed to enrolled staff
- All experiences, toolkit, and quiz open as standalone SPAs in new browser tabs
- Blackboard URL variable substitution passes user identity: `?uid=@X@user.batch_uid@X@`
- All HTML uses **inline CSS only** — Blackboard strips `<style>` tags
- Blackboard retiring end of 2026, replaced by Canvas — minimal BB investment intentional
- Goal: "wow" users with polished SPAs, not typical LMS clutter

### 2. The AI Exchange — "The Registry"

- Separate project: https://github.com/michael-borck/the-ai-exchange
- FastAPI + React/TypeScript, Docker deployment
- Voluntary registry for recording/discovering/connecting around AI use cases
- Curtin email auth (@curtin.edu.au), verified anonymity feature
- NOT a learning platform — does not host courseware or pathways
- Hosted on desktop machine, Curtin internal network, VPN-accessible

### 3. Progress Tracker — Completion Recording

- Simplified FastAPI server in `server/app.py` (~75 lines)
- Two endpoints: `POST /complete`, `GET /progress/{uid}`
- SQLite database for persistence
- Emoji badges: 🧪 Explorer (1) → 🧠 Thinker (3) → 🛠️ Builder (5)
- SPAs use localStorage as fallback when server unavailable
- Runs on desktop machine, Curtin internal network
- Interactive docs at `/docs` (Swagger UI)

## The Five Core Experiences

These are the learning content. Everything else (AI in 5, workshops, pacing) is a delivery mode.

| # | Experience | Focus | Time | Audience |
|---|---|---|---|---|
| 1 | Is This AI? | Detection & Awareness | 15-60 min | All roles |
| 2 | What Would You Do? | Ethics & Dilemmas | 20-90 min | All roles |
| 3 | Rules of Engagement | Policy & Governance | 30-120 min | All roles |
| 4 | AI-Proof Your Assessments | Assessment Design | 45-75 min | Teaching-focused |
| 5 | Working WITH AI | Co-Creation & Integration | 30-60 min | All roles |

## Additional Components

- **Find Your Path** — Onboarding quiz recommending starting experience (`onboarding/`)
- **AI Toolkit** — Searchable reference library of frameworks, techniques, templates (`resources/`)
- **My Passport** — Badge progress display (`passport/`)

## Content Authoring

- **Quarto** is the primary authoring tool
- Single source → multiple outputs: interactive HTML (SPA), PDF, slides
- Each component is a Quarto project with `index.qmd`
- Output is a self-contained HTML page (SPA) in `_site/`
- SPAs include completion triggers (POST to server, localStorage fallback)
- All CSS inline for Blackboard compatibility

## Pacing Options (not separate content)

| Pace | Mechanism |
|---|---|
| Self-paced | Work through SPAs from Arrivals Hall links at own speed |
| AI in 5 | Daily 5-min micro-challenge via Blackboard Announcements (emailed) |
| Weekly | One experience per week for 5 weeks (suggested on Arrivals Hall) |
| Workshop | 2-hour face-to-face, same content, guided by facilitator |

## Technical Environment

- **Platform:** macOS with zsh
- **Network:** Curtin University internal network, VPN required for external access
- **Hosting:** Desktop machine (progress tracker, AI Exchange)
- **LMS:** Blackboard Classic now, Canvas late 2026
- **Blackboard constraints:** Inline CSS only, no `<style>` tags, no external files. CAN embed JS inline. CAN use URL variables for user identity
- **Version control:** Git + GitHub (SSH for push)
- **No Blackboard API access** — cannot programmatically post announcements

## Style Guide

- **Spelling:** Australian/British (analyse, behaviour, recognise, summarise, customise)
- **Shell:** Use `perl -pi -e` for in-place text substitution (BSD `sed` on macOS has quirks)

## Design Principles

- **Start Anywhere** — no prerequisites, no forced sequences
- **Everyone Belongs** — teaching, research, admin all have relevant content
- **Practical Over Theoretical** — staff use their own materials
- **Blackboard is a Shell** — minimal LMS footprint, SPAs are the product
- **Migration-Ready** — SPAs survive platform changes, just update URLs
- **Don't Over-Build** — pilot first, iterate based on real feedback

## Key Decisions Made

- **6-item sidebar** — Arrivals Hall is the hub, not a cluttered menu
- **SPAs over Blackboard content** — rich interactivity, platform-independent
- **Simplified progress tracker** — not full BadgeQuest, just completions + badges
- **localStorage fallback** — works without server for proof of concept
- **Inline CSS everywhere** — Blackboard strips `<style>` tags
- Terminals (T/R/A) rejected as structure — role tabs inside each experience instead
- Teams dropped — academics don't live there
- Power Automate dropped — Blackboard announcements work for pilot scale
- Grade Centre not used — progress tracker handles badges

## Project Structure

```
the-ai-skills-passport/
├── blackboard/
│   ├── arrivals-hall.html      # Landing page (paste into BB)
│   ├── ai-in-5.html            # AI in 5 subscribe page
│   ├── ai-toolkit.html         # Toolkit sidebar landing
│   ├── my-passport.html        # Badge progress overview
│   ├── contact.html            # Contact the AI Facilitator
│   └── about.html              # Initiative info, acknowledgements
├── onboarding/                  # Find Your Path quiz
├── resources/                   # AI Toolkit
├── passport/                    # My Passport
├── experiences/
│   ├── is-this-ai/
│   ├── what-would-you-do/
│   ├── rules-of-engagement/
│   ├── ai-proof-assessments/
│   └── teaching-with-ai/
├── server/
│   ├── app.py                  # Progress tracker (FastAPI)
│   └── requirements.txt
└── docs/
    ├── scaffold-guide.md       # Blackboard setup
    └── deployment-guide.md     # Build and deploy
```

## Commands

```bash
# Render all SPAs
for dir in onboarding resources passport experiences/*/; do
  quarto render "$dir"
done

# Run progress tracker
cd server
pip install -r requirements.txt
python app.py
# Open http://localhost:5050/docs

# Preview a single SPA
cd experiences/is-this-ai
quarto preview
```

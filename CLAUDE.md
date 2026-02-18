# CLAUDE.md — The AI Skills Passport

## Project Overview

The AI Skills Passport is a professional development initiative for the School of Marketing and Management (SoMM), Curtin University. It builds AI literacy across teaching academics, researchers, and administrative staff.

The project lead is Michael Borck, AI Facilitator for SoMM. He is the sole developer. The initiative was endorsed by school leadership (Head of School Julia) in late 2025.

## Architecture

Two platforms, each with one job:

### 1. Blackboard (LMS) — "The Launcher"
- Blackboard Classic/Original Organisation site
- Serves as a **menu with links**, not a content host
- Sidebar has 8 items: The Arrivals Hall, AI in 5, five experience links, My Passport
- "AI in 5" is renamed Announcements — daily micro-challenges emailed to enrolled staff
- Experiences open as standalone SPAs in new browser tabs via Blackboard links
- Blackboard URL variable substitution passes user identity: `?uid=@X@user.batch_uid@X@`
- My Passport is an embedded page that calls BadgeQuest API to show live progress
- All HTML in Blackboard uses **inline CSS only** — Blackboard strips `<style>` tags and external CSS
- Blackboard is being retired end of 2026, replaced by Canvas. Do not over-invest in BB-specific features
- The Arrivals Hall can contain embedded HTML/JS in a Blackboard content item

### 2. The AI Exchange — "The Registry"
- Separate project: https://github.com/michael-borck/the-ai-exchange
- FastAPI + React/TypeScript, Docker deployment
- Voluntary registry for recording/discovering/connecting around AI use cases
- Curtin email auth (@curtin.edu.au), verified anonymity feature
- NOT a learning platform — does not host courseware or pathways
- Hosted on desktop machine, Curtin internal network, VPN-accessible

### 3. BadgeQuest — Progress Tracking
- Separate project: https://github.com/michael-borck/badge-quest
- Flask-based badge/gamification server
- SPAs submit completion events to BadgeQuest API on module finish
- My Passport page reads from BadgeQuest API to display live progress
- Emoji-based badges: 🧪 Explorer (1 exp) → 🧠 Thinker (3) → 🛠️ Builder (5) → 🏆 Champion
- Additional: ☕ AI in 5 Streak, 🎓 Workshop Participant
- Hosted alongside AI Exchange on same desktop machine

## The Five Core Experiences

These are the learning content. Everything else (AI in 5, workshops, pacing) is a delivery mode.

| # | Experience | Focus | Time | Audience |
|---|---|---|---|---|
| 1 | Is This AI? | Detection & Awareness | 15-60 min | All roles |
| 2 | What Would You Do? | Ethics & Dilemmas | 20-90 min | All roles |
| 3 | Rules of Engagement | Policy & Governance | 30-120 min | All roles |
| 4 | AI-Proof Your Assessments | Assessment Design | 45-75 min | Teaching-focused |
| 5 | Teaching WITH AI | Co-Creation & Integration | 30-60 min | Teaching-focused |

Future Phase 2 additions (research/admin-specific):
- The AI Research Toolkit
- Integrity in the Age of AI
- Automate the Mundane
- AI for Better Communication

## Content Authoring

- **Quarto** is the primary authoring tool
- Single source → multiple outputs: interactive HTML (SPA), PDF, slides
- Each experience is a Quarto project in `experiences/[name]/`
- Output is a self-contained interactive HTML page (SPA)
- SPAs include a completion trigger that POSTs to BadgeQuest on finish
- Quarto supports OJS (Observable JS) for interactivity

## Pacing Options (not separate content)

| Pace | Mechanism |
|---|---|
| Self-paced | Work through SPAs from Blackboard links at own speed |
| AI in 5 | Daily 5-min micro-challenge via Blackboard Announcements (emailed) |
| Weekly | One experience per week for 5 weeks (self-directed, suggested on Arrivals Hall) |
| Workshop | 2-hour face-to-face, same content, guided by facilitator |

## Technical Environment

- **Network:** Curtin University internal network, locked down. VPN required for external access
- **Hosting:** Desktop machine running Docker containers (AI Exchange, BadgeQuest, SPAs)
- **Microsoft:** Enterprise M365 license, Copilot in tools. No confirmed API access to Azure OpenAI or Anthropic
- **LMS:** Blackboard Classic now, Canvas late 2026
- **Blackboard constraints:** Inline CSS only, no `<style>` tags, no external CSS/JS files. CAN embed JS inline. CAN use Blackboard URL variables for user identity
- **Version control:** Git + GitHub
- **No Blackboard API access** from Curtin — cannot programmatically post announcements

## Design Principles

- **Start Anywhere** — no prerequisites, no forced sequences
- **Everyone Belongs** — teaching, research, admin all have relevant content
- **Practical Over Theoretical** — staff use their own materials
- **Two Platforms, Two Jobs** — Blackboard launches, Exchange connects
- **Don't Over-Build** — pilot first, iterate based on real feedback

## Key Decisions Made

- Terminals (T/R/A) were explored as a structural concept but rejected — they work as entry framing but not as content silos. Each module includes examples from all contexts instead
- Teams was explored and dropped — academics don't live there, adds unnecessary platform
- Power Automate was explored and dropped — Blackboard announcements handle daily delivery natively for the pilot scale
- Content lives in SPAs, not in Blackboard — enables rich interactivity and survives LMS migration
- BadgeQuest handles all progress tracking — Grade Centre not used

## Existing Assets

Michael has existing interactive SPAs (teaching style quiz, AI journey assessment) that demonstrate the SPA-from-Blackboard approach works. These could be integrated as orientation tools.

## Commands

```bash
# Quarto render a single experience
cd experiences/is-this-ai && quarto render

# Run BadgeQuest locally
cd ../badge-quest && source .venv/bin/activate && badgequest run-server --port 5000

# Run AI Exchange locally
cd ../the-ai-exchange && docker-compose up -d

# Serve SPAs locally for testing
python -m http.server 8080 --directory experiences/
```

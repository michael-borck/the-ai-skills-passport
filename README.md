# The AI Skills Passport

<!-- BADGES:START -->
[![ai-literacy](https://img.shields.io/badge/-ai--literacy-blue?style=flat-square)](https://github.com/topics/ai-literacy) [![assessment-design](https://img.shields.io/badge/-assessment--design-blue?style=flat-square)](https://github.com/topics/assessment-design) [![css](https://img.shields.io/badge/-css-1572b6?style=flat-square)](https://github.com/topics/css) [![curtin-university](https://img.shields.io/badge/-curtin--university-blue?style=flat-square)](https://github.com/topics/curtin-university) [![html](https://img.shields.io/badge/-html-e34f26?style=flat-square)](https://github.com/topics/html) [![modular-learning](https://img.shields.io/badge/-modular--learning-blue?style=flat-square)](https://github.com/topics/modular-learning) [![professional-development](https://img.shields.io/badge/-professional--development-blue?style=flat-square)](https://github.com/topics/professional-development) [![python](https://img.shields.io/badge/-python-3776ab?style=flat-square)](https://github.com/topics/python) [![self-paced-learning](https://img.shields.io/badge/-self--paced--learning-blue?style=flat-square)](https://github.com/topics/self-paced-learning) [![shell](https://img.shields.io/badge/-shell-blue?style=flat-square)](https://github.com/topics/shell)
<!-- BADGES:END -->

**Professional development for AI literacy. School of Marketing and Management, Curtin University.**

## The Philosophy: Learn Your Way

The AI Skills Passport is built on one idea: **you choose how you engage**.

There are no prerequisites, no forced sequences, no "complete Module 1 before Module 2". Every experience stands alone. Start with whatever grabs your attention. Do one, do all seven, skip around. Come back later. It's your passport — stamp it however you like.

- **Want a guided starting point?** Take the 2-minute *Find Your Path* quiz
- **Prefer to explore?** Browse the seven experiences from the Arrivals Hall
- **Short on time?** Read the *Key Takeaways* — the essential insights in 5 minutes
- **Want weekly nudges?** Subscribe to *AI in 5* — a micro-challenge in your inbox each week
- **Just need a reference?** Search the *AI Toolkit* for frameworks, templates, and techniques
- **Prefer face-to-face?** Contact the AI Facilitator to arrange a workshop

Everyone belongs — teaching academics, researchers, and professional staff all have relevant content with role-specific tabs inside each experience.

## The Seven Experiences

| # | Experience | Focus | Time |
|---|---|---|---|
| 1 | Is This AI? | Detection & Awareness | 15-60 min |
| 2 | What Would You Do? | Ethics & Dilemmas | 20-90 min |
| 3 | Rules of Engagement | Policy & Governance | 30-120 min |
| 4 | AI-Proof Your Assessments | Assessment Design | 45-75 min |
| 5 | Working with AI | Co-Creation & Integration | 30-60 min |
| 6 | Working with Copilot | AI-Assisted Coding | 30-60 min |
| 7 | Researching with AI | Research & Literature | 30-60 min |

## Supporting Components

- **The Arrivals Hall** — the hub; everything launches from here
- **Find Your Path** — 2-minute quiz recommending your starting experience
- **AI Toolkit** — searchable reference library of frameworks, techniques, and templates
- **Key Takeaways** — the essential insights from all experiences, for when you're short on time
- **My Passport** — track your progress and collect badges
- **AI in 5** — weekly 5-minute micro-challenge delivered by email
- **Contact** — reach the AI Facilitator, request a workshop
- **About** — background on the initiative

## Architecture: Blackboard as a Shell

Blackboard does two things: **authenticate** and **redirect**. That's it.

All the real content lives in **self-contained SPAs** (single-page applications) built with Quarto. When a user clicks into the Arrivals Hall from Blackboard, a redirect sends them into SPA-land. From there, every link — experiences, toolkit, passport, key takeaways — is a **relative link between SPAs**. Users navigate freely without bouncing back to the LMS.

```
Blackboard (auth)
  └─ redirect ──▸ Arrivals Hall (SPA)
                     ├── experiences/is-this-ai.html
                     ├── experiences/what-would-you-do.html
                     ├── experiences/rules-of-engagement.html
                     ├── experiences/ai-proof-assessments.html
                     ├── experiences/teaching-with-ai.html
                     ├── experiences/working-with-copilot.html
                     ├── experiences/researching-with-ai.html
                     ├── ai-toolkit.html       (AI Toolkit)
                     ├── resources.html        (Resources landing)
                     ├── more.html             (More landing)
                     ├── key-takeaways.html
                     ├── passport.html         (My Passport)
                     ├── onboarding.html       (Find Your Path)
                     ├── contact.html
                     └── about.html
```

This design is intentionally **migration-ready**. When Blackboard retires (late 2026, replaced by Canvas), only the redirect needs updating. The SPAs survive unchanged.

### Why SPAs?

- Rich interactivity that Blackboard can't deliver natively
- Platform-independent — survive LMS migrations
- Each SPA has a hamburger menu for navigation between all pages
- Inline CSS only (Blackboard strips `<style>` tags)
- Self-contained HTML files — no external dependencies

### Progress Tracking

A **progress tracker server** has been developed (`server/app.py`) — a lightweight FastAPI + SQLite service that records experience completions and awards emoji badges:

- 🧪 **Explorer** — completed 1 experience
- 🧠 **Thinker** — completed 3 experiences
- 🛠️ **Builder** — completed 5 experiences
- 🏆 **Champion** — completed all 7 experiences

The server uses Blackboard's **URL variable substitution** (`@X@user.batch_uid@X@`) to identify users, passing the Blackboard UID as a query parameter when launching SPAs.

**For this MVP, server integration has not been implemented within the SPAs.** Before connecting SPAs to the server, privacy and data governance questions around storing Blackboard UIDs need to be resolved — even on a Curtin University system. See [Data Governance](docs/data-governance.md) for details.

Currently, the **My Passport** page uses **browser localStorage** to track progress. This keeps all data on the user's device with no server-side storage of identifiers.

The server code is included in this repository as a reference implementation, ready for integration once data governance approval is obtained. See [Progress Tracker API](docs/progress-tracker-api.md) for the full API reference and [SPA Integration Guide](docs/spa-integration-guide.md) for the modifications needed to connect SPAs to the server.

## Project Structure

```
the-ai-skills-passport/
├── arrivals-hall/              # The hub SPA
├── experiences/
│   ├── is-this-ai/
│   ├── what-would-you-do/
│   ├── rules-of-engagement/
│   ├── ai-proof-assessments/
│   ├── teaching-with-ai/
│   ├── working-with-copilot/
│   └── researching-with-ai/
├── onboarding/                 # Find Your Path quiz
├── ai-toolkit/                 # AI Toolkit (searchable reference)
├── resources/                  # Resources landing page
├── more/                       # More landing page
├── key-takeaways/              # Essential insights summary
├── passport/                   # My Passport (badge tracker)
├── contact/                    # Contact the AI Facilitator
├── about/                      # About the initiative
├── blackboard/                 # HTML pasted into Blackboard
├── ai-in-5/                    # Weekly challenge email utility
├── shared/                     # Brand CSS shared across SPAs
├── server/                     # Progress tracker (FastAPI)
├── scripts/
│   └── build.sh                # Render all SPAs and package
└── docs/
    ├── scaffold-guide.md          # Blackboard setup
    ├── deployment-guide.md        # Build and deploy
    ├── facilitator-guide.md       # Workshop facilitation
    ├── brand-guide.md             # Colours, typography, style
    ├── accessibility-notes.md     # Accessibility considerations
    ├── data-governance.md         # Privacy and data governance
    ├── progress-tracker-api.md    # Server API reference
    └── spa-integration-guide.md   # SPA-to-server integration
```

Each component is a Quarto project with `index.qmd`. The build script renders all of them and collects the self-contained HTML files into `dist/` for deployment.

## Quick Start

```bash
# Clone
git clone https://github.com/michael-borck/the-ai-skills-passport.git
cd the-ai-skills-passport

# Build everything
bash scripts/build.sh

# Preview a single SPA
cd experiences/is-this-ai
quarto preview

# Run progress tracker (optional)
cd server
pip install -r requirements.txt
python app.py
# Open http://localhost:5050/docs
```

## Pacing Options

All options use the same content, just different rhythms:

| Pace | How it works |
|---|---|
| **Self-paced** | Browse SPAs from the Arrivals Hall at your own speed |
| **AI in 5** | Weekly 5-minute micro-challenge delivered to your inbox |
| **Weekly** | One experience per week for seven weeks |
| **Workshop** | 2-hour face-to-face guided session |

## Data Governance

The progress tracker server stores **Blackboard UIDs** — personally identifiable information that maps to individual staff members. Although the SPAs are hosted within Blackboard (requiring a Curtin account to access), the server itself needs separate hosting. The database storing UIDs would sit outside Blackboard's institutional governance.

Curtin does not currently appear to offer a sandbox environment suitable for hosting this kind of lightweight application under institutional data governance. Until these questions are resolved:

- **This MVP uses browser localStorage only** — no server-side storage of user identifiers
- The server code is included as a **reference implementation**, ready for integration once approval is obtained
- See [docs/data-governance.md](docs/data-governance.md) for the full analysis and path forward

## Related Projects

- **[The AI Exchange](https://github.com/michael-borck/the-ai-exchange)** — voluntary registry for discovering and discussing AI use cases (FastAPI + React)

## Tech Stack

- **Content:** [Quarto](https://quarto.org/) — single source to self-contained HTML SPAs
- **Progress:** FastAPI + SQLite
- **LMS:** Blackboard Classic (Canvas late 2026)

## Author

**Michael Borck**, AI Facilitator, School of Marketing and Management, Curtin University

## Licence

**Code:** MIT Licence

**Content:** MIT (may transition to CC BY 4.0 for educational content)

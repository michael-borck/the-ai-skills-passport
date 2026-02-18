# The AI Skills Passport 🛂

**Professional development for AI literacy — School of Marketing and Management, Curtin University**

The AI Skills Passport is a flexible, self-paced program that builds AI literacy across teaching academics, researchers, and administrative staff. Five standalone learning experiences, no prerequisites, start anywhere.

## How It Works

**Blackboard** is the launcher — a menu of links and daily micro-challenges via email.

**Five interactive SPAs** are the learning — standalone web apps that open in new tabs, rich and interactive, hosted independently of any LMS.

**BadgeQuest** tracks progress — SPAs report completions, and a live passport page shows your badges.

**The AI Exchange** connects people — a voluntary registry where staff record, discover, and discuss AI use cases across the school.

## The Five Experiences

| # | Experience | Focus | Time |
|---|---|---|---|
| 1 | 🔍 Is This AI? | Detection & Awareness | 15–60 min |
| 2 | 🤔 What Would You Do? | Ethics & Dilemmas | 20–90 min |
| 3 | 📋 Rules of Engagement | Policy & Governance | 30–120 min |
| 4 | 🛡️ AI-Proof Your Assessments | Assessment Design | 45–75 min |
| 5 | 🤝 Teaching WITH AI | Co-Creation & Integration | 30–60 min |

## Pacing Options

All pacing options use the same content — they're just different rhythms:

- **Self-Paced** — work through SPAs on Blackboard at your own speed
- **AI in 5** — 5-minute daily micro-challenge in your inbox every morning
- **Weekly** — one experience per week for five weeks
- **Workshop** — 2-hour face-to-face guided session

## Project Structure

```
the-ai-skills-passport/
├── CLAUDE.md                        # Project context for Claude Code
├── README.md                        # This file
├── docs/
│   └── architecture.md              # Full architecture specification
├── blackboard/
│   ├── arrivals-hall.html           # Landing page (inline CSS for BB)
│   ├── my-passport.html             # Badge progress page (calls BadgeQuest API)
│   └── coming-soon.html             # Placeholder for unpopulated experiences
├── experiences/
│   ├── is-this-ai/
│   │   ├── _quarto.yml
│   │   ├── index.qmd                # Quarto source
│   │   └── _output/                 # Built SPA (HTML)
│   ├── what-would-you-do/
│   │   ├── _quarto.yml
│   │   ├── index.qmd
│   │   └── _output/
│   ├── rules-of-engagement/
│   │   ├── _quarto.yml
│   │   ├── index.qmd
│   │   └── _output/
│   ├── ai-proof-assessments/
│   │   ├── _quarto.yml
│   │   ├── index.qmd
│   │   └── _output/
│   └── teaching-with-ai/
│       ├── _quarto.yml
│       ├── index.qmd
│       └── _output/
├── ai-in-5/
│   ├── content-bank.csv             # Daily challenge content library
│   └── README.md                    # Posting guide and theme schedule
├── workshops/
│   ├── README.md                    # Workshop facilitation notes
│   └── slides/                      # Quarto-generated slide decks
├── assets/
│   ├── images/
│   └── badges/                      # Badge emoji/image assets
└── scripts/
    └── setup.sh                     # Repo scaffold script
```

## Related Projects

- **[BadgeQuest](https://github.com/michael-borck/badge-quest)** — Gamified badge progression system (Flask)
- **[The AI Exchange](https://github.com/michael-borck/the-ai-exchange)** — AI use case registry and peer discovery (FastAPI + React)

## Tech Stack

- **Content Authoring:** [Quarto](https://quarto.org/) (single source → HTML SPA, PDF, slides)
- **Badge Tracking:** [BadgeQuest](https://github.com/michael-borck/badge-quest) (Flask + SQLite)
- **LMS:** Blackboard Classic (transitioning to Canvas late 2026)
- **Hosting:** Docker on Curtin internal network

## Quick Start

```bash
# Clone and set up
git clone https://github.com/michael-borck/the-ai-skills-passport.git
cd the-ai-skills-passport

# Render a specific experience
cd experiences/is-this-ai
quarto render

# Preview locally
quarto preview
```

## Author

**Michael Borck** — AI Facilitator, School of Marketing and Management, Curtin University

## License

MIT

# The AI Skills Passport 🛂

**Professional development for AI literacy — School of Marketing and Management, Curtin University**

The AI Skills Passport is a flexible, self-paced program that builds AI literacy across teaching academics, researchers, and administrative staff. Five standalone learning experiences, no prerequisites, start anywhere.

## How It Works

**Blackboard** is the launcher — a menu of links and daily micro-challenges via email.

**Interactive SPAs** are the learning — standalone web apps that open in new tabs, rich and interactive.

**Progress Tracker** records completions — SPAs report progress, My Passport shows your badges.

**The AI Exchange** connects people — a voluntary registry where staff discover and discuss AI use cases.

## The Five Experiences

| # | Experience | Focus | Time |
|---|---|---|---|
| 1 | 🔍 Is This AI? | Detection & Awareness | 15–60 min |
| 2 | 🤔 What Would You Do? | Ethics & Dilemmas | 20–90 min |
| 3 | 📋 Rules of Engagement | Policy & Governance | 30–120 min |
| 4 | 🛡️ AI-Proof Your Assessments | Assessment Design | 45–75 min |
| 5 | 🤝 Teaching WITH AI | Co-Creation & Integration | 30–60 min |

## Additional Components

- **Find Your Path** — 2-minute onboarding quiz to recommend your starting point
- **AI Toolkit** — Searchable reference library (frameworks, techniques, templates)
- **My Passport** — Track progress and collect badges
- **AI in 5** — Daily 5-minute micro-challenges via email

## Pacing Options

All options use the same content — just different rhythms:

- **Self-Paced** — work through SPAs at your own speed
- **AI in 5** — 5-minute daily challenge in your inbox
- **Weekly** — one experience per week for five weeks
- **Workshop** — 2-hour face-to-face guided session

## Project Structure

```
the-ai-skills-passport/
├── blackboard/
│   └── arrivals-hall.html       # Landing page (paste into Blackboard)
├── onboarding/
│   └── index.qmd                # Find Your Path quiz
├── resources/
│   └── index.qmd                # AI Toolkit
├── passport/
│   └── index.qmd                # My Passport (badge tracker)
├── experiences/
│   ├── is-this-ai/
│   ├── what-would-you-do/
│   ├── rules-of-engagement/
│   ├── ai-proof-assessments/
│   └── teaching-with-ai/
├── server/
│   ├── app.py                   # Progress tracker (FastAPI)
│   └── requirements.txt
└── docs/
    ├── scaffold-guide.md        # Blackboard setup
    ├── deployment-guide.md      # Build and deploy SPAs
    ├── facilitator-guide.md     # Workshop facilitation
    └── brand-guide.md           # Colours, typography, style
```

## Quick Start

```bash
# Clone
git clone https://github.com/michael-borck/the-ai-skills-passport.git
cd the-ai-skills-passport

# Render an experience
cd experiences/is-this-ai
quarto render
quarto preview

# Run progress tracker
cd server
pip install -r requirements.txt
python app.py
# Open http://localhost:5050/docs
```

## Deployment

See `docs/deployment-guide.md` for full instructions:

1. Render all Quarto projects to HTML
2. Upload HTML files to Blackboard
3. Update placeholder URLs in arrivals-hall.html
4. Paste arrivals-hall into Blackboard content item
5. (Optional) Run progress tracker server

## Related Projects

- **[The AI Exchange](https://github.com/michael-borck/the-ai-exchange)** — AI use case registry (FastAPI + React)

## Tech Stack

- **Content:** [Quarto](https://quarto.org/) → self-contained HTML SPAs
- **Progress:** FastAPI + SQLite (minimal server)
- **LMS:** Blackboard Classic (Canvas late 2026)

## Author

**Michael Borck** — AI Facilitator, School of Marketing and Management, Curtin University

## License

**Code:** MIT License

**Content:** MIT (may transition to CC BY 4.0 for educational content)

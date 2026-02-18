#!/bin/bash
# setup.sh — Scaffold the AI Skills Passport repo structure
# Run from the repo root: bash scripts/setup.sh

set -e

echo "🛂 Scaffolding The AI Skills Passport..."

# Docs
mkdir -p docs

# Blackboard HTML files
mkdir -p blackboard

# Experiences (Quarto projects)
for exp in is-this-ai what-would-you-do rules-of-engagement ai-proof-assessments teaching-with-ai; do
  mkdir -p "experiences/${exp}/_output"
  
  # Quarto project file
  if [ ! -f "experiences/${exp}/_quarto.yml" ]; then
    cat > "experiences/${exp}/_quarto.yml" << EOF
project:
  type: default
  output-dir: _output

format:
  html:
    theme: none
    minimal: true
    self-contained: true
    toc: false
EOF
  fi

  # Starter qmd
  if [ ! -f "experiences/${exp}/index.qmd" ]; then
    # Convert folder name to title
    title=$(echo "$exp" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g')
    cat > "experiences/${exp}/index.qmd" << EOF
---
title: "${title}"
format:
  html:
    self-contained: true
---

# ${title}

<!-- TODO: Build out this experience -->

This experience is under development.
EOF
  fi
done

# AI in 5
mkdir -p ai-in-5

if [ ! -f "ai-in-5/content-bank.csv" ]; then
  cat > "ai-in-5/content-bank.csv" << 'EOF'
day_number,weekday,theme,subject,body,link
1,Monday,Tools,"Try an AI tool today","Ask an AI to generate three discussion questions for your next meeting. How do they compare to yours?",
2,Tuesday,Prompts,"Write your first prompt","Write a prompt asking AI to summarise something from your field. What did it get right? What did it miss?",
3,Wednesday,Ethics,"Where's the line?","A colleague submits a report mostly written by AI. Where's the line?",
4,Thursday,Practice,"Draft with AI","Draft one email you need to send today with AI assistance. Was it faster? Better?",
5,Friday,Share,"Share what you tried","What's one thing you tried with AI this week? Register it on the AI Exchange.",
EOF
fi

if [ ! -f "ai-in-5/README.md" ]; then
  cat > "ai-in-5/README.md" << 'EOF'
# AI in 5 — Daily Micro-Challenges

## Posting Guide

1. Open Blackboard > AI in 5 (Announcements)
2. Create Announcement
3. Paste the day's challenge from `content-bank.csv`
4. Tick "Send a copy of this announcement immediately"
5. Post (~2 minutes)

## Weekly Theme Schedule

| Day       | Theme    | Focus                        |
|-----------|----------|------------------------------|
| Monday    | Tools    | Try a specific AI tool       |
| Tuesday   | Prompts  | Practice prompt writing      |
| Wednesday | Ethics   | Discuss an ethical scenario   |
| Thursday  | Practice | Apply AI to a real task      |
| Friday    | Share    | Share what you tried → AI Exchange |

## Content Bank

Edit `content-bank.csv` to add new challenges. Batch-write a month at a time (~20 weekday entries).
EOF
fi

# Workshops
mkdir -p workshops/slides

if [ ! -f "workshops/README.md" ]; then
  cat > "workshops/README.md" << 'EOF'
# Workshops — Face-to-Face Delivery

Same content as the self-paced SPAs, delivered in a guided 2-hour hands-on format.

## Formats

- **Taster** (45-60 min): Single experience, introductory
- **Full Workshop** (2 hrs): Two experiences back-to-back with discussion
- **Discipline-Specific** (2 hrs): Customised examples for a specific team or discipline group
- **Train the Trainer** (half day): For developing champions who can co-facilitate

## Slide Decks

Generated from Quarto. Source lives in the experience folders; slides are rendered here.

```bash
cd experiences/is-this-ai
quarto render --to revealjs --output-dir ../../workshops/slides/
```
EOF
fi

# Assets
mkdir -p assets/images assets/badges

# Scripts folder (this script lives here)
mkdir -p scripts

echo ""
echo "✅ Structure created:"
echo ""
find . -type f -not -path './.git/*' -not -name 'setup.sh' | sort | head -40
echo ""
echo "📋 Next steps:"
echo "   1. Copy existing files into place:"
echo "      - docs/architecture.md"
echo "      - blackboard/arrivals-hall.html"
echo "      - blackboard/my-passport.html"
echo "      - blackboard/coming-soon.html"
echo "   2. git init && git add -A && git commit -m 'Initial scaffold'"
echo "   3. Start building: cd experiences/is-this-ai && quarto preview"
echo ""
echo "🛂 Happy travels."

# The AI Skills Passport — Ecosystem Architecture

**School of Marketing and Management | Faculty of Business and Law**
**Curtin University**

**Author:** Michael Borck, AI Facilitator (SoMM)
**Version:** 2.0 — February 2026
**Status:** Draft Specification

---

## Executive Summary

The AI Skills Passport is a professional development initiative designed to build AI literacy across the entire School of Marketing and Management — teaching academics, researchers, and administrative staff.

The program runs on two platforms:

- **Blackboard** handles all structured learning and daily micro-challenges. Five self-contained learning experiences form the core. Daily "AI in 5" announcements deliver five-minute challenges directly to staff inboxes.
- **The AI Exchange** answers the question "what are we doing with AI in this school?" — a voluntary registry where staff record, discover, and connect around AI use cases.

Face-to-face workshops deliver the same content as Blackboard in a guided, hands-on format.

---

## Design Philosophy

**Start Anywhere.** No prerequisites, no forced sequences. Every experience is self-contained and immediately practical.

**Everyone Belongs.** Whether you teach, research, or keep the school running — each experience includes examples from all three contexts. Nobody arrives and wonders "is this for me?"

**Practical Over Theoretical.** Staff work with their own materials. When they leave any session, they have something they can use tomorrow.

**Decentralised Expertise.** The AI Facilitator should not be the permanent single point of contact. The AI Exchange enables direct staff-to-staff connection, scaling the facilitator role from answering every question to connecting people with each other.

**Two Platforms, Two Jobs.** Blackboard teaches. The Exchange connects. Neither tries to be the other.

---

## The Five Core Experiences

These are the content. Everything else — AI in 5, workshops, pathways — is a different pace or delivery mode for moving through them.

| # | Experience | Focus | Time | Context |
|---|---|---|---|---|
| 1 | **Is This AI?** | Detection & Awareness | 15–60 min | All roles |
| 2 | **What Would You Do?** | Ethics & Dilemmas | 20–90 min | All roles |
| 3 | **Rules of Engagement** | Policy & Governance | 30–120 min | All roles |
| 4 | **AI-Proof Your Assessments** | Assessment Design | 45–75 min | Teaching-focused (with research and admin angles) |
| 5 | **Teaching WITH AI** | Co-Creation & Integration | 30–60 min | Teaching-focused (with research and admin angles) |

Each experience is self-contained, requires no prior knowledge, and includes examples and scenarios from teaching, research, and administrative contexts. A sceptic and an enthusiast can sit in the same session and both leave with applicable skills.

### Content Approach

All content is authored in **Quarto**, providing multiple output formats from a single source — HTML for Blackboard embedding, PDF for offline use, slides for face-to-face workshops. When Canvas replaces Blackboard, the content is re-linked, not re-authored.

Experiences 4 and 5 skew toward teaching contexts because that is the strongest existing content and the largest audience. Research-specific and admin-specific experiences (e.g., "The AI Research Toolkit", "Automate the Mundane") are planned for Phase 2 based on demand from the pilot.

---

## Pacing Options

The five experiences can be consumed at different paces. These are not separate content — they are different rhythms for moving through the same material.

| Pace | What It Means | How It Works |
|---|---|---|
| **Self-Paced** | Work through experiences on Blackboard at your own speed | Default — always available |
| **AI in 5** | 5-minute daily micro-challenges that build curiosity and link to the full experiences | Blackboard announcements, emailed daily |
| **Weekly** | One experience per week for five weeks | Self-directed — suggested schedule on the Arrivals Hall |
| **Workshop** | 2-hour face-to-face guided session covering selected experiences hands-on | Delivered by AI Facilitator or trained champions, advertised on Blackboard |

### AI in 5

A daily micro-challenge delivered via Blackboard Announcements with "send immediately" enabled, so it arrives in staff email inboxes. Five days a week, themed:

| Day | Theme | Example |
|---|---|---|
| Monday | Tools | "Try asking AI to generate three discussion questions for your next meeting. How do they compare to yours?" |
| Tuesday | Prompts | "Write a prompt asking AI to summarise something from your field. What did it get right? What did it miss?" |
| Wednesday | Ethics | "A colleague submits a report mostly written by AI. Where's the line?" |
| Thursday | Practice | "Draft one email you need to send today with AI assistance. Was it faster? Better?" |
| Friday | Share | "What's one thing you tried with AI this week? Register it on the AI Exchange." |

Content is created weekly or batched in advance. Date-restricted announcements can be pre-loaded; the email trigger is activated manually each morning (~2 minutes).

### Workshops

Face-to-face workshops deliver the same content as Blackboard in a guided format. Upcoming workshops are advertised on the Arrivals Hall landing page and via AI in 5 announcements. Workshops can be requested by discipline groups or teams — this is the mechanism for training champions (train-the-trainer) and scaling the facilitator role.

---

## Platform 1: Blackboard — "The Passport Office"

### Purpose

Blackboard is the single platform for all structured learning, daily micro-challenges, and credential tracking. Staff self-enrol once and have access to everything.

### Site Specification

| Item | Detail |
|---|---|
| **Site Name** | The AI Skills Passport |
| **Site Type** | Blackboard Organisation (Classic) |
| **Enrolment** | Self-enrolment, open to all SoMM staff |
| **Key Features** | Announcements (AI in 5), Content Areas (experiences), Grade Centre (badge tracking via BadgeQuest) |

### Sidebar Structure

| Sidebar Item | Type | Purpose |
|---|---|---|
| **The Arrivals Hall** | Content Area (Entry Point) | Landing page — orientation, pacing guide, workshop schedule |
| **AI in 5** | Announcements (renamed) | Daily micro-challenges, emailed to all enrolled staff |
| **Is This AI?** | Content Area | Experience 1: Detection & Awareness |
| **What Would You Do?** | Content Area | Experience 2: Ethics & Dilemmas |
| **Rules of Engagement** | Content Area | Experience 3: Policy & Governance |
| **AI-Proof Your Assessments** | Content Area | Experience 4: Assessment Design |
| **Teaching WITH AI** | Content Area | Experience 5: Co-Creation & Integration |
| **My Passport** | Content Area | Badge overview, progress tracking |

Everything else hidden: Information, Contacts, Discussions, Tools, Collaborate Ultra, Groups, My Grades.

### Badge Tracking (BadgeQuest)

Badges are tracked via emoji stamps in Blackboard's Grade Centre using the BadgeQuest system. Grade Centre text columns store emoji values visible to members.

| Badge | Emoji | Criteria |
|---|---|---|
| Explorer | 🧪 | Complete 1 experience |
| Thinker | 🧠 | Complete 3 experiences |
| Builder | 🛠️ | Complete all 5 experiences |
| AI in 5 Streak | ☕ | 30 daily check-ins |
| Workshop Participant | 🎓 | Attend a face-to-face workshop |
| Champion | 🏆 | Complete all experiences + facilitate or mentor others |

### LMS Transition

Blackboard is being retired end of 2026, replaced by Canvas. The design accounts for this:

- Courseware is authored in Quarto and embedded/linked — not built natively in Blackboard. Migration is re-linking, not re-authoring.
- The Blackboard site is a thin shell: sidebar navigation, HTML landing pages, announcements, and grade columns. Rebuilding this in Canvas is a day's work.
- BadgeQuest is LMS-portable — Canvas also supports text in gradebook columns.
- Don't over-invest in Blackboard-specific features (adaptive release chains, complex rules). Keep it simple.

---

## Platform 2: The AI Exchange — "The Registry"

### Purpose

The AI Exchange answers two questions:

1. **"What's actually happening with AI in this school?"** — Even partial voluntary registration creates visibility that didn't exist before. Valuable for the facilitator role and for leadership reporting.

2. **"Who else is working on something like this?"** — Staff can find peers in their own discipline rather than routing everything through the AI Facilitator. Some people won't approach the designated AI person — but they will search for a colleague doing something similar.

### What It Is

A voluntary internal registry where SoMM staff record AI-related activities, search for what others are doing, find potential collaborators, and generate reports on AI adoption. It is a discovery and connection tool, not a learning platform.

### What It Is Not

The Exchange does not host learning content, pathways, or badges. That is Blackboard's job. If someone wants to learn, they go to Blackboard. If someone wants to see what others are doing or find someone to talk to, they go to the Exchange.

### Key Features

- **Nine resource types:** Requests, Use Cases, Prompts, Tools, Policies, Papers, Projects, Conferences, Datasets
- **Verified Anonymity:** Post anonymously while verified as SoMM staff — encourages honest sharing of failures
- **Discipline-based discovery:** Filter by discipline, AI tool, application type, outcome
- **Peer connection:** "Working on Similar?" collaboration workflow, author contact cards
- **Auto-tagging:** YAKE keyword extraction
- **Subscriptions and notifications:** Email alerts for matching resources
- **Reporting:** Visibility into AI adoption across the school

### Technical Details

| Item | Detail |
|---|---|
| **Stack** | FastAPI (Python), React + TypeScript |
| **Database** | SQLite (pilot), PostgreSQL (production) |
| **Auth** | Curtin email domain locking (@curtin.edu.au) |
| **Deployment** | Docker |
| **Hosting (Pilot)** | Desktop machine, Curtin internal network, VPN-accessible |
| **Source** | Open source (MIT) — [github.com/michael-borck/the-ai-exchange](https://github.com/michael-borck/the-ai-exchange) |

### Adoption Strategy

The Exchange is voluntary. The strategy:

- **Seed with real content** — 6–8 genuine use cases before launch, including at least one honest failure
- **Sell stories, not the platform** — short demos showing a real connection or discovery
- **Friday AI in 5** — the weekly "Share" prompt nudges people toward the Exchange
- **Live demos** during workshops — register a use case together in the session
- **One good connection** — if one person finds a collaborator, that story spreads

---

## Cross-Platform Integration

The two platforms reference each other at natural points but operate independently.

| From | To | Trigger |
|---|---|---|
| Blackboard (AI in 5 Friday) | AI Exchange | "Register what you tried this week →" |
| Blackboard (experience completion) | AI Exchange | "Share what you built →" |
| Blackboard (Arrivals Hall) | AI Exchange | Quick link on landing page |
| AI Exchange (use case) | Blackboard | "Build this skill →" link to relevant experience |
| Workshop | Both | Participants enrol in Blackboard and register a use case on the Exchange |

---

## Implementation Plan

### Phase 0 — Infrastructure (Weeks 1–2)

| Task | Platform |
|---|---|
| Configure Blackboard sidebar and enrolment | Blackboard |
| Build Arrivals Hall landing page (HTML) | Blackboard |
| Create content area shells for all 5 experiences | Blackboard |
| Set up My Passport page and Grade Centre badge columns | Blackboard |
| Rename Announcements → AI in 5 | Blackboard |
| Scaffold Quarto project for courseware | Courseware |
| Finalise AI Exchange frontend, seed with 6–8 use cases | AI Exchange |

### Phase 1 — Soft Launch (Weeks 3–4)

| Task | Detail |
|---|---|
| Open self-enrolment | Announce via school newsletter and email |
| Start AI in 5 | Daily announcements, Monday–Friday |
| Populate first 2 experiences with Quarto content | "Is This AI?" and "What Would You Do?" |
| Run first taster workshop | "AI-Proof Your Assessments" face-to-face |
| Recruit 3–5 early adopters across roles | Personal invitations |

**Target:** 10–15 enrolled staff. Focus on engagement quality over numbers.

### Phase 2 — Build Out (Weeks 5–8)

| Task | Detail |
|---|---|
| Populate remaining 3 experiences | "Rules of Engagement", "AI-Proof Your Assessments", "Teaching WITH AI" |
| Open AI Exchange for broad registration | Announce with seeded content visible |
| Run second workshop | Different experience, potentially for a specific discipline group |
| Issue first badges | Update Grade Centre for early completers |

**Target:** 25–30 enrolled. First organic sharing on the AI Exchange.

### Phase 3 — Sustain and Grow (Weeks 9–12)

| Task | Detail |
|---|---|
| Identify and recruit first champion(s) | Staff who've completed multiple experiences and want to facilitate |
| Run a discipline-specific workshop | Champion co-delivers, building train-the-trainer capability |
| Add research-specific and/or admin-specific experiences if demand warrants | Based on pilot feedback |
| Report to leadership | Participation, completion, Exchange data, qualitative stories |

### Reaching "The Unconverted"

**Problem-first invitations.** Don't invite people to "AI Training." Invite them to "AI-Proof Your Assessments" — solving a problem they already have.

**AI in 5 via email.** Five minutes in their inbox every morning. No login required. Lowest possible barrier.

**Non-threatening names.** "Rules of Engagement" sounds like governance. "Is This AI?" sounds like a game. Neither assumes you should already be using AI.

**Quiet browsing.** Sceptics can browse the AI Exchange anonymously to see what peers are doing.

**Workshops for specific teams.** "Can you run a session for our discipline group?" is easier to say yes to than "should I sign up for AI training?"

---

## Success Metrics

| Category | Metric | Target (Pilot) |
|---|---|---|
| **Reach** | Self-enrolments in Blackboard | 30+ staff |
| **Diversity** | Staff from teaching, research, and admin | At least 5 per role |
| **Engagement** | Completed ≥1 experience | 20+ staff |
| **Habit** | AI in 5 sustained readership (email opens) | Qualitative — are people replying/reacting? |
| **Depth** | Completed all 5 experiences | 5–10 staff |
| **Registry** | AI Exchange entries | 15+ use cases |
| **Connection** | Peer contacts via Exchange | Any |
| **Workshops** | Attendance at face-to-face sessions | 10+ per session |
| **Champions** | Staff willing to co-facilitate | 1–2 |
| **The Real Metric** | "You HAVE to try this!" | Unmeasurable but unmistakable |

---

## Governance and Maintenance

### Roles

| Role | Responsibility |
|---|---|
| **AI Facilitator** (Michael Borck) | Program ownership, content authoring (Quarto), Blackboard admin, AI in 5 posting, workshop delivery, Exchange moderation |
| **Blackboard Admin** (IT/Learning Support) | Site creation, technical support |
| **Champions** (from early completers) | Co-deliver workshops, seed Exchange content, provide discipline-specific examples |

### Ongoing Commitments

| Task | Frequency | Effort |
|---|---|---|
| AI in 5 announcements | Daily (weekdays) | ~2 min/day posting, ~1 hr/week writing |
| Workshop delivery | 1–2 per month | ~2 hrs/session + prep |
| Content updates (Quarto) | Quarterly | ~4 hrs/quarter |
| Exchange moderation | As needed | ~30 min/week |

### Sustainability

Champions co-deliver workshops, reducing facilitator dependency. The AI Exchange enables peer-to-peer learning without the facilitator in the middle. Quarto content is version-controlled and LMS-portable. AI in 5 content can be recycled across semesters with minor updates. The goal is a self-sustaining community, not a permanent training program.

---

## Technical Dependencies

| Component | Technology | Notes |
|---|---|---|
| Learning and credentialing | Blackboard Classic (→ Canvas end 2026) | Site established, self-enrolment enabled |
| Courseware | Quarto | Multi-format output, Git version-controlled |
| Badge tracking | BadgeQuest | Emoji badges via Grade Centre text columns |
| AI Registry | AI Exchange (FastAPI + React, Docker) | Desktop-hosted, Curtin network, VPN-accessible |
| Daily delivery | Blackboard Announcements | "Send immediately" emails to enrolled staff |

---

*This document was prepared with AI assistance and human oversight. All recommendations have been reviewed and adapted for the SoMM institutional context.*

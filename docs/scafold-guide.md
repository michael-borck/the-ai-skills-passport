# The AI Skills Passport — Blackboard Scaffold Guide

**Blackboard Classic/Original — Organisation Site**

---

## Step 1: Clean the Sidebar

**Hide everything except:**
- Announcements (we'll rename this)

**Add these Content Areas** (click `+` above sidebar > Content Area):
1. The Arrivals Hall
2. Is This AI?
3. What Would You Do?
4. Rules of Engagement
5. AI-Proof Your Assessments
6. Working WITH AI
7. My Passport

**Rename Announcements** → **AI in 5**
(Sidebar chevron > Rename Link, or Customisation > Tool Availability)

**Set Entry Point:** Customisation > Teaching Style > Select Entry Point → "The Arrivals Hall"

**Final sidebar (top to bottom):**

```
The Arrivals Hall          ← entry point / landing page
AI in 5                    ← daily micro-challenges (renamed Announcements)
Is This AI?                ← experience 1
What Would You Do?         ← experience 2
Rules of Engagement        ← experience 3
AI-Proof Your Assessments  ← experience 4
Working WITH AI           ← experience 5
My Passport                ← badge tracking
```

---

## Step 2: Configure Enrolment

Customisation > Enrolment Options:
- Enable **Self Enrolment**
- Access code: blank (no barrier) or a simple code to share

---

## Step 3: Populate Content Areas

For each content area, create an **Item** (Build Content > Item), switch to **HTML/Code view**, and paste the corresponding HTML file.

| Content Area | HTML File | Notes |
|---|---|---|
| The Arrivals Hall | `arrivals-hall.html` | Landing page — orientation, pacing guide, quick links |
| Is This AI? | `coming-soon.html` (until Quarto content ready) | Replace with actual content when available |
| What Would You Do? | `coming-soon.html` | Replace with actual content when available |
| Rules of Engagement | `coming-soon.html` | Replace with actual content when available |
| AI-Proof Your Assessments | `coming-soon.html` | Replace with actual content when available |
| Working WITH AI | `coming-soon.html` | Replace with actual content when available |
| My Passport | `my-passport.html` | Badge overview and how it works |

---

## Step 4: AI in 5 (Daily Announcements)

1. Go to **AI in 5** in the sidebar
2. Click **Create Announcement**
3. Write the daily challenge (~50-100 words, include a question or task)
4. Check **"Send a copy of this announcement immediately"**
5. Post each weekday morning (~2 minutes)

**Weekly theme schedule:**
- Monday: Tools
- Tuesday: Prompts
- Wednesday: Ethics
- Thursday: Practice
- Friday: Share (nudge toward AI Exchange)

Optionally batch-create with Date Restrict for the announcements area, then manually trigger the email each morning.

---

## Step 5: Badge Columns (BadgeQuest)

Grade Centre > Create Column (for each badge):
- Type: Text
- Points Possible: 0

| Column Name | Emoji | Criteria |
|---|---|---|
| Explorer | 🧪 | Complete 1 experience |
| Thinker | 🧠 | Complete 3 experiences |
| Builder | 🛠️ | Complete all 5 experiences |
| AI in 5 Streak | ☕ | 30 daily check-ins |
| Workshop Participant | 🎓 | Attend face-to-face session |
| Champion | 🏆 | All experiences + facilitate/mentor |

---

## Step 6: Smoke Test

Switch to Student Preview and verify:

- [ ] Lands on The Arrivals Hall
- [ ] All 8 sidebar items visible
- [ ] Admin/Control Panel NOT visible
- [ ] AI in 5 shows announcements
- [ ] Each experience shows content or coming-soon placeholder
- [ ] My Passport shows badge explanation

---

## Files

| File | Purpose |
|---|---|
| `arrivals-hall.html` | Main landing page |
| `my-passport.html` | Badge overview |
| `coming-soon.html` | Placeholder for experiences not yet populated |

All HTML uses inline CSS only — no `<style>` tags, no external files.

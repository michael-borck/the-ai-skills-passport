# Blackboard Scaffold Guide

**Blackboard Classic/Original — Organisation Site**

Blackboard is just a shell — authentication, announcements, and a launch point. All real content lives in SPAs that open in new tabs.

---

## Design Philosophy

- **Minimal Blackboard footprint** — we're migrating to Canvas late 2026
- **SPAs do the heavy lifting** — rich, interactive, platform-independent
- **Arrivals Hall is the hub** — one beautiful landing page, not a cluttered sidebar
- **3 sidebar items only** — clean, purposeful, not typical LMS clutter

---

## Step 1: Clean the Sidebar

**Hide everything** except Announcements.

**Add only these Content Areas:**
1. The Arrivals Hall
2. My Passport

**Rename Announcements** → **AI in 5**
(Sidebar chevron → Rename Link)

**Set Entry Point:**
Customisation → Teaching Style → Select Entry Point → "The Arrivals Hall"

---

## Step 2: Final Sidebar (3 items only)

```
The Arrivals Hall    ← entry point, the hub for everything
AI in 5              ← daily micro-challenges (Announcements)
My Passport          ← badge progress, motivation
```

That's it. Everything else is accessed via links in The Arrivals Hall.

---

## Step 3: Configure Enrolment

Customisation → Enrolment Options:
- Enable **Self Enrolment**
- Access code: leave blank (no barrier) or set a simple code

---

## Step 4: Upload SPAs

Upload all rendered HTML files to Blackboard's Content Collection:

1. Control Panel → Content Collection → course folder
2. Create folder: `ai-passport-spas`
3. Upload all `_site/index.html` files (rename them for clarity):
   - `find-your-path.html`
   - `is-this-ai.html`
   - `what-would-you-do.html`
   - `rules-of-engagement.html`
   - `ai-proof-assessments.html`
   - `teaching-with-ai.html`
   - `ai-toolkit.html`
   - `my-passport.html`

Get the URL for each file (right-click → copy link).

---

## Step 5: Set Up The Arrivals Hall

1. Go to **The Arrivals Hall** content area
2. **Build Content** → **Item**
3. Name it: "Welcome" (or leave blank)
4. Click **HTML** button to switch to code view
5. Paste contents of `blackboard/arrivals-hall.html` (with URLs replaced)
6. Submit

---

## Step 6: Set Up My Passport

1. Go to **My Passport** content area
2. **Build Content** → **Web Link**
3. URL: your uploaded `my-passport.html` URL
4. Check **Open in New Window**
5. Submit

---

## Step 7: AI in 5 Self-Enrollment Group

> ⚠️ **Curtin-specific:** These steps may vary. Check with eLearning support if menus differ.

To let staff opt-in to daily emails:

### Option A: Self-Enrollment Group (if available)

1. **Control Panel** → **Users and Groups** → **Groups**
2. **Create** → **Self-Enroll**
3. Settings:
   - Name: "AI in 5 Daily Challenges"
   - Allow sign-up: Yes
   - Max members: Unlimited
4. Add sign-up link to The Arrivals Hall or sidebar
5. When posting announcements, select this group as recipient

### Option B: Use Organisation Enrollment (simpler)

If group features aren't available on Organisation sites:
1. Anyone enrolled in the site receives announcements
2. Promote the site enrollment link
3. All announcements go to all enrolled users

### Posting Daily Challenges

1. Go to **AI in 5** in sidebar (renamed Announcements)
2. **Create Announcement**
3. Write daily challenge (~50-100 words)
4. Check **"Send a copy immediately"**
5. Post each weekday morning

**Weekly themes:**
- Monday: Tools
- Tuesday: Prompts
- Wednesday: Ethics
- Thursday: Practice
- Friday: Share

---

## Step 8: Smoke Test

Student Preview mode:

- [ ] Lands on The Arrivals Hall
- [ ] Only 3 sidebar items visible
- [ ] Arrivals Hall looks polished (not like typical Blackboard)
- [ ] All experience links open SPAs in new tabs
- [ ] Find Your Path quiz works
- [ ] My Passport shows badge progress
- [ ] AI in 5 shows announcements
- [ ] No admin clutter visible

---

## What Lives Where

| Component | Location | Why |
|-----------|----------|-----|
| Arrivals Hall | Blackboard Item (embedded HTML) | Entry point, always visible |
| AI in 5 | Blackboard Announcements | Email delivery, daily engagement |
| My Passport | Link to SPA | Sidebar visibility for motivation |
| Everything else | SPAs via Arrivals Hall links | Rich UX, platform-independent |

---

## Migration Notes

When moving to Canvas (late 2026):

1. SPAs don't change — just re-upload HTML files
2. Create new landing page (paste arrivals-hall.html)
3. Update URLs in arrivals-hall.html
4. Set up announcement equivalent for AI in 5

The SPAs are the product. The LMS is just the wrapper.

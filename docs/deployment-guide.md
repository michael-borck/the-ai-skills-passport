# Deployment Guide

How to build the SPAs and deploy everything to Blackboard.

---

## Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Quarto (.qmd)  │ ──► │  HTML (render)  │ ──► │   Blackboard    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                       │
                                                       ▼
                                               ┌─────────────────┐
                                               │ Progress Server │
                                               │   (optional)    │
                                               └─────────────────┘
```

**SPAs to deploy:**
- `onboarding/` → Find Your Path quiz
- `resources/` → AI Toolkit
- `passport/` → My Passport (badge tracker)
- `experiences/is-this-ai/`
- `experiences/what-would-you-do/`
- `experiences/rules-of-engagement/`
- `experiences/ai-proof-assessments/`
- `experiences/teaching-with-ai/`

---

## Step 1: Render All SPAs

Each folder is a Quarto project. Render them to self-contained HTML:

```bash
cd /Users/michael/Projects/the-ai-skills-passport

# Render each SPA
quarto render onboarding/
quarto render resources/
quarto render passport/
quarto render experiences/is-this-ai/
quarto render experiences/what-would-you-do/
quarto render experiences/rules-of-engagement/
quarto render experiences/ai-proof-assessments/
quarto render experiences/teaching-with-ai/
```

Or render all at once:
```bash
for dir in onboarding resources passport experiences/*/; do
  echo "Rendering $dir..."
  quarto render "$dir"
done
```

Output files will be in each folder's `_site/` directory (e.g., `onboarding/_site/index.html`).

---

## Step 2: Upload to Blackboard

For each SPA, upload the rendered HTML file to Blackboard:

1. Go to the relevant **Content Area** in Blackboard (e.g., "Is This AI?")
2. **Build Content** → **File**
3. Browse and upload the `index.html` from the `_site/` folder
4. Set **Open in New Window: Yes**
5. Click **Submit**

**Alternatively**, use the Blackboard Content Collection:
1. Control Panel → Content Collection → course folder
2. Upload all HTML files to a subfolder (e.g., `/ai-passport-spas/`)
3. Link to them from Content Areas

---

## Step 3: Get Blackboard URLs

After uploading, get the URL for each file:

1. Click on the uploaded file link
2. Copy the URL from your browser
3. It will look something like:
   ```
   https://lms.curtin.edu.au/bbcswebdav/xid-12345678_1
   ```

Record all URLs:

| SPA | Placeholder | Blackboard URL |
|-----|-------------|----------------|
| Find Your Path | `[ONBOARDING_URL]` | `https://...` |
| Is This AI? | `[EXP1_URL]` | `https://...` |
| What Would You Do? | `[EXP2_URL]` | `https://...` |
| Rules of Engagement | `[EXP3_URL]` | `https://...` |
| AI-Proof Assessments | `[EXP4_URL]` | `https://...` |
| Working WITH AI | `[EXP5_URL]` | `https://...` |
| AI Toolkit | `[TOOLKIT_URL]` | `https://...` |
| My Passport | `[PASSPORT_URL]` | `https://...` |
| The AI Exchange | `[EXCHANGE_URL]` | `https://...` (external app) |
| AI Rubric Pack | `[RUBRIC_URL]` | `https://...` (Word docs) |

---

## Step 4: Update Arrivals Hall

1. Open `blackboard/arrivals-hall.html` in a text editor
2. Find and replace each placeholder with the actual Blackboard URL:
   - `[ONBOARDING_URL]` → your Find Your Path URL
   - `[EXP1_URL]` → your Is This AI? URL
   - etc.
3. The `@X@user.batch_uid@X@` part stays as-is. Blackboard replaces this with the user's ID

---

## Step 5: Paste Arrivals Hall into Blackboard

1. Go to **The Arrivals Hall** content area
2. **Build Content** → **Item**
3. Give it a name (e.g., "Welcome")
4. In the text editor, click the **HTML** button (or `<>` icon) to switch to code view
5. Paste the entire contents of `arrivals-hall.html`
6. Click **Submit**

---

## Step 6: Test Everything

Switch to **Student Preview** mode and verify:

- [ ] Arrivals Hall displays correctly
- [ ] "Find Your Path" button opens the quiz in a new tab
- [ ] Each experience card is clickable and opens the SPA
- [ ] AI Toolkit link works
- [ ] My Passport link works
- [ ] Completing an experience updates localStorage
- [ ] My Passport shows completion (in same browser)

---

## Optional: Progress Tracker Server

For persistent tracking across browsers/devices:

### Start the server

```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Server runs at `http://localhost:5050` (or your machine's IP for network access).

### Find your IP

```bash
# Mac
ipconfig getifaddr en0

# Windows
ipconfig
```

### Update SPAs to use server

In each experience's completion JavaScript, update the `recordCompletion` function to POST to the server:

```javascript
fetch('http://YOUR_IP:5050/complete', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    uid: uid,
    experience: 'is-this-ai'  // change per experience
  })
});
```

### Update My Passport

Update `passport/index.qmd` to fetch from the server instead of localStorage:

```javascript
fetch(`http://YOUR_IP:5050/progress/${uid}`)
  .then(res => res.json())
  .then(data => {
    // Use data.completions, data.badges
  });
```

---

## Quick Reference

| What | Where |
|------|-------|
| Arrivals Hall HTML | `blackboard/arrivals-hall.html` |
| SPA source files | `*/index.qmd` |
| Rendered SPAs | `*/_site/index.html` |
| Progress server | `server/app.py` |
| Scaffold guide | `docs/scaffold-guide.md` |

---

## Troubleshooting

**Links not working?**
- Check that URLs include `?uid=@X@user.batch_uid@X@`
- Verify "Open in New Window" is enabled

**Styling looks broken?**
- Ensure you pasted into HTML/code view, not rich text view
- Blackboard strips `<style>` tags, so all CSS must be inline (it already is)

**Progress not persisting?**
- localStorage is browser-specific
- Use the progress tracker server for cross-browser/device persistence

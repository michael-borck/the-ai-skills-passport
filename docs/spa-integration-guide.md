# SPA Integration Guide

This document describes the modifications needed to connect the SPAs to the progress tracker server. These changes have **not been implemented** in the current MVP — see [Data Governance](data-governance.md) for why.

## Overview

The integration requires three things:

1. **Pass the Blackboard UID into each SPA** via URL query parameter
2. **POST a completion** to the server when a user finishes an experience
3. **Fetch progress** from the server to display badges on the My Passport page

## Step 1: Pass the UID from Blackboard

Blackboard supports **URL variable substitution**. When configuring the redirect URL in Blackboard, append the UID as a query parameter:

```
https://your-content-host/arrivals-hall.html?uid=@X@user.batch_uid@X@
```

Blackboard replaces `@X@user.batch_uid@X@` with the logged-in user's batch UID at runtime. The Arrivals Hall then propagates this UID to all experience links.

### Propagating the UID Between SPAs

When the Arrivals Hall generates links to experiences, append the UID:

```javascript
// Read UID from query string
const params = new URLSearchParams(window.location.search);
const uid = params.get('uid');

// Append to all experience links
document.querySelectorAll('a[href*="experiences/"]').forEach(link => {
  if (uid) {
    const url = new URL(link.href, window.location.origin);
    url.searchParams.set('uid', uid);
    link.href = url.toString();
  }
});
```

## Step 2: Record Completions

Each experience SPA needs a completion trigger — a JavaScript function that fires when the user has meaningfully engaged with the content (e.g. reached the final section, clicked a "Mark Complete" button, or submitted a reflection).

```javascript
// UID from query string
const uid = new URLSearchParams(window.location.search).get('uid');

// Server base URL
const SERVER_URL = 'http://localhost:5050';  // Update for production

async function recordCompletion(experience) {
  // Always save to localStorage as fallback
  const completions = JSON.parse(localStorage.getItem('passport-completions') || '{}');
  completions[experience] = new Date().toISOString();
  localStorage.setItem('passport-completions', JSON.stringify(completions));

  // If UID available, also POST to server
  if (uid) {
    try {
      await fetch(`${SERVER_URL}/complete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uid, experience })
      });
    } catch (err) {
      console.warn('Server unavailable, completion saved to localStorage only');
    }
  }
}

// Example: call when user completes the experience
recordCompletion('is-this-ai');
```

**Key points:**
- Always write to localStorage first (graceful fallback)
- Only POST to server if a UID is present (no UID = no server tracking)
- Catch network errors silently — the user experience should not break if the server is down

## Step 3: Fetch Progress for My Passport

The My Passport page needs to display badges. With server integration, it can fetch the canonical progress from the server and merge with localStorage.

```javascript
const uid = new URLSearchParams(window.location.search).get('uid');
const SERVER_URL = 'http://localhost:5050';

async function loadProgress() {
  // Start with localStorage data
  let completions = JSON.parse(localStorage.getItem('passport-completions') || '{}');

  // If UID available, try to fetch server data
  if (uid) {
    try {
      const response = await fetch(`${SERVER_URL}/progress/${uid}`);
      if (response.ok) {
        const data = await response.json();
        // Merge: server is authoritative, localStorage fills gaps
        completions = { ...completions, ...data.completions };
        // Update localStorage with merged data
        localStorage.setItem('passport-completions', JSON.stringify(completions));
        return data;  // Server response includes badges
      }
    } catch (err) {
      console.warn('Server unavailable, using localStorage only');
    }
  }

  // Fallback: calculate badges from localStorage
  const count = Object.keys(completions).length;
  const badges = [];
  if (count >= 1) badges.push({ id: 'explorer', emoji: '🧪', name: 'Explorer' });
  if (count >= 3) badges.push({ id: 'thinker', emoji: '🧠', name: 'Thinker' });
  if (count >= 5) badges.push({ id: 'builder', emoji: '🛠️', name: 'Builder' });
  if (count >= 7) badges.push({ id: 'champion', emoji: '🏆', name: 'Champion' });

  return { completions, completed_count: count, badges };
}
```

## Summary of Changes by SPA

| SPA | Change Required |
|---|---|
| **Arrivals Hall** | Read `uid` from query string, propagate to all experience and passport links |
| **Each experience** | Add `recordCompletion()` call with the experience slug |
| **My Passport** | Fetch progress from server, merge with localStorage, display badges |
| **Find Your Path** | No change needed (quiz only, no completion) |
| **AI Toolkit** | No change needed (reference material, no completion) |
| **Key Takeaways** | No change needed (summary page, no completion) |

## Server URL Configuration

The server URL (`SERVER_URL`) should be configurable. Options:

- **Hardcoded** — simplest for the pilot, update before deployment
- **Query parameter** — pass `?server=https://...` alongside the UID
- **Relative URL** — if server and SPAs are co-hosted (unlikely in Blackboard scenario)

For the pilot, a hardcoded URL pointing to the desktop server on the Curtin internal network is the most pragmatic approach.

## Prerequisites

Before implementing these changes:

1. Data governance approval obtained — see [Data Governance](data-governance.md)
2. Server hosted in an appropriate environment
3. Server URL known and accessible from Blackboard-hosted SPAs
4. Blackboard URL variable substitution configured for the redirect

## Related Documents

- [Data Governance](data-governance.md) — privacy considerations that must be resolved first
- [Progress Tracker API](progress-tracker-api.md) — full API reference
- [Deployment Guide](deployment-guide.md) — build and deploy instructions

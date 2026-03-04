# Data Governance

## Overview

The AI Skills Passport progress tracker server records experience completions against a user identifier — specifically, the **Blackboard UID** passed via URL variable substitution. This document outlines the data governance considerations that must be resolved before the server is integrated into the SPAs.

## The Problem

Although the SPAs are hosted within Blackboard's Content Collection and users require a Curtin University account to access them, the **progress tracker server** is a separate service that needs its own hosting. The server stores Blackboard UIDs in a SQLite database to associate users with their completed experiences.

The core issue is not _whether_ we store the UID, but **where the database that stores it resides**:

- The SPAs live inside Blackboard — a Curtin-managed, institutionally governed platform
- The progress tracker server currently runs on a desktop machine on the Curtin internal network
- The SQLite database containing UIDs sits on that desktop machine, outside of any institutionally managed data storage

This creates a gap between where users authenticate (Blackboard, governed by Curtin policies) and where their progress data would be stored (a local machine, without formal data governance).

## What the Server Stores

| Data | Example | Sensitivity |
|---|---|---|
| Blackboard UID | `borckm` or batch UID string | Personally identifiable — maps to a specific staff member |
| Experience slug | `is-this-ai` | Not sensitive |
| Completion timestamp | `2026-03-04T10:30:00` | Not sensitive on its own |

The UID is the sensitive element. Combined with the completion records, it creates a profile of which staff have (or have not) engaged with AI professional development. Even in a voluntary programme, this data requires careful handling.

## Why This Matters

1. **No institutional sandbox available.** Curtin does not currently appear to offer a sandboxed server environment where this kind of lightweight application could run under institutional data governance. If such an environment existed, the server could be deployed there with appropriate data handling policies.

2. **Blackboard UID is institutional data.** The `batch_uid` passed by Blackboard is controlled by Curtin's identity systems. Storing it in an external database — even on the internal network — may require approval from IT governance or the privacy office.

3. **Voluntary participation must remain genuinely voluntary.** If progress data is stored server-side and linked to identifiable UIDs, there is a risk (real or perceived) that participation could be monitored. This could undermine the "start anywhere, no pressure" philosophy of the initiative.

4. **Data retention and access.** Questions to resolve include: who can access the database? How long is data retained? Can users request deletion? What happens when the project ends?

## Current MVP Approach

For the MVP, all progress tracking uses **browser localStorage**:

- Completion records are stored in the user's browser only
- No server-side storage of UIDs or progress data
- Data does not leave the user's device
- If a user clears their browser data or uses a different device, progress is lost

This approach deliberately avoids the data governance issues while still providing a functional progress tracking experience for the pilot.

## Path to Server Integration

Before enabling server-side progress tracking, the following steps are needed:

1. **Consult Curtin's privacy/data governance team** about storing Blackboard UIDs in an application database, even on the internal network
2. **Identify appropriate hosting** — ideally an institutionally managed server or container environment with appropriate data handling policies
3. **Define a data retention policy** — how long records are kept, who has access, deletion procedures
4. **Consider anonymisation options** — could a hashed or pseudonymised identifier replace the raw Blackboard UID?
5. **Update the SPAs** to connect to the server — see [SPA Integration Guide](spa-integration-guide.md)
6. **Communicate transparently** with participants about what data is stored and why

## Related Documents

- [Progress Tracker API](progress-tracker-api.md) — server API reference
- [SPA Integration Guide](spa-integration-guide.md) — modifications needed to connect SPAs to the server

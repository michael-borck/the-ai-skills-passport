> This content is from the AI Toolkit resource: Beyond the God Prompt: A Blueprint for Reliable Chatbot Architecture, part of the AI Skills Passport for SoMM staff at Curtin University.

# Beyond the God Prompt: A Blueprint for Reliable Chatbot Architecture

## The Problem with Monolithic Prompts

Engineering teams frequently attempt to solve chatbot reliability through prompt engineering alone -- writing increasingly comprehensive system prompts that anticipate every business rule, every edge case, and every possible user response. This is the "God Prompt" approach. The belief is that a sufficiently detailed prompt will make the LLM behave predictably.

In practice, it doesn't work. When a single prompt must simultaneously manage strict sequencing, complex rules, and a specific persona, reasoning degrades. The model begins to "sway" -- following negative examples provided to show what *not* to do, or getting confused by contradictory instructions buried thousands of tokens deep. You might achieve a 30% success rate where the logic holds but the tone is wrong, or the tone is right but critical protocols are ignored.

> "You just can't describe it all up front. When you create God Prompts like this, it just doesn't work."

Reliability requires a governed, opinionated workflow -- not a single prompt trying to do everything at once.

---

## The Three-Phase Sandwich Architecture

The alternative is a three-phase design pattern that sandwiches deterministic logic between two specialised LLM layers. Each layer has a single responsibility, which makes the system significantly easier to test and debug.

### Phase 1: The Analyst (Fact Extraction)

A fast LLM layer performs a first pass on the conversation to extract structured tags: the user's tone, the current topic, the conversation state. Its only job is to identify facts -- not to respond.

### Phase 2: The Engine (Deterministic Logic)

The extracted facts are passed to a classical code engine -- not an AI. This scenario handler maps combinations of facts to specific business rules. If the Analyst identifies an angry user discussing a billing dispute, the Engine maps those facts to the exact protocol for that situation.

The Engine does not generate language. It generates instructions -- and it also triggers deterministic side effects: logging to a database, scheduling a follow-up, escalating to a human supervisor. These actions happen reliably because they are code, not inference.

### Phase 3: The Composer (Tone Layer)

A second LLM layer takes the Engine's specific instructions and drafts the response. Because the Composer is only responsible for phrasing a predetermined message, it can focus entirely on voice and tone without needing to reason about underlying logic.

The separation is the point. Logic lives in code. Language lives in the LLM. Neither is asked to do the other's job.

---

## Cascading Analysis: Solving Latency and Cost

A common concern about multi-phase architectures is that breaking one prompt into several steps will increase latency and cost. Counter-intuitively, prompt fragmentation usually improves both.

The strategy is **cascading analysis**:

- **Shallow pass** -- a fast, cheap model identifies the broad topic category
- **Deep-dive** -- once the topic is known, a targeted analyser prompt fires using only the context relevant to that topic

By sending only relevant context to the deeper layer, the system avoids the "tipping point" where too much context degrades reasoning. The results:

- **Lower latency** -- parallelised sub-queries execute faster than one large sequential prompt
- **Lower cost** -- reduced token consumption by trimming irrelevant context
- **Higher accuracy** -- eliminating unrelated rules prevents the model from being swayed by contradictory examples

---

## Regression Testing: The 10% Rule

In a system with thousands of potential conversation paths, manual testing is not feasible. Tweaking a prompt to fix a tone issue in one branch can silently break logic in dozens of others.

A practical baseline: allocate **5--10% of total project budget** specifically for building regression testing tools. The approach that works well is using the LLM itself to generate a library of test conversations -- starting with representative scenarios and scaling to hundreds -- then running them simultaneously after any change. If you cannot run a smoke test of your core happy-path cases in minutes, the system is not ready for production.

---

## The "Too Fast" Problem

In optimising for low latency, there is a counterintuitive UX issue: the bot can be too fast. Receiving a multi-paragraph, perfectly formatted response the instant you hit send feels jarringly artificial in contexts where human connection matters.

The solution is often to "fake" a human pace on the frontend -- moving from instant streaming to a more deliberate cadence. Production reliability is not just about technical throughput; it is also about whether the user's experience feels trustworthy.

---

## The Human Safety Valve

Deterministic architectures are not a total replacement for human judgment. No matter how many scenario handlers are built, a user will eventually veer outside the system's design -- a personal crisis, an unexpected topic, a situation that requires genuine discretion.

Every production chatbot needs a **safety valve**: a clear protocol for the bot to recognise when it is out of its depth and hand the conversation to a human operator. Knowing when to exit autopilot is a strategic necessity for maintaining trust, not an admission of failure.

The question to ask of any chatbot deployment is not just "how well does it handle the expected cases?" but "what happens when something unexpected occurs -- and who is responsible for that moment?"

---

*This resource draws on production experience with deterministic chatbot architectures in high-stakes service environments. The principles apply across domains wherever reliable, auditable AI-assisted communication is required.*

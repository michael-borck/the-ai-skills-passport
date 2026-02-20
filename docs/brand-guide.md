# Brand & Style Guide

**AI Skills Passport: Visual Identity**

---

## Colour Palette

The palette is based on Tailwind CSS colours for consistency and accessibility.

### Primary Colours

| Name | Hex | Usage |
|------|-----|-------|
| **Slate 900** | `#0F172A` | Dark headers, primary text on light backgrounds |
| **Slate 800** | `#1E293B` | Header gradients, dark backgrounds |
| **Slate 700** | `#334155` | Body text |
| **Slate 500** | `#64748B` | Secondary text, labels |
| **Slate 400** | `#94A3B8` | Muted text, placeholders |
| **Slate 200** | `#E2E8F0` | Borders, dividers |
| **Slate 100** | `#F1F5F9` | Light backgrounds, cards |
| **Slate 50** | `#F8FAFC` | Page backgrounds |

### Accent Colours

| Name | Hex | Usage |
|------|-----|-------|
| **Indigo 600** | `#4F46E5` | Primary actions, links, buttons |
| **Indigo 700** | `#4338CA` | Hover states, emphasis |
| **Indigo 900** | `#312E81` | Dark indigo text |
| **Indigo 100** | `#EEF2FF` | Indigo light backgrounds |
| **Indigo 200** | `#E0E7FF` | Indigo borders |

### Status Colours

| Name | Hex | Usage |
|------|-----|-------|
| **Green 500** | `#22C55E` | Success, completion, positive |
| **Green 600** | `#16A34A` | Green buttons, hover |
| **Green 800** | `#166534` | Green dark text |
| **Green 900** | `#14532D` | Green headers |
| **Green 100** | `#DCFCE7` | Green light background |
| **Green 50** | `#F0FDF4` | Green very light background |
| **Amber 500** | `#F59E0B` | Warning, attention |
| **Amber 800** | `#92400E` | Amber dark text |
| **Amber 100** | `#FEF3C7` | Amber light background |
| **Red 800** | `#991B1B` | Error, negative |
| **Red 100** | `#FEE2E2` | Red light background |

### Special Colours

| Name | Hex | Usage |
|------|-----|-------|
| **Violet 600** | `#7C3AED` | Secondary accent, gradients |
| **Fuchsia 300** | `#E879F9` | AI Exchange branding |
| **Fuchsia 900** | `#701A75` | AI Exchange text |

---

## Typography

### Font Stack
```css
font-family: Georgia, 'Times New Roman', serif;  /* Body text */
font-family: 'Courier New', Consolas, monospace; /* Headers, labels, code */
```

### Why These Fonts
- **Georgia:** Professional, readable, available everywhere
- **Courier New:** Technical feel, good for labels and headers
- Both are web-safe, no external font loading needed

### CSS Notes
- **SPAs** (served as HTML files from Content Collection): Can use `<style>` tags or external CSS
- **Arrivals Hall** (pasted into Blackboard content item): Must use inline styles only. Blackboard strips `<style>` tags from content items

### Text Sizes
- Page title: 28px
- Section headers: 20-22px
- Card titles: 16-18px
- Body text: 14-15px
- Labels/meta: 11-13px

---

## Component Patterns

### Cards
- White background (`#FFFFFF`)
- 1px border (`#E2E8F0`)
- 12px border radius
- 20-24px padding
- Hover: border colour changes to indigo (`#4F46E5`)

### Buttons
- Primary: Indigo gradient (`#4F46E5` → `#7C3AED`)
- Success: Green gradient (`#22C55E` → `#16A34A`)
- 8px border radius
- 12-14px padding
- White text, bold

### Headers (dark)
- Gradient: `#0F172A` → `#1E293B`
- 16px border radius
- White/light text
- Courier New font for titles

### Status Badges
- Explorer: 🧪 (1 experience)
- Thinker: 🧠 (3 experiences)
- Builder: 🛠️ (5 experiences)

---

## Accessibility Notes

### Colour Contrast
All text colour combinations should meet WCAG AA (4.5:1 for normal text, 3:1 for large text):
- `#334155` on `#FFFFFF` ✓
- `#FFFFFF` on `#4F46E5` ✓
- `#166534` on `#F0FDF4` ✓
- `#64748B` on `#FFFFFF`, borderline, use for secondary text only

### Interactive Elements
- All clickable elements should have visible focus states
- Buttons should have sufficient padding for touch targets (min 44px)
- Links should be distinguishable by more than just colour

### Content
- Don't rely on colour alone to convey meaning
- Emojis supplement text, don't replace it
- Provide text alternatives for any visual-only content

---

## Voice & Tone

### Writing Style
- **Conversational:** write like you're explaining to a colleague
- **Practical:** focus on what they can do, not theory
- **Encouraging:** normalise learning and experimentation
- **Concise:** respect their time

### Words to Use
- "Try" over "must"
- "Explore" over "complete"
- "Your context" over "the correct way"
- "Conversation" over "delegation"

### Words to Avoid
- Jargon without explanation
- "Simple" or "easy" (subjective)
- Overly formal academic language
- Marketing superlatives

---

## Emoji Usage

Emojis are used sparingly for visual anchors:

| Context | Examples |
|---------|----------|
| Experience icons | 🔍 🤔 📋 🛡️ 🤝 |
| Badges | 🧪 🧠 🛠️ 🏆 |
| Quick links | 📬 🧰 🌐 🏅 |
| Status | ✅ ⚠️ ❌ |
| Time indicators | ⚡ 🗺️ 🎓 |

Don't overuse. One emoji per card/section is usually enough.

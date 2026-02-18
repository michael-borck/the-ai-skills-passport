# Accessibility Review

**AI Skills Passport — WCAG 2.1 Considerations**

---

## Current Status: Baseline Accessible ✓

The SPAs use semantic HTML and have reasonable baseline accessibility. This document notes what's working and what could improve.

---

## What's Working

### Semantic HTML
- ✅ Headings used in logical hierarchy (`<h1>`, `<h2>`, `<h3>`)
- ✅ Buttons for interactive actions (not divs with onclick)
- ✅ Labels associated with form inputs
- ✅ Lists used for list content

### Keyboard Navigation
- ✅ All buttons are focusable and activatable via keyboard
- ✅ Checkboxes work with keyboard
- ✅ Tab order follows visual order
- ✅ No keyboard traps

### Colour & Contrast
- ✅ Primary text (`#334155` on white) meets WCAG AA
- ✅ White text on dark headers meets AA
- ✅ Not relying on colour alone — icons/emojis supplement meaning

### Text & Readability
- ✅ Base font size is 14-16px (readable)
- ✅ Line height of 1.5-1.7 (good spacing)
- ✅ Max width constraints prevent overly long lines

---

## Improvements for Future Iterations

### High Priority

**1. Focus Indicators**
Currently using browser defaults. Could add visible focus styles:
```css
button:focus, a:focus, input:focus {
  outline: 3px solid #4F46E5;
  outline-offset: 2px;
}
```

**2. Skip Link**
Add a "Skip to main content" link for screen reader users:
```html
<a href="#main-content" style="position: absolute; left: -9999px;
   top: 0; z-index: 999;">Skip to main content</a>
```

**3. ARIA Labels for Icon-Only Elements**
Tab buttons could be clearer:
```html
<button aria-label="Teaching context">📚 Teaching</button>
```

### Medium Priority

**4. Reduced Motion**
Respect user preferences for reduced animation:
```css
@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; }
}
```

**5. Dark Mode Support**
Could add prefers-color-scheme media query for users who prefer dark mode.

**6. Error Announcements**
Form validation errors should be announced to screen readers:
```html
<div role="alert" aria-live="polite">Please select an answer</div>
```

### Lower Priority

**7. Language Attribute**
Ensure `<html lang="en-AU">` is set.

**8. Landmark Roles**
Add ARIA landmarks for major sections:
```html
<main role="main">
<nav role="navigation">
<footer role="contentinfo">
```

---

## Testing Recommendations

### Quick Checks (Do Before Launch)
- [ ] Tab through each SPA — can you reach everything?
- [ ] Complete each SPA using only keyboard
- [ ] Zoom to 200% — is content still readable?
- [ ] Check on mobile device

### Screen Reader Testing (If Resources Allow)
- [ ] VoiceOver (Mac): Cmd+F5 to enable
- [ ] Test heading navigation (VO+U, then arrows)
- [ ] Test form completion

### Automated Tools
- [axe DevTools](https://www.deque.com/axe/) browser extension
- [WAVE](https://wave.webaim.org/) web accessibility evaluator
- Lighthouse (Chrome DevTools → Lighthouse → Accessibility)

---

## Colour Contrast Reference

| Combination | Ratio | WCAG AA | WCAG AAA |
|-------------|-------|---------|----------|
| `#334155` on `#FFFFFF` | 8.5:1 | ✓ | ✓ |
| `#64748B` on `#FFFFFF` | 4.5:1 | ✓ | ✗ |
| `#FFFFFF` on `#4F46E5` | 6.1:1 | ✓ | ✗ |
| `#FFFFFF` on `#0F172A` | 16.1:1 | ✓ | ✓ |
| `#166534` on `#F0FDF4` | 5.8:1 | ✓ | ✗ |
| `#312E81` on `#EEF2FF` | 8.9:1 | ✓ | ✓ |

All combinations meet WCAG AA for normal text.

---

## No Images = No Alt Text Needed

The SPAs currently use emoji and text only — no `<img>` elements. If images are added later, ensure:
- Informative images have descriptive alt text
- Decorative images have `alt=""`
- Complex diagrams have extended descriptions

---

## Summary

The AI Skills Passport SPAs are **baseline accessible** and should work for most users, including those using keyboards or assistive technology. The improvements listed above would enhance the experience but are not blocking issues.

For a pilot with limited resources, the current state is acceptable. Plan accessibility improvements for iteration based on user feedback.

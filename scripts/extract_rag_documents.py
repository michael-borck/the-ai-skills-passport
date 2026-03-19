#!/usr/bin/env python3
"""
Extract content from the AI Skills Passport project into clean markdown files
suitable for upload to AnythingLLM (or any RAG system).

Produces:
  rag-documents/
    toolkit/          — Clean markdown from ai-toolkit/downloads/*.qmd
    experiences/      — Text extracted from SPA HTML, split by step
    navigation/       — Key takeaways, onboarding, overview
    references/       — Collated references

Usage:
    python scripts/extract_rag_documents.py
"""

import os
import re
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "rag-documents"

PREAMBLE_TEMPLATE = (
    "> This content is from {source}, part of the AI Skills Passport "
    "for SoMM staff at Curtin University.\n\n"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_yaml_frontmatter(text):
    """Remove YAML frontmatter (between --- markers) and return (frontmatter, body)."""
    m = re.match(r'^---\s*\n(.*?\n)---\s*\n', text, re.DOTALL)
    if m:
        return m.group(1), text[m.end():]
    return "", text


def extract_yaml_title(frontmatter):
    """Pull title or pagetitle from YAML frontmatter."""
    for key in ("title", "pagetitle"):
        m = re.search(rf'^{key}:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
        if m:
            return m.group(1).strip()
    return None


def strip_html_tags(text):
    """Remove HTML tags but keep the text content."""
    # Remove script blocks entirely
    text = re.sub(r'<script\b[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove style blocks entirely
    text = re.sub(r'<style\b[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove nav blocks entirely
    text = re.sub(r'<nav\b[^>]*>.*?</nav>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove button elements (Continue ->, Mark as Complete, etc.)
    text = re.sub(r'<button\b[^>]*>.*?</button>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove input/textarea elements
    text = re.sub(r'<(?:input|textarea)\b[^>]*(?:>.*?</(?:input|textarea)>|/?>)', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove progress bar divs
    text = re.sub(r'<div\s+id="progress-bar"[^>]*>.*?</div>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove completion UI sections
    text = re.sub(r'<div\s+id="completion-(?:section|trigger)"[^>]*>.*?</div>\s*</div>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # Convert <br> to newlines
    text = re.sub(r'<br\s*/?\s*>', '\n', text, flags=re.IGNORECASE)
    # Convert </p>, </div>, </li>, </h*> to newlines for spacing
    text = re.sub(r'</(?:p|div|li|h[1-6]|tr|td|th)>', '\n', text, flags=re.IGNORECASE)
    # Convert <li> to bullet points
    text = re.sub(r'<li\b[^>]*>', '- ', text, flags=re.IGNORECASE)
    # Convert heading tags to markdown headings
    text = re.sub(r'<h1\b[^>]*>', '\n# ', text, flags=re.IGNORECASE)
    text = re.sub(r'<h2\b[^>]*>', '\n## ', text, flags=re.IGNORECASE)
    text = re.sub(r'<h3\b[^>]*>', '\n### ', text, flags=re.IGNORECASE)
    # Convert <strong>/<b> to markdown bold
    text = re.sub(r'<strong\b[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<b\b[^>]*>(.*?)</b>', r'**\1**', text, flags=re.DOTALL | re.IGNORECASE)
    # Convert <em>/<i> to markdown italic
    text = re.sub(r'<em\b[^>]*>(.*?)</em>', r'*\1*', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<i\b[^>]*>(.*?)</i>', r'*\1*', text, flags=re.DOTALL | re.IGNORECASE)
    # Decode common HTML entities
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('&eacute;', 'e')
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&#9776;', '')  # hamburger menu icon
    text = text.replace('&#8594;', '->')  # right arrow
    text = text.replace('&#9658;', '')  # play/chevron icon
    # Strip all remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text


def clean_whitespace(text):
    """Normalise whitespace: collapse blank lines, strip trailing/leading spaces."""
    # Remove lines that are just standalone decorative emoji (single emoji on a line)
    text = re.sub(r'^\s*[\U0001F300-\U0001FAFF\u2600-\u27BF\u2700-\u27BF]\s*$', '', text, flags=re.MULTILINE)
    # Remove leftover "Continue ->" lines
    text = re.sub(r'^\s*Continue\s*->\s*$', '', text, flags=re.MULTILINE)
    # Remove leftover "Mark as Complete" lines
    text = re.sub(r'^\s*Mark as Complete\s*$', '', text, flags=re.MULTILINE)
    # Remove lines that are just navigation links (Browse Experiences ->, AI Toolkit ->, etc.)
    text = re.sub(r'^\s*(?:Browse Experiences|AI Toolkit|Find Your Path)\s*->\s*$', '', text, flags=re.MULTILINE)
    # Strip leading indentation from each line (HTML nesting artefact)
    lines = [line.strip() for line in text.split('\n')]
    # But preserve markdown code blocks and list indentation
    cleaned_lines = []
    for line in lines:
        # Re-add bullet indent for nested items (lines starting with -)
        cleaned_lines.append(line)
    # Collapse runs of 3+ blank lines to 1
    result = []
    blank_count = 0
    for line in cleaned_lines:
        if line == '':
            blank_count += 1
            if blank_count <= 1:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)
    # Strip leading/trailing blank lines
    text = '\n'.join(result).strip()
    return text + '\n'


def write_doc(subdir, filename, content):
    """Write a document to rag-documents/{subdir}/{filename}."""
    out_dir = OUTPUT_DIR / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    out_path.write_text(content, encoding='utf-8')
    return out_path


# ---------------------------------------------------------------------------
# Extract JS-embedded content from experience files
# ---------------------------------------------------------------------------

def extract_js_answers(text):
    """Extract answer explanations from JS objects like:
       const answers = { 1: { correct: 'ai', explanation: '...' }, ... };
    """
    results = {}
    # Match the whole answers object
    m = re.search(r'(?:const|var)\s+answers\s*=\s*\{(.*?)\};', text, re.DOTALL)
    if m:
        body = m.group(1)
        # Find each entry
        for entry in re.finditer(
            r'(\d+)\s*:\s*\{\s*correct\s*:\s*[\'"](\w+)[\'"]\s*,\s*explanation\s*:\s*[\'"](.+?)[\'"]\s*\}',
            body, re.DOTALL
        ):
            num = int(entry.group(1))
            correct = entry.group(2)
            explanation = entry.group(3).replace("\\'", "'").replace('\\"', '"')
            results[num] = {"correct": correct, "explanation": explanation}
    return results


def extract_js_reflections(text):
    """Extract scenario reflections from JS objects like:
       var reflections = { 1: { a: "...", b: "...", ... }, ... };
    """
    results = {}
    m = re.search(r'(?:const|var)\s+reflections\s*=\s*\{(.*?)\n\s*\};', text, re.DOTALL)
    if m:
        body = m.group(1)
        # Find each scenario
        for scenario_m in re.finditer(r'(\d+)\s*:\s*\{([^}]+)\}', body):
            num = int(scenario_m.group(1))
            entries = {}
            for choice_m in re.finditer(r'(\w)\s*:\s*"(.*?)"', scenario_m.group(2)):
                entries[choice_m.group(1)] = choice_m.group(2).replace('\\"', '"')
            results[num] = entries
    return results


# ---------------------------------------------------------------------------
# Experience extraction
# ---------------------------------------------------------------------------

EXPERIENCE_META = {
    "is-this-ai": {
        "title": "Is This AI?",
        "subtitle": "Detection & Awareness",
        "experience_num": 1,
        "time": "15-60 minutes",
        "audience": "All roles",
    },
    "what-would-you-do": {
        "title": "What Would You Do?",
        "subtitle": "Ethics & Dilemmas",
        "experience_num": 2,
        "time": "20-90 minutes",
        "audience": "All roles",
    },
    "rules-of-engagement": {
        "title": "Rules of Engagement",
        "subtitle": "Policy & Governance",
        "experience_num": 3,
        "time": "30-120 minutes",
        "audience": "All roles",
    },
    "ai-proof-assessments": {
        "title": "AI-Proof Your Assessments",
        "subtitle": "Assessment Design",
        "experience_num": 4,
        "time": "45-75 minutes",
        "audience": "Teaching-focused",
    },
    "teaching-with-ai": {
        "title": "Working with AI",
        "subtitle": "Co-Creation & Integration",
        "experience_num": 5,
        "time": "30-60 minutes",
        "audience": "All roles",
    },
    "working-with-copilot": {
        "title": "Working with Copilot",
        "subtitle": "Microsoft 365 Copilot",
        "experience_num": 6,
        "time": "30-60 minutes",
        "audience": "All roles",
    },
    "the-conversation-loop": {
        "title": "The Conversation Loop",
        "subtitle": "Thinking with AI",
        "experience_num": 6,
        "time": "30-60 minutes",
        "audience": "All roles",
    },
    "researching-with-ai": {
        "title": "Researching with AI",
        "subtitle": "Research & AI Tools",
        "experience_num": 8,
        "time": "30-60 minutes",
        "audience": "All roles",
    },
    "streamlining-your-workflows": {
        "title": "Streamlining Your Workflows",
        "subtitle": "AI for Professional Staff",
        "experience_num": 9,
        "time": "30-60 minutes",
        "audience": "Professional staff",
    },
}


def split_experience_steps(html_content):
    """Split experience HTML into steps using <!-- ===== STEP N: Title ===== --> markers."""
    # Find all step markers
    pattern = r'<!--\s*=+\s*STEP\s+(\d+)\s*:\s*(.*?)\s*=+\s*-->'
    markers = list(re.finditer(pattern, html_content))

    if not markers:
        return [("Full Content", html_content)]

    steps = []
    for i, marker in enumerate(markers):
        step_num = int(marker.group(1))
        step_title = marker.group(2).strip()
        start = marker.start()
        end = markers[i + 1].start() if i + 1 < len(markers) else len(html_content)
        step_html = html_content[start:end]
        steps.append((step_num, step_title, step_html))

    return steps


def extract_experience(exp_dir):
    """Extract content from a single experience directory."""
    qmd_path = exp_dir / "index.qmd"
    if not qmd_path.exists():
        return []

    exp_id = exp_dir.name
    meta = EXPERIENCE_META.get(exp_id, {
        "title": exp_id.replace("-", " ").title(),
        "subtitle": "",
        "experience_num": "?",
        "time": "varies",
        "audience": "All roles",
    })

    raw = qmd_path.read_text(encoding='utf-8')
    _, body = strip_yaml_frontmatter(raw)

    # Remove Quarto raw-html fences
    body = body.replace('```{=html}', '').replace('```', '')

    # Extract JS-embedded content before stripping scripts
    answers = extract_js_answers(body)
    reflections = extract_js_reflections(body)

    # Split into steps
    steps = split_experience_steps(body)

    documents = []

    for step_num, step_title, step_html in steps:
        # Skip welcome/intro steps that are mostly just "how this works" boilerplate
        # and completion steps that are just UI
        title_lower = step_title.lower()
        if title_lower in ("welcome",):
            # Still extract welcome — it has learning objectives
            pass

        # Strip HTML to text
        text = strip_html_tags(step_html)
        text = clean_whitespace(text)

        # Skip if very little content after stripping
        # (e.g. completion section is mostly buttons)
        meaningful_text = re.sub(r'\s+', ' ', text).strip()
        if len(meaningful_text) < 80:
            continue

        # Build the document
        source_label = f"Experience {meta['experience_num']}: {meta['title']} ({meta['subtitle']})"
        preamble = PREAMBLE_TEMPLATE.format(source=source_label)

        doc_title = f"# {meta['title']} — {step_title}\n\n"
        doc_meta = (
            f"*Experience {meta['experience_num']} | {meta['subtitle']} | "
            f"{meta['time']} | {meta['audience']}*\n\n---\n\n"
        )

        content = preamble + doc_title + doc_meta + text

        # Append any JS answer explanations relevant to this step
        if answers and "detection game" in step_title.lower():
            content += "\n\n## Answer Explanations\n\n"
            for num in sorted(answers.keys()):
                a = answers[num]
                content += (
                    f"**Sample {num}:** {a['correct'].upper()} — {a['explanation']}\n\n"
                )

        # Append reflections for scenario steps
        if reflections and ("scenario" in step_title.lower() or "dilemma" in step_title.lower()):
            content += "\n\n## Reflection Notes\n\n"
            content += (
                "Each scenario has multiple valid perspectives. "
                "Here are considerations for each choice:\n\n"
            )
            for scenario_num in sorted(reflections.keys()):
                r = reflections[scenario_num]
                content += f"**Scenario {scenario_num}:**\n"
                for choice, reflection in sorted(r.items()):
                    content += f"- Option {choice.upper()}: {reflection}\n"
                content += "\n"

        content = clean_whitespace(content)

        # Generate filename
        safe_title = re.sub(r'[^a-z0-9]+', '-', step_title.lower()).strip('-')
        filename = f"{exp_id}--{safe_title}.md"

        documents.append((filename, content))

    return documents


# ---------------------------------------------------------------------------
# Toolkit extraction
# ---------------------------------------------------------------------------

def extract_toolkit_file(filepath):
    """Extract a single toolkit .qmd or .md file to clean markdown."""
    raw = filepath.read_text(encoding='utf-8')
    frontmatter, body = strip_yaml_frontmatter(raw)
    title = extract_yaml_title(frontmatter) or filepath.stem.replace('-', ' ').title()

    # Remove Quarto raw-html fences if present
    body = body.replace('```{=html}', '').replace('```', '')

    # If body is mostly HTML (experience-style), strip tags
    html_tag_ratio = len(re.findall(r'<[^>]+>', body)) / max(len(body.split('\n')), 1)
    if html_tag_ratio > 0.3:
        body = strip_html_tags(body)

    preamble = PREAMBLE_TEMPLATE.format(source=f"the AI Toolkit resource: {title}")

    # Add title as H1 if not already present
    if not body.lstrip().startswith('# '):
        body = f"# {title}\n\n{body}"

    content = preamble + body
    content = clean_whitespace(content)

    filename = filepath.stem + ".md"
    return filename, content


# ---------------------------------------------------------------------------
# Navigation pages extraction
# ---------------------------------------------------------------------------

def extract_key_takeaways():
    """Extract key takeaways page content."""
    filepath = PROJECT_ROOT / "key-takeaways" / "index.qmd"
    if not filepath.exists():
        return None

    raw = filepath.read_text(encoding='utf-8')
    _, body = strip_yaml_frontmatter(raw)
    body = body.replace('```{=html}', '').replace('```', '')

    text = strip_html_tags(body)
    # Clean whitespace first so regexes can match flush-left lines
    text = clean_whitespace(text)

    # Remove duplicate header lines from the HTML header section
    text = re.sub(r'^\s*AI Skills Passport\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*#*\s*KEY TAKEAWAYS\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*The big ideas.*?Eight principles worth knowing\.?\s*$', '', text, flags=re.MULTILINE)
    # Remove footer branding
    text = re.sub(r'^\s*AI Skills Passport\s.*Curtin University.*$', '', text, flags=re.MULTILINE)
    # Remove "Go deeper: ..." navigation links
    text = re.sub(r'^\s*Go deeper:.*$', '', text, flags=re.MULTILINE)
    # Remove "Want to explore further?" section and footer nav
    text = re.sub(r'^\s*#{0,3}\s*Want to explore further\?\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*These ideas come alive.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*Browse Experiences.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*AI Toolkit.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*Find Your Path.*$', '', text, flags=re.MULTILINE)

    text = clean_whitespace(text)

    preamble = PREAMBLE_TEMPLATE.format(source="the Key Takeaways page")

    content = preamble + "# Key Takeaways\n\n"
    content += (
        "*The big ideas from the AI Skills Passport. "
        "Eight principles worth knowing, even if you do nothing else.*\n\n---\n\n"
    )
    content += text
    content = clean_whitespace(content)

    return "key-takeaways.md", content


def extract_onboarding():
    """Extract onboarding quiz content."""
    filepath = PROJECT_ROOT / "onboarding" / "index.qmd"
    if not filepath.exists():
        return None

    raw = filepath.read_text(encoding='utf-8')
    _, body = strip_yaml_frontmatter(raw)
    body = body.replace('```{=html}', '').replace('```', '')

    text = strip_html_tags(body)
    text = clean_whitespace(text)

    preamble = PREAMBLE_TEMPLATE.format(source="the Find Your Path onboarding quiz")

    content = preamble + "# Find Your Path\n\n"
    content += (
        "*An onboarding quiz that helps staff discover their recommended starting point "
        "in the AI Skills Passport based on their role and experience.*\n\n---\n\n"
    )
    content += text
    content = clean_whitespace(content)

    return "find-your-path.md", content


def create_overview_doc():
    """Create an overview document describing the AI Skills Passport structure."""
    content = PREAMBLE_TEMPLATE.format(source="the AI Skills Passport overview")
    content += """# How the AI Skills Passport Works

*A professional development initiative for the School of Marketing and Management (SoMM), Curtin University, building AI literacy across teaching academics, researchers, and administrative staff.*

---

## What Is It?

The AI Skills Passport is a self-paced program that helps staff build practical AI skills. It is not a course with grades — it is a set of experiences you work through at your own pace.

## Nine Experiences

There are nine learning experiences across two categories. You can start anywhere — there are no prerequisites.

### Core Experiences — For Everyone

1. **Is This AI?** (Detection & Awareness, 15-60 min) — Test your ability to tell the difference between human and AI-generated content. Explore why detection tools are unreliable and develop practical strategies.

2. **What Would You Do?** (Ethics & Dilemmas, 20-90 min) — Navigate real-world AI dilemmas with no easy answers. Build a personal ethical framework using Transparency, Understanding, and Purpose.

3. **Rules of Engagement** (Policy & Governance, 30-120 min) — Explore real university AI policies, stress-test them with scenarios, and draft a policy statement for your own context.

4. **Working with AI** (Co-Creation & Integration, 30-60 min) — Learn the RTCF framework (Role, Task, Context, Format), experiment in the Prompt Lab, explore techniques, and build a personal prompt library.

5. **The Conversation Loop** (Thinking with AI, 30-60 min) — Learn the Brainstorm, Ideate, Iterate, Amplify loop for working with AI as a thinking partner. Covers the three cognitive traps and why unchecked AI chains are dangerous.

6. **Working with Copilot** (Microsoft 365 Copilot, 30-60 min) — Practical setup and usage of Copilot in Outlook, Word, Excel, PowerPoint, and Teams.

### For Your Role

7. **AI-Proof Your Assessments** (Assessment Design, 45-75 min, teaching-focused) — Stress-test your assessments against AI, explore redesign pathways, and redesign an assessment.

8. **Researching with AI** (Research & AI Tools, 30-60 min) — AI tools for literature discovery, writing, data analysis, and research integrity.

9. **Streamlining Your Workflows** (AI for Professional Staff, 30-60 min) — Identify bottlenecks in your daily work, build reusable prompt templates, and create a personal AI efficiency playbook.

## Other Ways to Engage

- **Key Takeaways** — Ten principles worth knowing, even if you skip the experiences (8 universal, 2 for teaching)
- **AI Toolkit** — A searchable library of 40+ downloadable frameworks, techniques, templates, and guides
- **Find Your Path** — A quiz that recommends where to start based on your role and experience
- **AI in 5** — Weekly 5-minute micro-challenges delivered by email
- **My Passport** — Track your progress and earn badges (Explorer, Thinker, Builder)
- **The Concierge** — An AI chatbot available on every page (click the + icon bottom right) that can answer questions about the Passport content

## Pacing Options

- **Self-paced:** Work through experiences from the Arrivals Hall at your own speed
- **AI in 5:** Weekly 5-minute micro-challenges via email
- **Weekly:** One experience per week
- **Workshop:** 2-hour face-to-face session with a facilitator

## Badges

Complete experiences to earn badges:
- 🧪 **Explorer** — Complete 1 experience
- 🧠 **Thinker** — Complete 3 experiences
- 🛠️ **Builder** — Complete 5 experiences

## Who Is It For?

Everyone in SoMM — teaching academics, researchers, and professional/administrative staff. Each experience has role-specific content with tabs for Teaching, Research, and Admin perspectives.
"""
    return "how-the-passport-works.md", clean_whitespace(content)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Clean output directory
    if OUTPUT_DIR.exists():
        import shutil
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    file_count = 0

    # --- 1. Toolkit resources ---
    print("Extracting toolkit resources...")
    toolkit_dir = PROJECT_ROOT / "ai-toolkit" / "downloads"
    refs_file = None

    for filepath in sorted(toolkit_dir.glob("*.qmd")):
        filename, content = extract_toolkit_file(filepath)
        if "references-collated" in filepath.stem:
            refs_file = (filename, content)
            continue
        write_doc("toolkit", filename, content)
        file_count += 1
        print(f"  toolkit/{filename}")

    # Also grab the .md file
    for filepath in sorted(toolkit_dir.glob("*.md")):
        filename, content = extract_toolkit_file(filepath)
        write_doc("toolkit", filename, content)
        file_count += 1
        print(f"  toolkit/{filename}")

    # --- 2. Experiences ---
    print("\nExtracting experiences...")
    exp_base = PROJECT_ROOT / "experiences"
    for exp_dir in sorted(exp_base.iterdir()):
        if not exp_dir.is_dir():
            continue
        docs = extract_experience(exp_dir)
        for filename, content in docs:
            write_doc("experiences", filename, content)
            file_count += 1
            print(f"  experiences/{filename}")

    # --- 3. Navigation pages ---
    print("\nExtracting navigation pages...")

    result = extract_key_takeaways()
    if result:
        filename, content = result
        write_doc("navigation", filename, content)
        file_count += 1
        print(f"  navigation/{filename}")

    result = extract_onboarding()
    if result:
        filename, content = result
        write_doc("navigation", filename, content)
        file_count += 1
        print(f"  navigation/{filename}")

    filename, content = create_overview_doc()
    write_doc("navigation", filename, content)
    file_count += 1
    print(f"  navigation/{filename}")

    # --- 4. References ---
    print("\nExtracting references...")
    if refs_file:
        filename, content = refs_file
        write_doc("references", filename, content)
        file_count += 1
        print(f"  references/{filename}")

    # --- Summary ---
    print(f"\nDone! Extracted {file_count} documents to {OUTPUT_DIR}/")
    print("\nStructure:")
    for subdir in sorted(OUTPUT_DIR.iterdir()):
        if subdir.is_dir():
            count = len(list(subdir.glob("*.md")))
            print(f"  {subdir.name}/ ({count} files)")


if __name__ == "__main__":
    main()

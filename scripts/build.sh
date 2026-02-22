#!/bin/bash
# build.sh — Render all Quarto projects and package for deployment
# Run from the repo root: bash scripts/build.sh

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"
ZIP_NAME="ai-skills-passport.zip"

echo "Building AI Skills Passport..."
echo ""

# Clean previous build
rm -rf "$DIST"
mkdir -p "$DIST/blackboard" "$DIST/experiences"

# --- Render Quarto projects ---

QUARTO_DIRS=(
  onboarding
  ai-toolkit
  resources
  more
  passport
  key-takeaways
  arrivals-hall
  contact
  about
  ai-in-5-archive
  experiences
  experiences/is-this-ai
  experiences/what-would-you-do
  experiences/rules-of-engagement
  experiences/ai-proof-assessments
  experiences/teaching-with-ai
  experiences/working-with-copilot
  experiences/researching-with-ai
)

for dir in "${QUARTO_DIRS[@]}"; do
  echo "Rendering $dir ..."
  (cd "$ROOT/$dir" && quarto render)
done

echo ""

# --- Collect outputs ---

# Find the rendered index.html in a Quarto project (_output or _site)
find_output() {
  for candidate in "$1/_output/index.html" "$1/_site/index.html"; do
    if [ -f "$candidate" ]; then
      echo "$candidate"
      return
    fi
  done
  echo "ERROR: No rendered output found in $1" >&2
  return 1
}

# Top-level SPAs
for name in onboarding passport key-takeaways arrivals-hall contact about ai-in-5-archive resources more; do
  src="$(find_output "$ROOT/$name")"
  cp "$src" "$DIST/$name.html"
  echo "  Collected $name.html"
done

# AI Toolkit (SPA + downloads folder — keeps relative links intact)
cp "$ROOT/ai-toolkit/_output/index.html" "$DIST/ai-toolkit.html"
if [ -d "$ROOT/ai-toolkit/_output/downloads" ]; then
  mkdir -p "$DIST/downloads"
  cp "$ROOT/ai-toolkit/_output/downloads/"* "$DIST/downloads/"
  echo "  Collected ai-toolkit.html + downloads/ ($(ls "$DIST/downloads/" | wc -l | tr -d ' ') files)"
else
  echo "  Collected ai-toolkit.html"
fi

# Experience SPAs
for exp_name in is-this-ai what-would-you-do rules-of-engagement ai-proof-assessments teaching-with-ai working-with-copilot researching-with-ai; do
  src="$(find_output "$ROOT/experiences/$exp_name")"
  cp "$src" "$DIST/experiences/$exp_name.html"
  echo "  Collected experiences/$exp_name.html"
done

# Experiences index
cp "$ROOT/experiences/_output/index.html" "$DIST/experiences.html"
echo "  Collected experiences.html"

# Blackboard HTML (static, no render needed)
cp "$ROOT/blackboard/arrivals-hall.html" "$DIST/blackboard/"
cp "$ROOT/blackboard/ai-in-5.html" "$DIST/blackboard/"
echo "  Collected blackboard/arrivals-hall.html, blackboard/ai-in-5.html"

echo ""

# --- Create zip ---

(cd "$ROOT" && rm -f "$ZIP_NAME" && cd dist && zip -r "$ROOT/$ZIP_NAME" .)

echo ""
echo "Build complete:"
echo "  dist/              — all rendered files"
echo "  $ZIP_NAME  — ready to upload"
echo ""
echo "Contents:"
(cd "$DIST" && find . -type f | sort | sed 's|^./|  |')

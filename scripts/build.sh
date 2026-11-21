#!/bin/bash
# Build the public AI Skills Passport into dist/.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$ROOT/dist"

echo "Building The AI Skills Passport..."
rm -rf "$DIST"
mkdir -p "$DIST/experiences"

QUARTO_DIRS=(
  onboarding
  ai-toolkit
  passport
  key-takeaways
  arrivals-hall
  contact
  about
  more
  experiences
  experiences/is-this-ai
  experiences/what-would-you-do
  experiences/rules-of-engagement
  experiences/ai-proof-assessments
  experiences/teaching-with-ai
  experiences/the-conversation-loop
  experiences/working-with-copilot
  experiences/researching-with-ai
  experiences/streamlining-your-workflows
)

for dir in "${QUARTO_DIRS[@]}"; do
  echo "Rendering $dir ..."
  (cd "$ROOT/$dir" && quarto render)
done

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

for name in onboarding passport key-takeaways arrivals-hall contact about more; do
  cp "$(find_output "$ROOT/$name")" "$DIST/$name.html"
  echo "  Collected $name.html"
done

cp "$ROOT/ai-toolkit/_output/index.html" "$DIST/ai-toolkit.html"
if [ -d "$ROOT/ai-toolkit/_output/downloads" ]; then
  cp -R "$ROOT/ai-toolkit/_output/downloads" "$DIST/downloads"
fi
echo "  Collected ai-toolkit.html"

cp "$ROOT/experiences/_output/index.html" "$DIST/experiences.html"
for exp_name in is-this-ai what-would-you-do rules-of-engagement ai-proof-assessments teaching-with-ai the-conversation-loop working-with-copilot researching-with-ai streamlining-your-workflows; do
  cp "$(find_output "$ROOT/experiences/$exp_name")" "$DIST/experiences/$exp_name.html"
  echo "  Collected experiences/$exp_name.html"
done

cat > "$DIST/index.html" <<'HTML'
<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<title>The AI Skills Passport</title>
<meta http-equiv="refresh" content="0; url=arrivals-hall.html">
<link rel="canonical" href="arrivals-hall.html">
</head>
<body>
<p><a href="arrivals-hall.html">Enter the Arrivals Hall</a></p>
</body>
</html>
HTML

cp "$ROOT/.nojekyll" "$DIST/.nojekyll" 2>/dev/null || true

# Experience SPAs live one directory down; resolve their root-relative links.
python3 - <<'PYBASE'
from pathlib import Path
for p in Path('dist/experiences').glob('*.html'):
    data = p.read_bytes()
    if b'<base ' not in data:
        data = data.replace(b'<head>', b'<head>\n<base href="../">', 1)
        p.write_bytes(data)
PYBASE

# Downloads are rendered standalone; make their cross-links point at HTML.
python3 - <<'PYDL'
import re
from pathlib import Path
for p in Path('dist/downloads').glob('*.html'):
    data = p.read_bytes()
    data = re.sub(rb'href="([^"]+)\.qmd"', rb'href="\1.html"', data)
    p.write_bytes(data)
PYDL

find "$DIST" -name '._*' -delete
find "$DIST" -name '.DS_Store' -delete

echo ""
echo "Built $DIST"

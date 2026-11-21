# The AI Skills Passport

An open, self-paced AI literacy programme for teaching, research and professional staff. No prerequisites and no fixed order: start wherever it is useful.

This is the public edition. It is the same learning design as the institutional original, with institutional branding, internal links, policy references and the hosted chatbot removed. The tools and frameworks are generic and can be used by any institution.

## Structure

```
arrivals-hall/       Hub page
experiences/         Nine standalone learning experiences
ai-toolkit/          Searchable toolkit + downloadable guides
onboarding/          Find Your Path quiz
passport/            Badge and progress display
key-takeaways/       Summary page
contact/             Contact page
about/               About the programme
more/                Links to the rest
shared/              CSS and shared assets
scripts/build.sh     Render everything into dist/
```

## Build

Requires Quarto 1.6 or newer. PDF downloads also require TinyTeX.

```bash
bash scripts/build.sh
python3 -m http.server -d dist 8000
# open http://localhost:8000
```

The build renders each Quarto project, collects the SPAs into `dist/`, copies the toolkit downloads, and adds a root redirect to the Arrivals Hall.

## Sanitising

`scripts/sanitise.py` is the one-pass clean-up used for the public edition. It replaces institutional names, removes internal navigation and the hosted chatbot, drops internal-only toolkit documents, and renames the institutional engagement guide.

Run it only on a copy, never on the private historical repository. Review the diff before committing.

## Deploy

GitHub Pages builds from GitHub Actions. The workflow installs Quarto and TinyTeX, runs `scripts/build.sh`, and deploys `dist/`.

Deployed at https://michael-borck.github.io/the-ai-skills-passport/. To use `passport.borck.education`, add a DNS `CNAME` for `passport` to `michael-borck.github.io`, add a `CNAME` file containing the domain, and set it in Pages settings.

## What was removed

- Institutional names, school names and policy references
- Internal LMS links and URL variables
- The Briefing archive and AI in 5 email content
- Internal documentation, the RAG corpus, and the progress-tracker server
- The hosted chatbot embed
- Institution-specific toolkit documents

## Licence

Code and layout: MIT. Prose: CC BY 4.0 unless a page says otherwise. Third-party adaptations keep their original licences, noted on the page.

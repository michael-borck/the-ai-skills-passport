# Prompt: Set Up a RAG Chatbot with AnythingLLM

Use this prompt in any project to create an embedded RAG chatbot powered by AnythingLLM. Copy it into a new Claude Code session and it will examine your project structure and adapt automatically.

---

## The Prompt

```
I need you to create a RAG pipeline for AnythingLLM for this project. Please examine this project's directory structure first, then adapt the scripts to match whatever content structure exists here.

This involves three Python scripts in a `scripts/` directory. Use `requests` library for API calls. Use `pathlib` for file operations. Add `rag-documents/` to `.gitignore`.

## Script 1: `scripts/extract_rag_documents.py`

Extract all user/student-facing content from this project into clean markdown files in a `rag-documents/` directory. The script should:

- Walk the project's content directories and identify all content files (.md, .qmd, .html, .rst, .txt, etc.)
- Skip staff-only files (anything with "staff", "marking-guide", "answer-guide", "template" in the path)
- Strip and clean content:
  - YAML frontmatter (but extract title from it)
  - Quarto syntax (`:::{.callout}`, `{{< meta ... >}}`, raw-html fences)
  - HTML tags, script blocks, style blocks, navigation elements
  - UI-only elements (buttons, progress bars, form inputs, completion triggers)
  - HTML entities (decode to plain text)
  - Convert HTML formatting to markdown (headings, bold, italic, lists)
- Add a source preamble to each file: `> This content is from {source}, part of {PROJECT_NAME} at Curtin University.`
- Ensure each file has an H1 title
- Normalise whitespace (collapse multiple blank lines, strip trailing spaces)
- Organise output into subdirectories by content type (e.g. modules/, assessments/, course-info/, toolkit/, etc.)
- Be idempotent (clean and recreate output directory each run)
- Print a summary of what was extracted

Derive the project name, unit code, module names, and assessment names from this specific project's files.

## Script 2: `scripts/upload_to_anythingllm.py`

Upload the extracted documents to AnythingLLM and embed them in a workspace. The script should:

- Read the API key from `ANYTHINGLLM_API_KEY` environment variable (or `--api-key` flag)
- Accept `--base-url` (default: https://chat.eduserver.au), `--workspace` (slug), `--create-workspace`, and `--dry-run` flags
- Look for an existing workspace matching the project/unit, or create one if `--create-workspace` is passed
- When creating/updating a workspace, configure:
  - chatProvider: "anthropic"
  - chatModel: "claude-haiku-4-5-20251001"
  - openAiTemp: 0.5
  - A system prompt scoping the bot to this project's content only
  - A refusal response for off-topic questions
  - similarityThreshold: 0.25, topN: 4
- Upload each markdown file via `POST /api/v1/document/upload` (multipart form, field name: "file")
- Collect the `location` from each upload response
- Embed all documents into the workspace via `POST /api/v1/workspace/{slug}/update-embeddings` with `{"adds": [locations], "deletes": []}`
- Add a 0.2s delay between uploads to avoid overwhelming the server
- Report successes, failures, and provide document paths for manual embedding if the embed step fails

## Script 3: `scripts/add_chatbot_embed.py`

Add the AnythingLLM chat widget to user/student-facing content files. The script should:

- Accept `--embed-id` (required) and `--dry-run` flags
- Target user/student-facing content files (overviews, readings, activities, assessments, etc.)
- Skip files already containing the widget (check for "anythingllm-chat-widget")
- Skip staff/template files
- Append a raw HTML script block that loads the AnythingLLM embed widget using the provided embed ID

## AnythingLLM API Endpoints Reference

- `GET /api/v1/workspaces` — list workspaces
- `GET /api/v1/documents` — list uploaded documents
- `POST /api/v1/document/upload` — upload a file (multipart form, field name: "file")
- `POST /api/v1/workspace/{slug}/update-embeddings` — embed documents (JSON body: `{"adds": [doc_paths], "deletes": []}`)
- `POST /api/v1/workspace/new` — create workspace (JSON body with name, config)
- `POST /api/v1/workspace/{slug}/update` — update workspace settings

All requests use header: `Authorization: Bearer {api_key}`

## Workflow

1. Run `python scripts/extract_rag_documents.py` — collates and cleans all content
2. Run `python scripts/upload_to_anythingllm.py --create-workspace` — uploads to AnythingLLM and embeds
3. Manually in AnythingLLM UI:
   - Set chat mode to "Query" (only answers from documents, won't hallucinate)
   - Enable "Show citations in responses" (Workspace Settings > Chat) so users see source documents
   - Create an embed (Settings > Embed Chat) and copy the embed UUID
4. Run `python scripts/add_chatbot_embed.py --embed-id <UUID>` — adds chatbot widget to all pages

## Usage

```bash
# Step 1: Extract documents
python3 scripts/extract_rag_documents.py

# Step 2: Upload and embed (set your API key first)
export ANYTHINGLLM_API_KEY="your-key-here"
python3 scripts/upload_to_anythingllm.py --create-workspace

# Or dry run first to preview
python3 scripts/upload_to_anythingllm.py --dry-run

# Step 3: After creating embed in AnythingLLM UI
python3 scripts/add_chatbot_embed.py --embed-id "your-embed-uuid"
python3 scripts/add_chatbot_embed.py --embed-id "your-embed-uuid" --dry-run  # preview first
```
```

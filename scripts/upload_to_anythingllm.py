#!/usr/bin/env python3
"""
Upload RAG documents to AnythingLLM and embed them in a workspace.

Usage:
    export ANYTHINGLLM_API_KEY="your-api-key"
    python3 scripts/upload_to_anythingllm.py

Or pass the key directly:
    python3 scripts/upload_to_anythingllm.py --api-key "your-api-key"

Options:
    --base-url    AnythingLLM instance URL (default: http://chat.eduserver.au)
    --workspace   Workspace slug (auto-detected if only one exists)
    --api-key     API key (or set ANYTHINGLLM_API_KEY env var)
    --dry-run     Show what would be uploaded without doing it
"""

import argparse
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' library required. Install with: pip install requests")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAG_DIR = PROJECT_ROOT / "rag-documents"

DEFAULT_BASE_URL = "https://chat.eduserver.au"

# Folder names in AnythingLLM for each document category
FOLDER_MAP = {
    "toolkit": "toolkit",
    "experiences": "experiences",
    "navigation": "navigation",
    "references": "references",
}


def get_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
    }


def list_workspaces(base_url, api_key):
    """List all workspaces."""
    r = requests.get(f"{base_url}/api/v1/workspaces", headers=get_headers(api_key))
    r.raise_for_status()
    return r.json().get("workspaces", [])


def list_documents(base_url, api_key):
    """List all uploaded documents."""
    r = requests.get(f"{base_url}/api/v1/documents", headers=get_headers(api_key))
    r.raise_for_status()
    return r.json()


def upload_file(base_url, api_key, filepath):
    """Upload a single file to AnythingLLM."""
    url = f"{base_url}/api/v1/document/upload"
    h = {"Authorization": f"Bearer {api_key}"}
    with open(filepath, "rb") as f:
        r = requests.post(url, headers=h, files={"file": f})
    if r.status_code != 200:
        raise Exception(f"HTTP {r.status_code}: {r.text[:200]}")
    try:
        return r.json()
    except Exception:
        raise Exception(f"Non-JSON response: {r.text[:200]}")


def get_workspace_documents(base_url, api_key, workspace_slug):
    """Get list of document paths currently embedded in a workspace."""
    r = requests.get(
        f"{base_url}/api/v1/workspace/{workspace_slug}",
        headers=get_headers(api_key),
    )
    r.raise_for_status()
    data = r.json().get("workspace", {})
    # API may return workspace as a list (with one element) or a dict
    if isinstance(data, list):
        workspace = data[0] if data else {}
    else:
        workspace = data
    documents = workspace.get("documents", [])
    return [doc.get("docpath") for doc in documents if doc.get("docpath")]


def update_embeddings(base_url, api_key, workspace_slug, add_paths, delete_paths=None):
    """Add and/or remove documents from a workspace (update embeddings)."""
    url = f"{base_url}/api/v1/workspace/{workspace_slug}/update-embeddings"
    payload = {"adds": add_paths, "deletes": delete_paths or []}
    r = requests.post(url, headers=get_headers(api_key), json=payload)
    r.raise_for_status()
    return r.json()


def main():
    parser = argparse.ArgumentParser(description="Upload RAG documents to AnythingLLM")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="AnythingLLM URL")
    parser.add_argument("--workspace", default=None, help="Workspace slug")
    parser.add_argument("--api-key", default=None, help="API key")
    parser.add_argument("--dry-run", action="store_true", help="Preview without uploading")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ANYTHINGLLM_API_KEY")
    if not api_key:
        print("Error: Provide API key via --api-key or ANYTHINGLLM_API_KEY env var")
        sys.exit(1)

    base_url = args.base_url.rstrip("/")

    if not RAG_DIR.exists():
        print(f"Error: {RAG_DIR} not found. Run extract_rag_documents.py first.")
        sys.exit(1)

    # --- Discover workspace ---
    print(f"Connecting to {base_url}...")
    workspaces = list_workspaces(base_url, api_key)
    if not workspaces:
        print("Error: No workspaces found. Create one in AnythingLLM first.")
        sys.exit(1)

    if args.workspace:
        workspace_slug = args.workspace
    elif len(workspaces) == 1:
        workspace_slug = workspaces[0]["slug"]
    else:
        print("Multiple workspaces found:")
        for w in workspaces:
            print(f"  - {w['name']} (slug: {w['slug']})")
        print("Use --workspace <slug> to specify which one.")
        sys.exit(1)

    print(f"Target workspace: {workspace_slug}")

    # --- Collect files to upload ---
    files_to_upload = []
    for subdir in sorted(RAG_DIR.iterdir()):
        if not subdir.is_dir():
            continue
        folder_name = FOLDER_MAP.get(subdir.name, subdir.name)
        for md_file in sorted(subdir.glob("*.md")):
            files_to_upload.append((md_file, folder_name))

    print(f"Found {len(files_to_upload)} documents to upload\n")

    if args.dry_run:
        for filepath, folder in files_to_upload:
            print(f"  [DRY RUN] {folder}/{filepath.name}")
        print(f"\nDry run complete. {len(files_to_upload)} files would be uploaded.")
        return

    # --- Upload files ---
    print("Uploading documents...")
    uploaded_doc_paths = []
    failed = []

    for i, (filepath, folder_name) in enumerate(files_to_upload, 1):
        try:
            result = upload_file(base_url, api_key, filepath)
            # AnythingLLM returns the document location for embedding
            if result.get("success") and result.get("documents"):
                for doc in result["documents"]:
                    doc_location = doc.get("location")
                    if doc_location:
                        uploaded_doc_paths.append(doc_location)
            print(f"  [{i}/{len(files_to_upload)}] {folder_name}/{filepath.name}")
        except Exception as e:
            print(f"  [{i}/{len(files_to_upload)}] FAILED {folder_name}/{filepath.name}: {e}")
            failed.append((filepath, str(e)))
        # Small delay to avoid overwhelming the server
        time.sleep(0.2)

    print(f"\nUploaded: {len(uploaded_doc_paths)}, Failed: {len(failed)}")

    if failed:
        print("\nFailed uploads:")
        for filepath, err in failed:
            print(f"  {filepath.name}: {err}")

    if not uploaded_doc_paths:
        print("No documents uploaded successfully. Skipping embedding.")
        return

    # --- Remove old embeddings, then add new ones ---
    print(f"\nFetching existing workspace documents...")
    try:
        existing_docs = get_workspace_documents(base_url, api_key, workspace_slug)
        if existing_docs:
            print(f"  Found {len(existing_docs)} existing documents — will remove them first")
        else:
            print("  No existing documents (fresh workspace)")
    except Exception as e:
        print(f"  Warning: Could not fetch existing documents ({e}), proceeding with adds only")
        existing_docs = []

    # Step 1: Remove old embeddings in batches
    if existing_docs:
        print(f"Removing {len(existing_docs)} old embeddings...")
        batch_size = 50
        for i in range(0, len(existing_docs), batch_size):
            batch = existing_docs[i:i + batch_size]
            try:
                update_embeddings(base_url, api_key, workspace_slug,
                                  add_paths=[], delete_paths=batch)
                print(f"  Removed batch {i // batch_size + 1} ({len(batch)} docs)")
            except Exception as e:
                print(f"  Warning: batch removal failed ({e}), continuing...")
            time.sleep(0.5)
        print("  Old embeddings removed")

    # Step 2: Add new embeddings in batches
    print(f"Embedding {len(uploaded_doc_paths)} new documents into workspace '{workspace_slug}'...")
    batch_size = 20
    for i in range(0, len(uploaded_doc_paths), batch_size):
        batch = uploaded_doc_paths[i:i + batch_size]
        try:
            update_embeddings(base_url, api_key, workspace_slug,
                              add_paths=batch, delete_paths=[])
            print(f"  Embedded batch {i // batch_size + 1} ({len(batch)} docs)")
        except Exception as e:
            print(f"  Embedding batch failed: {e}")
            print("  Document paths for manual embedding:")
            for p in batch:
                print(f"    {p}")
        time.sleep(0.5)

    print("Embedding complete!")

    print("\nDone!")


if __name__ == "__main__":
    main()

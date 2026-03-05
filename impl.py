#!/usr/bin/env python3
"""
Generate facets from Claude Code session-meta files.
Run this script after accumulating new sessions.
"""
import json
import os
from pathlib import Path
from datetime import datetime

# Paths
CLAUDE_DIR = Path.home() / ".claude"
SESSION_META_DIR = CLAUDE_DIR / "usage-data" / "session-meta"
FACETS_DIR = CLAUDE_DIR / "usage-data" / "facets"

# Ensure facets directory exists
FACETS_DIR.mkdir(parents=True, exist_ok=True)

def get_session_files():
    """Get list of all session-meta files that don't have facets yet."""
    session_files = list(SESSION_META_DIR.glob("*.json"))
    existing_facets = {f.name for f in FACETS_DIR.glob("*.json")}
    return [f for f in session_files if f.name not in existing_facets]

def analyze_session(session_data: dict) -> dict:
    """Analyze session-meta data and generate facet information."""
    session_id = session_data["session_id"]
    duration = session_data.get("duration_minutes", 0)
    user_msg_count = session_data.get("user_message_count", 0)
    assistant_msg_count = session_data.get("assistant_message_count", 0)
    tool_counts = session_data.get("tool_counts", {})
    tool_errors = session_data.get("tool_errors", 0)
    tool_error_categories = session_data.get("tool_error_categories", {})
    languages = session_data.get("languages", {})
    git_commits = session_data.get("git_commits", 0)
    lines_added = session_data.get("lines_added", 0)
    lines_removed = session_data.get("lines_removed", 0)
    files_modified = session_data.get("files_modified", 0)
    first_prompt = session_data.get("first_prompt", "")
    summary = session_data.get("summary", "")
    user_interruptions = session_data.get("user_interruptions", 0)

    # Determine session type and outcome
    if assistant_msg_count == 0 or "exit" in first_prompt.lower() or "clear" in first_prompt.lower():
        return {
            "underlying_goal": "User wanted to exit Claude Code session",
            "goal_categories": {},
            "outcome": "unclear_from_transcript",
            "user_satisfaction_counts": {},
            "claude_helpfulness": "unhelpful",
            "session_type": "session_exit",
            "friction_counts": {},
            "friction_detail": "",
            "primary_success": "none",
            "brief_summary": f"Session exit after {duration} minutes. {user_msg_count} user messages, 0 assistant messages, 0 tools used.",
            "session_id": session_id
        }

    # Extract goal from first_prompt or summary
    underlying_goal = summary[:100] if summary else first_prompt[:100]

    # Determine goal categories based on tools and context
    goal_categories = {}
    if any(k in tool_counts for k in ["Edit", "Write"]):
        goal_categories["development"] = 1
    if tool_errors > 0 or "error" in first_prompt.lower() or "fix" in first_prompt.lower():
        goal_categories["troubleshooting"] = 1
    if "explain" in first_prompt.lower() or "understand" in first_prompt.lower() or "how" in first_prompt.lower():
        goal_categories["explanation"] = 1
    if "refactor" in first_prompt.lower() or "migrate" in first_prompt.lower():
        goal_categories["refactoring"] = 1
    if "task" in first_prompt.lower() or "plan" in first_prompt.lower():
        goal_categories["planning"] = 1

    # Determine outcome
    if user_interruptions > 0:
        outcome = "interrupted"
    elif lines_added > 0 or git_commits > 0 or files_modified > 0:
        outcome = "achieved"
    elif assistant_msg_count > 0:
        outcome = "mostly_achieved"
    else:
        outcome = "unclear_from_transcript"

    # Determine helpfulness
    if tool_errors > 5:
        helpfulness = "barely_helpful"
    elif tool_errors > 0:
        helpfulness = "moderately_helpful"
    elif lines_added > 0 or git_commits > 0:
        helpfulness = "helpful"
    else:
        helpfulness = "unknown"

    # Determine session type
    if "refactor" in first_prompt.lower():
        session_type = "refactoring"
    elif "debug" in first_prompt.lower() or "fix" in first_prompt.lower() or "error" in first_prompt.lower():
        session_type = "debugging"
    elif "learn" in first_prompt.lower() or "explain" in first_prompt.lower():
        session_type = "learning"
    elif "analyze" in first_prompt.lower() or "understand" in first_prompt.lower():
        session_type = "exploration"
    elif "task" in first_prompt.lower():
        session_type = "task_planning"
    elif lines_added > 100:
        session_type = "active_development"
    else:
        session_type = "general"

    # Build friction detail
    friction_detail = ""
    if tool_errors > 0:
        error_types = ", ".join(f"{k}: {v}" for k, v in tool_error_categories.items())
        friction_detail = f"{tool_errors} tool errors: {error_types}"

    # Primary success
    if git_commits > 0:
        primary_success = "committed_changes"
    elif lines_added > 50:
        primary_success = "substantial_code_additions"
    elif lines_added > 0:
        primary_success = "code_modifications"
    elif files_modified > 0:
        primary_success = "file_modifications"
    elif "explain" in first_prompt.lower() or "understand" in first_prompt.lower():
        primary_success = "code_understanding"
    else:
        primary_success = "general_progress"

    # Brief summary
    brief_summary = f"{duration}-minute session"
    if languages:
        brief_summary += f" working with {', '.join(languages.keys())}"
    if lines_added > 0 or lines_removed > 0:
        brief_summary += f". Modified {files_modified} files with {lines_added} additions and {lines_removed} deletions"
    brief_summary += f". {summary[:200] if summary else first_prompt[:200]}"

    return {
        "underlying_goal": underlying_goal[:200],
        "goal_categories": goal_categories,
        "outcome": outcome,
        "user_satisfaction_counts": {"likely_satisfied": 1} if outcome == "achieved" else {},
        "claude_helpfulness": helpfulness,
        "session_type": session_type,
        "friction_counts": tool_error_categories,
        "friction_detail": friction_detail[:300],
        "primary_success": primary_success,
        "brief_summary": brief_summary[:500],
        "session_id": session_id
    }

def main():
    # Get files to process
    to_process = get_session_files()
    total = len(to_process)

    if total == 0:
        print("✅ All session-meta files already have corresponding facets!")
        return

    print(f"📊 Generating {total} facets from session-meta files...")
    print()

    # Process in batches
    batch_size = 10
    for i in range(0, total, batch_size):
        batch = to_process[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total + batch_size - 1) // batch_size

        print(f"Batch {batch_num}/{total_batches}: Processing {len(batch)} files...")

        for session_file in batch:
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)

                facet = analyze_session(session_data)
                facet_file = FACETS_DIR / session_file.name

                with open(facet_file, 'w', encoding='utf-8') as f:
                    json.dump(facet, f, indent=2, ensure_ascii=False)

                print(f"  ✓ {session_file.name}")
            except Exception as e:
                print(f"  ✗ {session_file.name}: {e}")

        print()

    print(f"✅ Complete! {total} facets generated.")
    print(f"📁 Location: {FACETS_DIR}")
    print()
    print("Run `/insights` to see updated report.")

if __name__ == "__main__":
    main()

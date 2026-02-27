"""Helper utilities for the review skill."""


def count_diff_lines(diff_text: str) -> dict[str, int]:
    """Count added and removed lines in a unified diff."""
    added = sum(1 for line in diff_text.splitlines() if line.startswith("+"))
    removed = sum(1 for line in diff_text.splitlines() if line.startswith("-"))
    return {"added": added, "removed": removed}

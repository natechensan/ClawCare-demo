"""Helper for the safe formatting skill."""


def count_issues(ruff_output: str) -> int:
    """Count the number of lint issues found by ruff."""
    return len([line for line in ruff_output.splitlines() if ": " in line])

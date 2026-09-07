#!/usr/bin/env python3
"""Check the skill folder against the Agent Skills spec before it is packaged.

Rules come from the published spec: SKILL.md is the only required file, and its
YAML frontmatter carries the two required fields. `description` is the string
Claude matches a request against, so a broken one silently stops the skill from
ever triggering — worth failing a build over.

Deliberately stdlib-only, and it parses the two fields by hand rather than
importing PyYAML, so it runs anywhere the renderer runs.
"""
import os
import re
import sys

MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_UNCOMPRESSED = 30 * 1024 * 1024
RESERVED = ("anthropic", "claude")


def frontmatter(text):
    """Return the raw frontmatter block, or None if the file has none."""
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    return m.group(1) if m else None


def field(block, key):
    """Read one top-level scalar, folded (>-) or literal (|) block included."""
    m = re.search(rf"^{key}:[ \t]*(.*)$", block, re.M)
    if not m:
        return None
    head = m.group(1).strip()
    if head not in (">", ">-", ">+", "|", "|-", "|+"):
        return head.strip("\"'")
    folded = head.startswith(">")
    lines = []
    for line in block[m.end():].splitlines():
        if line.strip() and not line[:1].isspace():
            break  # next top-level key
        lines.append(line.strip())
    return (" " if folded else "\n").join(l for l in lines if l).strip()


def main(skill_dir):
    errors = []
    path = os.path.join(skill_dir, "SKILL.md")

    if not os.path.isfile(path):
        sys.exit(f"FAIL {path} is missing — a skill is a folder containing SKILL.md")

    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    block = frontmatter(text)
    if block is None:
        sys.exit(f"FAIL {path} has no YAML frontmatter. The name and description "
                 "Claude extracts live there; there is no separate metadata file.")

    name = field(block, "name")
    description = field(block, "description")

    if not name:
        errors.append("`name` is missing from the frontmatter")
    else:
        if len(name) > MAX_NAME:
            errors.append(f"`name` is {len(name)} chars, max {MAX_NAME}")
        if not re.fullmatch(r"[a-z0-9-]+", name):
            errors.append(f"`name` {name!r} must be lowercase letters, numbers and hyphens only")
        for word in RESERVED:
            if word in name.lower():
                errors.append(f"`name` may not contain the reserved word {word!r}")
        folder = os.path.basename(os.path.normpath(skill_dir))
        if name != folder:
            errors.append(f"`name` {name!r} does not match the folder {folder!r}; "
                          "Claude Code derives the command name from the folder")

    if not description:
        errors.append("`description` is missing or empty — Claude cannot match the skill without it")
    else:
        if len(description) > MAX_DESCRIPTION:
            errors.append(f"`description` is {len(description)} chars, max {MAX_DESCRIPTION}")
        if re.search(r"<[^>]+>", description):
            errors.append("`description` may not contain XML tags")

    total = sum(
        os.path.getsize(os.path.join(root, f))
        for root, _, files in os.walk(skill_dir)
        for f in files
    )
    if total > MAX_UNCOMPRESSED:
        errors.append(f"skill is {total / 1e6:.1f} MB uncompressed, max 30 MB")

    if errors:
        for e in errors:
            print(f"FAIL {e}", file=sys.stderr)
        sys.exit(1)

    print(f"OK   name:        {name}")
    print(f"OK   description: {len(description)}/{MAX_DESCRIPTION} chars")
    print(f"OK   size:        {total / 1024:.0f} KB uncompressed")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: validate_skill.py <skill-dir>")
    main(sys.argv[1])

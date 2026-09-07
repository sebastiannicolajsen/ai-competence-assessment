#!/usr/bin/env python3
"""Pull the person's own turns out of exported AI conversations.

Why this exists: a history-search tool only reaches the place it is run from.
On claude.ai a run outside a project cannot see the project's conversations and
a run inside one cannot see anything else, and no run sees another vendor's
tool at all. So the honest way to widen a card is to let the person hand over
material, and this turns that material into something quotable.

It never scores and never summarises. It extracts the person's own messages,
verbatim, so the quote rules in SKILL.md still apply downstream.

    python3 scripts/collect_evidence.py ~/.claude/projects  --surface cc  > evidence.json
    python3 scripts/collect_evidence.py conversations.json  --surface gpt > evidence.json

Standard library only. Formats are auto-detected; --surface only sets the tag
that ends up next to each quote on the card.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys

# Turns that are machinery rather than the person talking. Tools inject plenty
# of these into the user role -- slash-command envelopes, IDE events, hook
# output, task notifications -- and quoting one as evidence of how someone works
# would be exactly the fabrication the card's other safeguards exist to prevent.
# Matching any opening tag beats maintaining a list of them, since prose almost
# never starts with one.
TAG_OPENER = re.compile(r"^<[a-zA-Z][\w-]*[ >]")
NOISE_PREFIXES = (
    "Caveat:", "[Request interrupted", "This session is being continued",
    "API Error", "/clear", "/compact",
)
MIN_CHARS = 15


def clean(text):
    """Keep real prose the person typed; drop machinery and trivial turns."""
    text = (text or "").strip()
    if len(text) < MIN_CHARS:
        return None
    if TAG_OPENER.match(text) or any(text.startswith(p) for p in NOISE_PREFIXES):
        return None
    return text


def iso(ts):
    if not ts:
        return None
    try:
        return dt.datetime.fromtimestamp(float(ts), dt.timezone.utc).date().isoformat()
    except (TypeError, ValueError, OSError):
        return str(ts)[:10] or None


def from_claude_code(path):
    """Claude Code session transcripts: ~/.claude/projects/<slug>/<uuid>.jsonl

    Each line is an event. Tool results arrive with type "user" too, so the
    content blocks are filtered rather than the event type.
    """
    files = sorted(glob.glob(os.path.join(path, "**", "*.jsonl"), recursive=True)) \
        if os.path.isdir(path) else [path]
    for f in files:
        messages, date = [], None
        try:
            handle = open(f, encoding="utf-8")
        except OSError:
            continue
        with handle:
            for line in handle:
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                if ev.get("type") != "user":
                    continue
                date = date or (ev.get("timestamp") or "")[:10] or None
                content = (ev.get("message") or {}).get("content")
                blocks = content if isinstance(content, list) else [
                    {"type": "text", "text": content}]
                for b in blocks:
                    if not isinstance(b, dict) or b.get("type") != "text":
                        continue  # tool_result and friends are not the person talking
                    text = clean(b.get("text"))
                    if text:
                        messages.append(text)
        if messages:
            yield {
                "id": os.path.splitext(os.path.basename(f))[0],
                "title": os.path.basename(os.path.dirname(f)),
                "date": date,
                "url": None,  # local sessions have no shareable address
                "messages": messages,
            }


def from_chatgpt(path):
    """ChatGPT data export: conversations.json from Settings -> Data controls.

    Best effort: the export format is not versioned publicly, so unknown node
    shapes are skipped rather than guessed at.
    """
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        data = data.get("conversations", [])
    for conv in data if isinstance(data, list) else []:
        if not isinstance(conv, dict):
            continue
        nodes = list((conv.get("mapping") or {}).values())
        nodes.sort(key=lambda n: ((n.get("message") or {}).get("create_time") or 0)
                   if isinstance(n, dict) else 0)
        messages = []
        for node in nodes:
            msg = (node or {}).get("message") if isinstance(node, dict) else None
            if not isinstance(msg, dict):
                continue
            if (msg.get("author") or {}).get("role") != "user":
                continue
            content = msg.get("content") or {}
            if content.get("content_type") != "text":
                continue
            text = clean("\n".join(str(p) for p in content.get("parts") or [] if p))
            if text:
                messages.append(text)
        if messages:
            cid = conv.get("conversation_id") or conv.get("id") or ""
            yield {
                "id": cid,
                "title": conv.get("title") or "(untitled)",
                "date": iso(conv.get("create_time")),
                "url": f"https://chatgpt.com/c/{cid}" if cid else None,
                "messages": messages,
            }


def detect(path):
    if os.path.isdir(path):
        return "claude-code" if glob.glob(
            os.path.join(path, "**", "*.jsonl"), recursive=True) else None
    if path.endswith(".jsonl"):
        return "claude-code"
    if path.endswith(".json"):
        return "chatgpt"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="a transcript file, an export file, or a directory of them")
    ap.add_argument("--surface", default=None,
                    help="tag for the quotes (cc, gpt, gemini, copilot, other)")
    ap.add_argument("--limit", type=int, default=40,
                    help="most recent N conversations to keep (default 40)")
    args = ap.parse_args()

    kind = detect(args.path)
    if kind is None:
        sys.exit(f"Can't tell what {args.path!r} is. Point this at a directory of Claude Code "
                 f"transcripts (~/.claude/projects), a .jsonl transcript, or a ChatGPT "
                 f"conversations.json export.")

    reader = from_claude_code if kind == "claude-code" else from_chatgpt
    default_surface = {"claude-code": "cc", "chatgpt": "gpt"}[kind]
    try:
        conversations = list(reader(args.path))
    except (OSError, ValueError) as exc:
        sys.exit(f"Could not read {args.path}: {exc}")

    if not conversations:
        sys.exit(f"Found no messages from the person in {args.path}. Nothing to assess from here.")

    conversations.sort(key=lambda c: c.get("date") or "", reverse=True)
    conversations = conversations[:args.limit]
    dates = sorted(c["date"] for c in conversations if c.get("date"))

    json.dump({
        "surface": args.surface or default_surface,
        "format": kind,
        "source": os.path.abspath(args.path),
        "n_conversations": len(conversations),
        "date_range": [dates[0], dates[-1]] if dates else None,
        "conversations": conversations,
    }, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")

    print(f"{len(conversations)} conversations, "
          f"{sum(len(c['messages']) for c in conversations)} of the person's own messages"
          + (f", {dates[0]} to {dates[-1]}" if dates else ""), file=sys.stderr)


if __name__ == "__main__":
    main()

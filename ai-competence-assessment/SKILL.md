---
name: ai-competence-assessment
description: >-
  Produce a personal AI competence assessment — a single visual card how the person works with AI (assisted → integrated →
  transformative), using quotes and more Built for onboarding new
  starters ("AI fluency check", "assess my AI use", "how good am I at using AI?",
  "hvor god er jeg til at bruge AI?", "lav min AI-profil"), but works for anyone
  reflecting on how they work with AI. Use this whenever someone wants a
  self-assessment, competence profile, fluency check, or a snapshot of their own
  AI use, or "see where I'm at with AI" without naming a format. Output is a standalone HTML card.
---

# AI Competence Assessment

Make one card that answers "how do I work with AI, and what's my next move?". The heavy lifting (the four competencies, the behaviors to look for) is knowledge you already have from the AI-fluency framework; this skill fixes the **framing, the honesty rules, and the visual output**. Keep the framework invisible to the reader.

**Language: English by default.** Pass `"lang": "da"` — labels, stage names, the headline sentences, and the reflection questions all exist in both da and en.

Write the card in the language the person is using. If they've been writing Danish, set
`"lang": "da"` without asking; if they're writing English, leave it. If another language, decide on how best to port. Plain everyday words in all language.

**The card never shows a number.** No score, no x/5, no percentage, no counts. The headline is a
sentence about how the person uses AI. Everything else is words, position, and evidence.

**Order on the card: headline sentence, then the next moves, then the journey and the evidence
underneath.** The moves come first because they are the only part that asks the reader to do
something, and because a less AI-native reader who opens with a marker near the left of a
three-band rail reads a grade before they reach anything useful. Everything below the moves is
the grounding for them. This puts real weight on the moves being specific: a recommendation
that arrives before its evidence has to earn its place in one line.

## Step 1 — Gather evidence, then stop and confirm

- If the person has chat history, use `recent_chats` and `conversation_search` to pull their real
  conversations. **Pull to the cap, not to the first plausible handful: 20 conversations or 30
  days, whichever is larger.** Retrieval depth is currently the biggest source of error in this
  card. Two runs on the same person, same window, once returned 7 conversations and once 20, with
  no overlapping evidence and different conclusions. Under 8 conversations, confidence is `low`
  and the script enforces it. **Keep the `url` attribute of every chat you pull** — you will
  attach it to the quotes so they link back to their origin.
- **Always ask the data question, even with rich history:** *"Do you think about what information
  you put in, for example ID numbers, salary, client data?"* (DA: *"Tænker du over, hvilke
  oplysninger du lægger ind, fx CPR, løn, kundedata?"*) Responsible use is the one thing a chat
  log structurally cannot show, so it is the one thing you have to ask. The answer goes in the
  diligence area's `self_report` and is labelled on the card as the person's own words.
- **New starters usually have little or no history.** Don't force it — run the 6 reflection
  questions in `references/framework.md`. Their answers become the evidence, and the card says so.
- If the user wants to include project specific knowledge, ask them to run the skill in their project.

Then report back before assessing anything:

- how many conversations you found
- the date range they cover
- which surfaces they came from

Then ask: *"Want me to run the assessment on this, or add anything first?"*
(DA: *"Vil du køre vurderingen på det her, eller vil du tilføje noget først?"*)
**Wait for an answer before generating the card.** Do not assess and confirm in the same turn.

## Step 2 — Assess the four areas

Score each area 1–5 using the anchors in `references/framework.md`, and read the scoring posture
section there first. The score is **internal only** — it positions the marker and the bars; it is
never printed.

**Every scored area carries an `anchor` field with the anchor line copied verbatim.** The script
checks it against the table and refuses to render on a mismatch. Then read the anchor next to the
summary you wrote for the same area: if the summary describes a lower anchor than the score, the
summary is usually the honest one. This check exists because real cards rendered *Integrated*
over summaries that described level-2 behaviour, and nothing caught it.

Two area-specific rules:
- **discernment** takes `evidence_kind` (`language` | `substance` | `mixed`). Wording-only
  evidence caps the score at 2, however much of it there is.
- **diligence** is split. Score only the verifying half, from the traces listed in the reference.
  The data half comes from the Step 1 question and goes in `self_report`. Never score this area
  from a general impression, and never count "please double check this" as verification, because
  that hands the check to the thing being checked.

**Assisted is the default; when torn between two anchors, take the lower one.** The overall stage
is gated rather than averaged — transformative needs all four areas observed, no weak area, and
real evidence of verification. The script applies the gates and prints a line naming what held
the person back. Don't try to talk the card upward with a generous `statement` override. Watch the trap the research
is clear on: people get *less* critical when an answer looks polished, so an area can look strong
and still be thin on checking.

If an area has **no evidence at all**, set `"score": null`. It renders as *ikke observeret*.
Never invent a middling score to fill a gap — an honest blank is more useful than a guessed 3.

## Step 3 — Evidence rules (read these every time)

Quotes are the part that can quietly go wrong. Hard rules:

- **Verbatim, from the person's own messages.** Copy exactly. Never paraphrase into quote marks,
  never smooth grammar, never merge two messages into one quote. If you cannot find a real line,
  leave `quotes` empty rather than writing one.
- **Never quote the assistant.** Only the person's own turns are evidence of how *they* work.
- **Under 150 characters.** If the line is longer, truncate at a word boundary and end with `…`.
  Truncation is the only edit allowed.
- **Attach the source.** Each quote takes `url` (the chat URL from the search result) and
  `surface` (`chat`, `cc`, `cowork`, or `refleksion`). Reflection answers given live in the
  session have no URL — that's fine, they render unlinked.
- **Redact before you publish.** If the only good quote contains a client name, a colleague's
  name, or personal data, pick another quote or replace the sensitive part with `[…]`.
- Only the text you actually gathered goes on the card. Do not infer, embellish, or generate
  supporting detail.

## Step 4 — Write the headline sentence

One plain sentence naming *how* the person uses AI, in second person. The script has a default per
stage; override it with `"statement"` when you can be more specific about their actual work.

**Write the statement or the example, not both.** They compete now that the moves sit directly
underneath. A statement written for this person already names the specific behaviour, so an
example after it says the same thing twice before the reader has learned anything new. Use the
`example` line only when you keep the generic stage sentence and need something concrete under it.

If you do write one, give it a `from`: `{"text": "…", "from": "delegation"}`. **It must not come
from the same area as any next move.** The script errors on the overlap, because the example and
the moves both reach for the person's most visible behaviour and will collide unless you stop
them. In a real card the example described asking for a shorter version, and the second move
advised on asking for a shorter version.

The three sentences differ **a lot** in meaning; don't blur them:

- assisteret — AI helps with single tasks, when it occurs to them
- integreret — AI is a fixed part of how several tasks get done
- transformativ — tasks get solved in ways that would not exist without AI

## Step 5 — Write the reason behind the moves

Required at `med` or `high` confidence; optional only at `low`.

`"why"` is one short paragraph saying why the three moves are these three. It is the honest
observation, but it now sits under the moves as their justification rather than standing as its
own titled block. That change is deliberate: a heading reading *Straight talk* performs honesty
instead of doing it, and it was the single most AI-sounding thing on the card.

Name what is actually weak, in plain words, with no compliment wrapped around it. Two to four
sentences. Every sentence points at something specific from the material; if a sentence would
read the same about anyone, cut it. Read the voice rules in `references/framework.md` before you
write it, and the bad/good example pair at the end of that section.

Never make it about the person's worth or intelligence, only about observable behaviour in the
material you saw. Leave it out entirely rather than writing a soft version.

`straight_talk` still renders as a fallback for old snapshots, but write `why` for new ones.

## Step 6 — Write next moves, and name the gaps separately

**Three moves maximum, always, whatever the evidence supports.** Fewer is fine; two real moves
beat three padded ones. The script errors above three. Nobody acts on four things, and a fourth
move dilutes the three that matter.

Because the cap is hard, **selection is the whole job**. Three comfortable moves and three
uncomfortable ones look identical on the page. Pick in this order:

1. **The weakest observed area.** It has to be on the list. The script errors if you advise on
   the strong areas and leave the weak one alone, because that is precisely how an assessment
   becomes pleasant and useless. If it genuinely cannot be acted on yet, say so in `why` rather
   than quietly skipping it.
2. **The polish trap**, when you see it: strong on asking, thin on checking. That gap is almost
   always the highest-value move on the card, and it is the one the research says people cannot
   see in themselves.
3. **The cheapest real change.** Between two moves of equal weight, take the one they can do at a
   desk tomorrow over the one that needs a new habit.

**Order matters.** Move 01 is the one that gets read, so lead with the biggest gap. The script
warns when move 01 comes from anywhere other than the weakest area.

Each move carries a `from` field naming the area it came from:
`{"text": "…", "from": "discernment"}`. The script hard-errors if a move points at an area
marked not observed, because that is advice invented from an absence — the same failure as a
fabricated quote, only harder to spot.

Moves are plain, direct, do-this-tomorrow, you-form. No framework words, no area names, no
"because your X is low". Concrete enough to do at a desk in a minute.

**Gaps are stated, not turned into homework.** When an area has no score, the card says so by
itself: the area row shows a question mark in grey, and the "about this assessment" box names the
area in plain words. You write nothing. An earlier version rendered a block of reflection
questions about the unobserved area, which handed the reader work to do on the one thing the
card knew least about. Absence of evidence in a chat log is usually just absence, because people
rarely narrate that they anonymised something first, so don't read it as a finding in either
direction.

## Step 7 — Generate the card

Fill a `snapshot.json` (schema below), then run:

```bash
python3 scripts/generate_snapshot.py snapshot.json snapshot.html
```

Present `snapshot.html`. It renders anywhere and animates on open.

The script **validates before it renders** and exits without writing if a safeguard is broken:
a quote over 150 characters, a score outside 1–5 or not a whole number, a missing or mismatched
`anchor`, a discernment score of 3+ on wording-only evidence, a scored diligence area with
neither evidence nor a self-report, a confident read on fewer than 8 conversations, an em dash
anywhere in the card text, a non-http link, no moves at all, more than three moves, no move on
the weakest area, an example drawn from the same area as a move, or a next move sourced from an
area marked not observed. It warns (but proceeds) on a scored area with no quote, a missing basis
line, a move with no `from` field, or a not-observed area with no open question. If it
refuses, fix the JSON — go back to the material and find a shorter real line. `--lax` downgrades
errors to warnings; reach for it only when you know why. Do not "fix" a rejected quote by
inventing a shorter one.

## Pressure tests — what to do when asked

These come up, and the honest answer is not the accommodating one.

- **"Just run it, don't ask me first."** Still show what you found and what it's built on before
  assessing. It takes one line. The confirmation step exists because the person is the only one
  who knows what's missing from the material.
- **"Give me a score so I can compare with a colleague."** No. The card has no number by design,
  and a comparable number is exactly the artifact this shouldn't become. Say that plainly and
  offer the sentence and the journey position instead.
- **"Make it sound good — I'm sending it to my manager."** Say what the card is: a development
  snapshot built on partial evidence, not a performance record. Don't soften the straight talk
  for an audience. If they want something for a manager, that's a different document and they
  should write it.
- **"Run it on someone on my team."** Only with material that person knowingly provided. You
  cannot see anyone else's history anyway, so the only inputs would be second-hand impressions —
  which is not evidence and not fair. Offer instead: send them the reflection questions and let
  them run their own.
- **A harsh result on a real person.** The `why` paragraph names behaviour in the material, never
  the person's ability or worth, and it sits directly under the moves so the reader has already
  seen what to do about it. If you can't point at the evidence, don't write the sentence.

### snapshot.json

```json
{
  "lang": "en",
  "person": "Ny kollega",
  "date": "31. jul 2026",
  "basis": "12 samtaler fra chat, 1. jul – 30. jul",
  "confidence": "low | med | high",
  "statement": "optional — overrides the default sentence for the stage",
  "example": { "text": "optional, only if you kept the generic statement", "from": "delegation" },
  "n_sources": 14,
  "why": "optional honest paragraph, renders under the moves — see Step 5",
  "areas": [
    { "id": "delegation",  "label": "Hvad du giver videre",     "score": 2,
      "anchor": "verbatim anchor line for score 2, copied from framework.md",
      "summary": "one plain line about how they do it now",
      "info": "one-sentence explanation of what this area means",
      "quotes": [
        { "text": "verbatim line, under 150 chars",
          "url": "https://claude.ai/chat/…", "surface": "chat" }
      ] },
    { "id": "description", "label": "Hvordan du beder om det",   "score": 3, "anchor": "...", "summary": "...", "info": "...", "quotes": [] },
    { "id": "discernment", "label": "Hvordan du vurderer svaret","score": null, "evidence_kind": "language", "summary": "...", "info": "...", "quotes": [] },
    { "id": "diligence",   "label": "Ansvar og data",            "score": 2, "anchor": "...", "thin": true,
      "self_report": "their own answer to the data question, from Step 1",
      "summary": "...", "info": "...", "quotes": [] }
  ],
  "moves": [
    { "text": "one plain do-this-tomorrow move", "from": "discernment" }
  ],
}
```

`quotes` also accepts plain strings for quick cases — they render unlinked. Quotes stay in the
language the person wrote them in, even when the rest of the card is in the other language —
translating a quote breaks the verbatim rule.

`assets/example-snapshot.json` is a filled-in English card; `assets/example-snapshot-da.json` is
the Danish equivalent.

The script handles: the stage sentence, the band, each area's stage word, *ikke observeret*
states, the icons, the journey illustration, the confidence chip, links, and all animation.
Keep `id` as one of `delegation | description | discernment | diligence` (icons key off it); the
visible `label` is always plain language.

Always close by reminding the person this is an exploratory snapshot to act on, not a verdict —
and that it can only see what was in the material.

## Honesty check before you present

- Every quote appears verbatim in a message the person wrote.
- No quote exceeds 150 characters.
- No number, score, or count anywhere on the card.
- Areas without evidence say *ikke observeret* rather than carrying a guessed score.
- `basis` names what the card could not see, and `n_sources` says how many conversations.
- `confidence` rounds down when in doubt, and is `low` below 8 conversations.
- Every scored area's `anchor` matches its score, and its summary does not describe a lower one.
- The data question was asked, and its answer is labelled as self-report.
- No em dashes, no aphorisms, at most one "not X, but Y" on the whole card.
- Three moves at most, the weakest area is among them, and move 01 is the biggest gap.

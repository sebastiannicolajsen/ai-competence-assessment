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

## Step 1 — Gather evidence, then stop and confirm

- If the person has chat history, use `recent_chats` and `conversation_search` to pull their real
  conversations. Aim for ~30 days or up to 20 conversations. **Keep the `url` attribute of every
  chat you pull** — you will attach it to the quotes so they link back to their origin.
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
Add one concrete `"example"` line drawn from what you saw — this is what makes it land.

The three sentences differ **a lot** in meaning; don't blur them:

- assisteret — AI helps with single tasks, when it occurs to them
- integreret — AI is a fixed part of how several tasks get done
- transformativ — tasks get solved in ways that would not exist without AI

## Step 5 — Straight talk (optional, but the point of the exercise)

Required at `med` or `high` confidence; optional only at `low`.

`"straight_talk"` is one short paragraph of honest observation — what you'd say about this person
to a colleague, not to their face. Name what's actually weak, in plain words, without a
compliment wrapped around it. No praise-padding, no "but overall you're doing great". Two to four
sentences. Leave it out entirely rather than writing a soft version.

Never make it about the person's worth or intelligence — only about observable behavior in the
material you saw.

## Step 6 — Write next moves, and name the gaps separately

**One move per area you actually saw. At most three, at least one — never a fixed quota.**

Each move carries a `from` field naming the area it came from:
`{"text": "…", "from": "discernment"}`. The script hard-errors if a move points at an area
marked not observed, because that is advice invented from an absence — the same failure as a
fabricated quote, only harder to spot. If you find yourself reaching for a third move because
three looks better than two, write two.

Moves are plain, direct, do-this-tomorrow, you-form. No framework words, no area names, no
"because your X is low". Concrete enough to do at a desk in a minute.

**Gaps go in `open_questions`, not in the moves.** When an area is not observed, the honest
output is a question, not a recommendation: *"Hvad lægger du faktisk ind i AI — og har I aftalt
på teamet, hvad man må?"* It renders in its own block, visually separated from the advice, with
a line saying there's nothing to base a recommendation on. Absence of evidence in a chat log is
usually just absence — people rarely narrate that they anonymised something first — so don't
read it as a finding in either direction.  Further, explain your points well in the improvements (e.g., what you mean with `the frame is found in the second message`)

## Step 7 — Generate the card

Fill a `snapshot.json` (schema below), then run:

```bash
python3 scripts/generate_snapshot.py snapshot.json snapshot.html
```

Present `snapshot.html`. It renders anywhere and animates on open.

The script **validates before it renders** and exits without writing if a safeguard is broken:
a quote over 150 characters, a score outside 1–5, a non-http link, or a next move sourced from an
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
- **A harsh result on a real person.** Straight talk names behavior in the material, never the
  person's ability or worth, and always sits next to three concrete next moves. If you can't
  point at the evidence, don't write the sentence.

### snapshot.json

```json
{
  "lang": "en",
  "person": "Ny kollega",
  "date": "31. jul 2026",
  "basis": "12 samtaler fra chat, 1. jul – 30. jul",
  "confidence": "low | med | high",
  "statement": "optional — overrides the default sentence for the stage",
  "example": "Fx bygger du dine egne skabeloner og genbruger dem på tværs af opgaver.",
  "straight_talk": "optional honest paragraph — see Step 5",
  "areas": [
    { "id": "delegation",  "label": "Hvad du giver videre",     "score": 2,
      "summary": "one plain line about how they do it now",
      "info": "one-sentence explanation of what this area means",
      "quotes": [
        { "text": "verbatim line, under 150 chars",
          "url": "https://claude.ai/chat/…", "surface": "chat" }
      ] },
    { "id": "description", "label": "Hvordan du beder om det",   "score": 3, "summary": "...", "info": "...", "quotes": [] },
    { "id": "discernment", "label": "Hvordan du vurderer svaret","score": null, "summary": "...", "info": "...", "quotes": [] },
    { "id": "diligence",   "label": "Ansvar og data",            "score": 2, "thin": true, "summary": "...", "info": "...", "quotes": [] }
  ],
  "moves": [
    { "text": "one plain do-this-tomorrow move", "from": "discernment" }
  ],
  "open_questions": ["a question for an area the material could not show"],
  "epigraph": "optional closing line"
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
- `basis` names what the card could not see.
- `confidence` rounds down when in doubt.

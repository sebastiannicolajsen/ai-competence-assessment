# Reference — framing, labels, scoring, safeguards

You already know the underlying 4D AI Fluency competencies (Dakan & Feller with Anthropic). This file only fixes the
**plain-language framing**, the **label sets in both languages**, the **1–5 anchors**, and the
**evidence safeguards** so the output is consistent and never shows the framework to the reader.

**English is the default.** Danish is fully supported — every label, stage name, headline
sentence and reflection question below exists in both. Write the card in whichever language the
person is using.

## Tone (applies to everything on the card)

Everyday words, second person. No consultant- or framework-speak. Say it out loud: if you
wouldn't say it to a colleague by the coffee machine, rewrite it. Danish uses du-form, never De.
Never print the words "4D", "Delegation/Description/Discernment/Diligence", "competency",
"kompetence", or "framework".

## Scoring posture — read this before you score anything

**Assisted is the default. Most people are assisted, and that is not an insult.** An assessment
that moves people up quickly feels generous and is worthless: if almost everyone comes out
integrated, the word stops carrying information.

- **When torn between two anchors, take the lower one.** Scoring up is this tool's failure mode,
  not scoring down. Enthusiasm, volume of use, and fluent prompts are not competence.
- **3 is a genuinely good score.** It means a real, working habit. Most competent professionals
  sit at 2–3 in most areas.
- **4 means demonstrated consistently across different kinds of work**, not once impressively.
- **5 is rare.** It requires that the person has built something reusable that other people could
  pick up. If you are reaching for reasons to justify a 5, it is a 4.
- **Never score from the person's self-description of how good they are.** Score from what they
  did in the material.

## The four areas

Each has a stable `id` (used by the icons), a visible label per language, and 1–5 anchors.

### delegation
- EN label: *"What you hand over"* · DA label: *"Hvad du giver videre"*
- What it is: deciding what AI should do and what you keep yourself.

| | EN | DA |
|---|---|---|
| 1 | Uses AI at random, without thinking about what it's suited for. | Bruger AI tilfældigt, uden at tænke over hvad der egner sig. |
| 2 | Reaches for AI on impulse; sometimes on tasks that were faster by hand. | Griber AI i ny og næ; nogle gange til opgaver der var hurtigere selv. |
| 3 | Hands routine work to AI, keeps what needs judgement. | Giver rutineopgaver til AI, beholder det der kræver dømmekraft. |
| 4 | Decides deliberately, across different kinds of work, before opening AI. | Beslutter bevidst, på tværs af opgavetyper, før AI åbnes. |
| 5 | Has a clear sense of what AI should do, and builds reusable ways of doing it. | Har en klar fornemmelse af hvad AI skal lave, og bygger genbrugelige måder at gøre det på. |

### description
- EN label: *"How you ask"* · DA label: *"Hvordan du beder om det"*
- What it is: how clearly you explain what you want — goal, format, examples.

| | EN | DA |
|---|---|---|
| 1 | Vague messages; hopes AI guesses right. | Vage beskeder; håber AI gætter rigtigt. |
| 2 | Says roughly what's wanted; leaves format and constraints to chance. | Siger nogenlunde hvad der ønskes; overlader format og rammer til tilfældet. |
| 3 | Says clearly what you want; corrects when the answer misses. | Siger tydeligt hvad du vil; retter til når svaret rammer ved siden af. |
| 4 | Sets goal, format and constraints up front most of the time. | Sætter mål, format og rammer fra start det meste af tiden. |
| 5 | Sets frame, format and examples up front; makes it a habit. | Sætter rammer, format og eksempler fra start; gør det til en fast måde. |

### discernment
- EN label: *"How you judge the answer"* · DA label: *"Hvordan du vurderer svaret"*
- What it is: reading the answer critically and catching errors — especially when it looks good.

| | EN | DA |
|---|---|---|
| 1 | Takes the answer at face value. | Tager svaret for gode varer. |
| 2 | Reacts to what reads wrong; corrects wording, tone or structure rather than substance. | Reagerer på det der lyder forkert; retter formulering, tone eller struktur frem for indhold. |
| 3 | Catches errors in the content itself, not only in how it is written. | Fanger fejl i selve indholdet, ikke kun i måden det er skrevet på. |
| 4 | Verifies claims outside their own expertise, not only inside it. | Efterprøver også påstande uden for eget fagområde, ikke kun inden for. |
| 5 | Questions the answer even when it looks convincing; has standing checks. | Stiller spørgsmål til svaret selv når det ser overbevisende ud; har faste tjek. |

### diligence
- EN label: *"Care and data"* · DA label: *"Ansvar og data"*
- What it is: confirming an answer before you rely on it, and looking after what you put in.

**Read this before you score it. This area failed on every real run so far**, once as a
guessed thin score and once as a blank, and the cause is not laziness in the assessment. It is
the channel. The other three areas leave traces inside the messages. This one mostly does not:

- The decision about what goes into the tool happens *before* the conversation starts. Nobody
  types "I stripped the names out of this first."
- Verification that succeeds is silent. You only see checking when it fails.
- So the area can only come out blank or falsely positive if you look for it the way you look
  for the others.

**Therefore: split it.** Score only the verifying half, from the traces listed below. The
data-handling half is not scorable from a chat log at all. Ask the one question in Step 1 and put
the answer in `self_report`, labelled on the card as the person's own words. Self-report is weak
evidence and honest evidence at the same time. A labelled weak answer beats a confident blank.

**What actually leaves a trace (look for these, not for good intentions):**

- asking where a claim comes from, or for a source
- correcting a fact using knowledge from outside the conversation
- asking whether something is okay to share, or about where data ends up
- pasting material they have already redacted themselves
- coming back and reporting what happened when the output met reality
- pushing on a figure, date or name before using it

**Negative evidence counts.** Because you are only hunting positives, absence always reads
neutral and the score can only float upward. Pasting apparently identifying material with no
framing around it is observable, and it counts down.

**The anti-pattern, which has already been scored as a positive once:** asking the assistant to
check its own work ("please double check that these links are the same", "kan du lige tjekke
om det passer") is *delegating* the check to the thing being checked. It is not verification.
It is not evidence here, and at best it is a delegation observation.

| | EN | DA |
|---|---|---|
| 1 | Nothing you write suggests you check anything before using an answer. | Intet i det du skriver tyder på, at du tjekker noget, før du bruger et svar. |
| 2 | You notice problems when they surface, but you take the answer as it comes. | Du opdager problemer når de dukker op, men tager svaret som det kommer. |
| 3 | You ask where a claim comes from when it matters, at least some of the time. | Du spørger hvor en påstand kommer fra når det betyder noget, i hvert fald nogle gange. |
| 4 | You ask for the source, or check it yourself, before you pass work on. | Du beder om kilden, eller tjekker selv, før du sender arbejdet videre. |
| 5 | Checking before use is routine, and you say what can and cannot go into the tool. | Tjek før brug er rutine, og du siger til og fra om hvad der må lægges ind i værktøjet. |

## The anchor commitment (this is how a score stays honest)

Every scored area carries an `anchor` field holding the anchor line above, **copied verbatim** in
the card's language. The script checks it against the table and refuses to render on a mismatch.

This exists because of a specific, repeated failure: an area rendered *Integrated* while its own
summary said the person "catches things after something visibly fails, not as a routine", which
is the level-2 anchor almost word for word. Writing the anchor out makes the score a claim you
can check against your own summary, instead of a number that quietly drifts up.

Before you commit an anchor, read it next to the summary you wrote for that area. If the summary
describes a lower anchor than the score, the summary is usually the honest one.

**Wording-only evidence caps discernment at 2.** If every quote for that area is about tone,
grammar, phrasing or paragraph balance, the score is 2, whatever the volume. Set
`"evidence_kind"` to `language`, `substance` or `mixed`; the script errors on `language` with a
score of 3 or more.

**A null area needs no writing from you.** The card states the gap on its own, in the area row
and in the "about this assessment" box. **Never recommend on a null area.** If an area is not observed, it gets no next move — it gets an
open question instead. Advice built on an absence looks exactly like advice built on evidence, and
the reader can't tell them apart. Absence in a chat log is usually just absence: people don't
narrate that they checked a figure or anonymised a file.

**Score null = ikke observeret / not observed.** If the material shows nothing either way for an
area, set `"score": null`. The card says so plainly. A guessed 3 is worse than an honest blank,
because it looks like a finding.

## The three stages (the journey — this is what the reader sees)

| id | EN | DA | Meaning |
|---|---|---|---|
| assisted | Assisted | Assisteret | You use AI for one-off tasks, when it occurs to you. |
| integrated | Integrated | Integreret | AI is a fixed part of several of your tasks; you know when it helps. |
| transformative | Transformative | Transformativ | You solve tasks in new ways because AI is there — not just faster, but different. |

**The overall stage is gated, not averaged.** The script decides it; you supply the scores.

- **transformative** requires *all four* areas observed, an average above 4, no area below 3,
  **and discernment of at least 4**. Someone who never checks the answer is not transformative
  however fast they move — they are quick and unverified. Any unobserved area rules it out: a
  partial picture cannot earn the top claim.
- **integrated** requires an average of at least 3 across at least three observed areas.
- **assisted** otherwise, and it is the honest default.

Per-area stage words use `< 3 → assisted · 3–4 → integrated · > 4 → transformative`, so a 4 is
still integrated.

When the top stage isn't reached, the card prints one plain line naming what held it there —
missing areas, no verification, one weak area, or simply distance to go. Do not soften or remove
that line; it is the most useful sentence on the card.

## The headline sentence (the top of the card)

The card opens with **one sentence about how the person uses AI** — never a number.

| Stage | EN | DA |
|---|---|---|
| assisted | You use AI to assist you on individual tasks. | Du anvender AI til at assistere dig i enkelte opgaver. |
| integrated | You integrate AI continuously into your work. | Du integrerer AI kontinuerligt i dit arbejde. |
| transformative | You solve tasks in new ways because AI is part of them. | Du løser opgaver på nye måder, fordi AI er en del af dem. |

These three mean genuinely different things — don't blur them into "you use AI quite a bit."
Assisted is *occasional and task-shaped*. Integrated is *habitual and load-bearing*.
Transformative is *the task itself changed shape*.

Override with a more specific sentence when the material supports it. **Then drop the `example`
line.** The moves sit immediately below the headline, and a specific statement plus an example
plus three moves means the reader meets the same observation three times in one screen. Keep the
example only when the statement stays generic, and never draw it from an area a move came from.

## The polish trap (watch for this while scoring)

The clearer and more polished an answer looks, the *less* people check it. So a high "how you ask"
score often sits next to a thin "how you judge" score. If you see lots of confident output and
little checking, that gap is usually the most useful next move.

## Voice (the card is read by people who did not ask for a report)

Everything on the card is read by someone who may not be fluent in this stuff, and who did not
choose to be assessed. Write the way you would talk, and constrain yourself:

- **No em dashes.** House rule, and the loudest AI tell on the page. The script errors on one.
- **One "not X, but Y" construction on the whole card, at most.** One is a point. Three is a
  voice, and it is not a human one.
- **No heading that announces its own honesty.** The honest paragraph is not a performance with
  a name over it; it is the reason the three moves are these three.
- **One idea per sentence.** No triple parallel clauses inside a single sentence.
- **No aphorisms.** If a line would work on a poster, it is doing nothing here. Cut it.
- Every sentence in the `why` paragraph points at something specific from the material. If it
  would read the same about anyone, delete it.

Bad, and drawn from a real card:

> Most of what you catch, you catch because something already looked wrong, not because you have
> a standing habit of checking before you use an answer. Your strongest habit is iterating on
> tone and wording until it's right, which is real skill, but it's a polish check, not a
> substance check.

Two reversals, three clauses deep, and the compliment exists to cushion the point.

Better:

> Your checking happens after something looks wrong. The link that failed, the survey question
> aimed at the wrong thing. You are quick on tone and wording. Nothing in these conversations
> shows you checking a fact before using it.

Shorter, no reversals, and each sentence names something that actually happened.

## Evidence safeguards (non-negotiable)

1. **Verbatim only.** Quotes are copied exactly from the person's own messages. No paraphrase in
   quote marks, no tidying, no stitching two messages together. Quote in the language they wrote
   in — never translate a quote, even when the rest of the card is in the other language.
2. **Their turns only.** Never quote the assistant's output as evidence of the person.
3. **Under 150 characters.** Longer lines are truncated at a word boundary with `…`.
4. **Source attached.** Each quote carries the `url` of the conversation it came from and a
   `surface` tag. Links are conversation-level — they open the chat, not the exact message — and
   only work for the account that owns the history. Sandboxed previews may block them entirely;
   the card reveals the raw address as a fallback.
5. **No quote, no claim.** If you can't find a real line for an area, leave `quotes` empty and let
   the card show it as thin or not observed.
6. **Redact.** Client names, colleagues' names, and personal data don't go on the card. Swap the
   quote or replace the fragment with `[…]`.
7. **Nothing invented.** Summaries, examples and straight talk describe only what was in the
   material. No plausible-sounding filler.

## Honesty: basis and confidence

- **basis** — one plain line naming the evidence ("6 reflection questions — your own answers",
  "12 conversations from chat, 1–30 July"). If real work is invisible (other tools, offline), say so.
- **confidence** — `low` for self-report or thin history (most new starters), `med` for a few real
  conversations, `high` only for rich, varied real usage. Round down when unsure.
- **retrieval floor.** Put the number of conversations in `n_sources`. Below 8, confidence is
  forced to `low` and the script errors if you claim otherwise. This is not pedantry: two runs on
  the same person over the same window pulled 7 conversations and 20, shared no evidence at all,
  and landed on different stages. Retrieval variance is currently the single largest source of
  error in this card, so a thin pull is not allowed to carry a confident conclusion.

Self-report is honest evidence, but it's weak evidence: it reflects how someone *thinks* they
work, not how they do. A new starter's snapshot is almost always `low` confidence, and the card
should say so plainly rather than dress a guess up as a measurement.

## Straight talk (required at med or high confidence)

Write it whenever there's enough evidence to say something real — that is, at `med` or `high`
confidence. Only omit it at `low`, where there isn't enough material to be fair.

Modelled on the "tell them what you actually saw" ask, not on a recommendation letter. One short
paragraph, plain, no compliment sandwich, naming the real weakness in behavior — never in
character. If you catch yourself softening it, either write the honest version or leave the block
out. It's about how the work went, not about who they are.

## Reflection questions (use when there's little chat history — e.g. a new starter)

Ask these plainly, one at a time is fine. Areas in brackets.

| # | EN | DA | Area |
|---|---|---|---|
| 1 | Before you use AI, do you decide what it should do and what you'll keep yourself? | Når du skal bruge AI, beslutter du så først hvad AI skal lave, og hvad du selv holder fast i? | delegation |
| 2 | How often do you end up using AI for something you'd have been better off doing yourself? | Hvor tit ender du med at bruge AI til noget, du hellere selv skulle have gjort? | delegation |
| 3 | Do you spell out what you want — format, length, an example — or fire off a short message? | Skriver du tydeligt hvad du vil have — format, længde, et eksempel — eller kaster du en kort besked af sted? | description |
| 4 | When an answer looks right, do you check anything in it before you use it? | Når du får et svar der ser rigtigt ud, tjekker du så noget i det, før du bruger det? | discernment |
| 5 | Have you hit an AI answer that sounded convincing but was wrong? What did you do? | Er du stødt på et AI-svar, der lød overbevisende men var forkert? Hvad gjorde du? | discernment |
| 6 | Do you think about what information you put in, for example ID numbers, salary, client data? | Tænker du over, hvilke oplysninger du lægger ind, fx CPR, løn, kundedata? | diligence |

**Question 6 is asked on every run**, including runs with plenty of chat history, because it is
the one thing the material structurally cannot show. Ask it on its own in Step 1, keep the answer
short, and put it in the diligence area's `self_report`. If the person does not answer, the area
goes to `null` and the gap becomes an open question. Do not infer an answer from their tone.

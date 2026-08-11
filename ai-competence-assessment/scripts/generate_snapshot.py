#!/usr/bin/env python3
"""Generate a standalone AI-fluency snapshot card (HTML) from a snapshot.json.

English by default; pass "lang": "da" for Danish.

Usage: python3 generate_snapshot.py snapshot.json snapshot.html

Only the standard library is used, so it runs offline. All visual/interaction
complexity lives here; the SKILL.md just supplies data.

Design rule enforced here: the card never prints a number. Scores in the JSON
are internal only — they position the journey marker and the area bars.
"""
import json
import sys
from html import escape

# ---- text by language --------------------------------------------------------
T = {
    "da": {
        "eyebrow": "AI-vurdering",
        "journey": "Din rejse",
        "here": "du er her",
        "areas": "S\u00e5dan arbejder du med AI",
        "areas_hint": "Klik p\u00e5 et felt for at se dine egne ord",
        "moves": "Dine n\u00e6ste skridt",
        "why_h": "Hvorfor de her",
        "open_h": "Det kunne kortet ikke se",
        "open_note": "Ingen anbefaling her. Der er ikke noget at bygge den p\u00e5. Tag sp\u00f8rgsm\u00e5let med til en kollega i stedet.",
        "explain": "Forklar",
        "selfreport": "det har du selv fortalt",
        "stages": {
            "assisted": ("Assisteret", "Du bruger AI til enkeltopgaver, n\u00e5r du kommer i tanke om det."),
            "integrated": ("Integreret", "AI er en fast del af flere af dine opgaver. Du ved hvorn\u00e5r det hj\u00e6lper."),
            "transformative": ("Transformativ", "Du l\u00f8ser opgaver p\u00e5 nye m\u00e5der, fordi AI er der. Ikke bare hurtigere, men anderledes."),
        },
        "statements": {
            "assisted": "Du anvender AI til at assistere dig i enkelte opgaver.",
            "integrated": "Du integrerer AI kontinuerligt i dit arbejde.",
            "transformative": "Du l\u00f8ser opgaver p\u00e5 nye m\u00e5der, fordi AI er en del af dem.",
        },
        "statement_none": "Der er endnu ikke nok at se p\u00e5 til at sige, hvordan du bruger AI.",
        "thin": "tyndt bel\u00e6g",
        "unseen": "ikke observeret",
        "unseen_note": "Intet i materialet viser det her, hverken godt eller skidt.",
        "basis_label": "Bygget p\u00e5",
        "conf_label": "Sikkerhed i analysen",
        "about_h": "Om denne vurdering",
        "n_areas": "{n} omr\u00e5der",
        "not_seen": "Kortet kunne ikke se {areas} i materialet. Det er hverken godt eller skidt, men der er ikke bygget nogen anbefaling p\u00e5 det.",
        "caps": {
            "partial": "Ikke h\u00f8jere, fordi kortet ikke kunne se alle fire omr\u00e5der. Delvist billede, delvis konklusion.",
            "unchecked": "Ikke h\u00f8jere, fordi der er lidt der tyder p\u00e5, at du efterpr\u00f8ver svarene. Hurtigt er ikke det samme som godt.",
            "uneven": "Ikke h\u00f8jere, fordi \u00e9t omr\u00e5de tr\u00e6kker tydeligt ned. K\u00e6den er ikke st\u00e6rkere end det svageste led.",
            "short": "Ikke h\u00f8jere endnu. Der er et stykke vej igen p\u00e5 tv\u00e6rs af omr\u00e5derne.",
        },
        "conf": {"low": "lav", "med": "middel", "high": "h\u00f8j"},
        "conf_info": {
            "low": "Bygget p\u00e5 f\u00e5 oplysninger, fx dine egne svar frem for hvordan du faktisk arbejder. Tag det som et udgangspunkt, ikke et facit.",
            "med": "Bygget p\u00e5 nogle f\u00e5 rigtige samtaler. Et rimeligt billede, men langtfra fuldt.",
            "high": "Bygget p\u00e5 mange, varierede samtaler, men stadig kun det der kunne ses.",
        },
        "limit_note": "Den kan kun se det, der er her. Ikke dit arbejde i andre v\u00e6rkt\u00f8jer eller det, du g\u00f8r uden AI. Brug det som et opl\u00e6g til samtale, ikke en m\u00e5ling.",
        "src": {"chat": "chat", "cc": "Claude Code", "cowork": "Cowork", "refleksion": "refleksion"},
        "src_hint": "\u00c5bn samtalen",
        "copy_hint": "Kopi\u00e9r link",
        "copied": "kopieret",
    },
    "en": {
        "eyebrow": "AI Assessment",
        "journey": "Your journey",
        "here": "you are here",
        "areas": "How you work with AI",
        "areas_hint": "Click a card to see your own words",
        "moves": "Your next moves",
        "why_h": "Why these",
        "open_h": "What the card couldn't see",
        "open_note": "No recommendation here. There is nothing to base one on. Take the question to a colleague instead.",
        "explain": "Explain",
        "selfreport": "you told me this",
        "stages": {
            "assisted": ("Assisted", "You use AI for one-off tasks, when it occurs to you."),
            "integrated": ("Integrated", "AI is a fixed part of several of your tasks. You know when it helps."),
            "transformative": ("Transformative", "You solve tasks in new ways because AI is there. Not just faster, but different."),
        },
        "statements": {
            "assisted": "You use AI to assist you on individual tasks.",
            "integrated": "You integrate AI continuously into your work.",
            "transformative": "You solve tasks in new ways because AI is part of them.",
        },
        "statement_none": "There isn't enough here yet to say how you use AI.",
        "thin": "thin evidence",
        "unseen": "not observed",
        "unseen_note": "Nothing in the material shows this, neither good nor bad.",
        "basis_label": "Built on",
        "conf_label": "Confidence in this read",
        "about_h": "About this assessment",
        "n_areas": "{n} areas",
        "not_seen": "The card couldn't see {areas} in the material. That is neither good nor bad, but nothing here is built on it.",
        "caps": {
            "partial": "No higher, because the card couldn't see all four areas. A partial picture earns a partial conclusion.",
            "unchecked": "No higher, because there's little sign you verify what you get back. Fast is not the same as good.",
            "uneven": "No higher, because one area is clearly dragging. The chain is only as strong as its weakest link.",
            "short": "Not yet. There's ground to cover across the areas.",
        },
        "conf": {"low": "low", "med": "medium", "high": "high"},
        "conf_info": {
            "low": "Built on little, for example your own answers rather than how you actually work. Treat it as a starting point, not a fact.",
            "med": "Built on a handful of real conversations. A fair picture, but far from complete.",
            "high": "Built on many varied conversations, but still only what could be seen.",
        },
        "limit_note": "It can only see what's here. Not your work in other tools or what you do without AI. Use it as a conversation starter, not a measurement.",
        "src": {"chat": "chat", "cc": "Claude Code", "cowork": "Cowork", "refleksion": "reflection"},
        "src_hint": "Open the conversation",
        "copy_hint": "Copy link",
        "copied": "copied",
    },
}

# Anchor text, verbatim from references/framework.md. The model must copy the
# anchor it picked into the area's "anchor" field; this table is what makes that
# claim checkable instead of decorative. Mismatch is an error, because "score 3
# with a summary describing level-2 behaviour" was the single most common failure
# in real runs and nothing in the pipeline caught it.
ANCHORS = {
    "delegation": {
        1: {"en": "Uses AI at random, without thinking about what it's suited for.",
            "da": "Bruger AI tilf\u00e6ldigt, uden at t\u00e6nke over hvad der egner sig."},
        2: {"en": "Reaches for AI on impulse; sometimes on tasks that were faster by hand.",
            "da": "Griber AI i ny og n\u00e6; nogle gange til opgaver der var hurtigere selv."},
        3: {"en": "Hands routine work to AI, keeps what needs judgement.",
            "da": "Giver rutineopgaver til AI, beholder det der kr\u00e6ver d\u00f8mmekraft."},
        4: {"en": "Decides deliberately, across different kinds of work, before opening AI.",
            "da": "Beslutter bevidst, p\u00e5 tv\u00e6rs af opgavetyper, f\u00f8r AI \u00e5bnes."},
        5: {"en": "Has a clear sense of what AI should do, and builds reusable ways of doing it.",
            "da": "Har en klar fornemmelse af hvad AI skal lave, og bygger genbrugelige m\u00e5der at g\u00f8re det p\u00e5."},
    },
    "description": {
        1: {"en": "Vague messages; hopes AI guesses right.",
            "da": "Vage beskeder; h\u00e5ber AI g\u00e6tter rigtigt."},
        2: {"en": "Says roughly what's wanted; leaves format and constraints to chance.",
            "da": "Siger nogenlunde hvad der \u00f8nskes; overlader format og rammer til tilf\u00e6ldet."},
        3: {"en": "Says clearly what you want; corrects when the answer misses.",
            "da": "Siger tydeligt hvad du vil; retter til n\u00e5r svaret rammer ved siden af."},
        4: {"en": "Sets goal, format and constraints up front most of the time.",
            "da": "S\u00e6tter m\u00e5l, format og rammer fra start det meste af tiden."},
        5: {"en": "Sets frame, format and examples up front; makes it a habit.",
            "da": "S\u00e6tter rammer, format og eksempler fra start; g\u00f8r det til en fast m\u00e5de."},
    },
    "discernment": {
        1: {"en": "Takes the answer at face value.",
            "da": "Tager svaret for gode varer."},
        2: {"en": "Reacts to what reads wrong; corrects wording, tone or structure rather than substance.",
            "da": "Reagerer p\u00e5 det der lyder forkert; retter formulering, tone eller struktur frem for indhold."},
        3: {"en": "Catches errors in the content itself, not only in how it is written.",
            "da": "Fanger fejl i selve indholdet, ikke kun i m\u00e5den det er skrevet p\u00e5."},
        4: {"en": "Verifies claims outside their own expertise, not only inside it.",
            "da": "Efterpr\u00f8ver ogs\u00e5 p\u00e5stande uden for eget fagomr\u00e5de, ikke kun inden for."},
        5: {"en": "Questions the answer even when it looks convincing; has standing checks.",
            "da": "Stiller sp\u00f8rgsm\u00e5l til svaret selv n\u00e5r det ser overbevisende ud; har faste tjek."},
    },
    "diligence": {
        1: {"en": "Nothing you write suggests you check anything before using an answer.",
            "da": "Intet i det du skriver tyder p\u00e5, at du tjekker noget, f\u00f8r du bruger et svar."},
        2: {"en": "You notice problems when they surface, but you take the answer as it comes.",
            "da": "Du opdager problemer n\u00e5r de dukker op, men tager svaret som det kommer."},
        3: {"en": "You ask where a claim comes from when it matters, at least some of the time.",
            "da": "Du sp\u00f8rger hvor en p\u00e5stand kommer fra n\u00e5r det betyder noget, i hvert fald nogle gange."},
        4: {"en": "You ask for the source, or check it yourself, before you pass work on.",
            "da": "Du beder om kilden, eller tjekker selv, f\u00f8r du sender arbejdet videre."},
        5: {"en": "Checking before use is routine, and you say what can and cannot go into the tool.",
            "da": "Tjek f\u00f8r brug er rutine, og du siger til og fra om hvad der m\u00e5 l\u00e6gges ind i v\u00e6rkt\u00f8jet."},
    },
}


# lucide-style stroke icons (inner markup), keyed by area id
ICONS = {
    "delegation": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.6" y1="13.5" x2="15.4" y2="17.5"/><line x1="15.4" y1="6.5" x2="8.6" y2="10.5"/>',
    "description": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "discernment": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    "diligence": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
}
INFO_ICON = '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>'
COPY_ICON = '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>'
QMARK_ICON = '<path d="M9.1 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>'
LINK_ICON = '<path d="M7 17 17 7"/><path d="M9 7h8v8"/>'


QUOTE_MAX = 150
VALID_IDS = ("delegation", "description", "discernment", "diligence")
VALID_SURFACES = ("chat", "cc", "cowork", "refleksion")
MIN_SOURCES = 8
MAX_MOVES = 3


def word_trunc(text, limit=QUOTE_MAX):
    """Truncate at a word boundary, the only edit the skill permits on a quote."""
    if len(text) <= limit:
        return text
    cut = text[:limit - 1]
    if " " in cut:
        cut = cut[:cut.rfind(" ")]
    return cut.rstrip(" ,.;:-") + "\u2026"


DELEGATED_CHECK = (
    "double check", "double-check", "can you check", "can you verify", "please verify",
    "dobbelttjek", "kan du tjekke", "tjek lige", "vil du tjekke", "tjekke om",
)


def validate(data, lax=False):
    """Enforce the evidence safeguards in code, not just in prose.

    Returns (errors, warnings). Errors block generation unless --lax is passed,
    because a rule that only lives in the SKILL.md is the first thing to go when
    the model is under pressure to produce a nice-looking card.
    """
    errors, warns = [], []
    lang = data.get("lang", "en")
    lang = lang if lang in ("en", "da") else "en"
    areas = data.get("areas") or []
    if not areas:
        errors.append("no areas in snapshot.json")

    scored = 0
    for i, a in enumerate(areas):
        aid = a.get("id")
        where = f"area[{i}] {aid or a.get('label') or '?'}"
        if aid not in VALID_IDS:
            warns.append(f"{where}: unknown id — icon will fall back to the generic one")
        s = a.get("score", None)
        if s is not None:
            scored += 1
            try:
                s = float(s)
            except (TypeError, ValueError):
                errors.append(f"{where}: score is not a number ({a.get('score')!r})")
                s = None
            if s is not None and not (1 <= s <= 5):
                errors.append(f"{where}: score {s} is outside 1–5 (it would be clamped silently)")
            elif s is not None and s != int(s):
                errors.append(f"{where}: score {s} is not a whole number. Scores name an anchor, "
                              f"and there is no anchor between two levels. Pick the lower one.")

        # --- the anchor commitment ------------------------------------------
        # A score is a claim about which anchor the person matched. Making the
        # model write that anchor out is what turns "3" from a vibe into a
        # checkable statement, and it is what catches a level-2 summary sitting
        # under a level-3 score.
        if s is not None and aid in ANCHORS and 1 <= s <= 5 and s == int(s):
            want = ANCHORS[aid][int(s)][lang]
            got = (a.get("anchor") or "").strip()
            if not got:
                errors.append(
                    f"{where}: score {int(s)} with no \"anchor\" field. Copy the anchor you "
                    f"matched, verbatim from references/framework.md:\n      \"{want}\"")
            elif " ".join(got.lower().split()) != " ".join(want.lower().split()):
                errors.append(
                    f"{where}: the anchor doesn't match score {int(s)}.\n"
                    f"      you wrote: \"{got}\"\n"
                    f"      level {int(s)} is: \"{want}\"\n"
                    f"      Either the score is wrong or the anchor is. Re-read the material and pick one.")

        # --- discernment: wording-only evidence cannot carry a 3 -------------
        if aid == "discernment" and s is not None:
            kind = (a.get("evidence_kind") or "").strip().lower()
            if not kind:
                warns.append(f"{where}: no \"evidence_kind\" — set it to language, substance or mixed "
                             f"so the wording-only cap can be checked")
            elif kind not in ("language", "substance", "mixed"):
                warns.append(f"{where}: unknown evidence_kind {kind!r}")
            elif kind == "language" and s >= 3:
                errors.append(
                    f"{where}: score {int(s)} on wording-only evidence. Catching a clumsy phrase is "
                    f"level 2, not level 3. If every quote is about tone, grammar or structure, "
                    f"the score is 2.")

        # --- diligence: the half that chat cannot see ------------------------
        if aid == "diligence":
            sr = (a.get("self_report") or "").strip()
            if s is not None and not sr and not (a.get("quotes") or []):
                errors.append(
                    f"{where}: scored with neither evidence nor a self-report answer. "
                    f"Responsible use is mostly invisible in a chat log; ask the data question "
                    f"and put the answer in \"self_report\", or set score to null.")
            if s is None and not sr:
                warns.append(
                    f"{where}: not observed and no self_report. This area comes out blank on almost "
                    f"every run. Ask the one data question in Step 1 rather than shipping a hole.")
            for q in (a.get("quotes") or []):
                t = (q if isinstance(q, str) else q.get("text", "")).lower()
                if any(k in t for k in DELEGATED_CHECK):
                    warns.append(
                        f"{where}: quote looks like asking AI to check its own work "
                        f"(\"{t[:48]}…\"). That is delegating the check, not performing one. "
                        f"It is not evidence here.")

        quotes = a.get("quotes") or []
        if s is not None and not quotes and not (a.get("self_report") or "").strip():
            warns.append(f"{where}: has a score but no quote — a claim with no evidence behind it")
        if s is None and quotes:
            warns.append(f"{where}: marked not-observed but carries quotes — pick one or the other")
        for q in quotes:
            q = {"text": q} if isinstance(q, str) else q
            t = (q.get("text") or "").strip()
            if not t:
                errors.append(f"{where}: empty quote")
                continue
            if len(t) > QUOTE_MAX:
                errors.append(
                    f"{where}: quote is {len(t)} chars, max {QUOTE_MAX}. "
                    f"Shorten it to a real line the person actually wrote, e.g.:\n"
                    f'      "{word_trunc(t)}"')
            raw = (q.get("url") or "").strip()
            if raw and not safe_url(raw):
                errors.append(f"{where}: url is not http(s) — dropped: {raw[:40]}")
            if not raw and q.get("surface") not in ("refleksion", None, ""):
                warns.append(f"{where}: quote from {q.get('surface')} has no url — it won't link back")
            if q.get("surface") and q["surface"] not in VALID_SURFACES:
                warns.append(f"{where}: unknown surface {q['surface']!r}")

    if scored == 0:
        warns.append("no area has a score — the card will say there isn't enough to go on")

    conf = str(data.get("confidence", "")).lower()
    if conf not in ("low", "med", "high"):
        warns.append(f"confidence {data.get('confidence')!r} not recognised — falling back to low")

    # --- retrieval floor -----------------------------------------------------
    # Two runs on the same person, same window, pulled 7 conversations and 20,
    # and landed on different stages. Thin retrieval is the instrument's weakest
    # link, so a thin pull is not allowed to carry a confident conclusion.
    n = data.get("n_sources")
    if n is None:
        warns.append("no n_sources — say how many conversations the card was built on so the "
                     "retrieval floor can be checked")
    else:
        try:
            n = int(n)
            if n < MIN_SOURCES and conf != "low":
                errors.append(
                    f"n_sources is {n} (floor is {MIN_SOURCES}) but confidence is '{conf}'. "
                    f"A thin pull cannot support a confident read. Set confidence to 'low', "
                    f"or go back and retrieve more.")
        except (TypeError, ValueError):
            warns.append(f"n_sources {n!r} is not a number")

    if not data.get("basis"):
        warns.append("no basis line — the card won't say what it was built on")
    moves = data.get("moves") or []
    unseen = [a.get("id") or a.get("label") or "?" for a in areas if a.get("score") is None]
    seen = [a.get("id") for a in areas if a.get("score") is not None]
    if not moves:
        errors.append("no next moves. The moves are the first thing the reader sees now; "
                      "a card without them is a diagnosis with no action.")
    if len(moves) > scored:
        errors.append(
            f"{len(moves)} next moves but only {scored} area(s) with evidence. "
            f"Every move must point at something you actually saw. Drop the extra move, "
            f"or put it under open_questions.")
    if len(moves) > MAX_MOVES:
        errors.append(
            f"{len(moves)} next moves. The cap is {MAX_MOVES}, whatever the evidence supports. "
            f"Nobody acts on four things, and a fourth move dilutes the three that matter. "
            f"Cut to the {MAX_MOVES} that would change the most, and lead with the biggest gap.")

    # --- the biggest gap has to be on the list, and should lead ---------------
    # With a hard cap, selection is the whole game: three comfortable moves and
    # three uncomfortable ones look identical on the page.
    scored_areas = {a.get("id"): float(a["score"]) for a in areas if a.get("score") is not None}
    if scored_areas and moves:
        weakest_score = min(scored_areas.values())
        weakest = [i for i, v in scored_areas.items() if v == weakest_score]
        srcs = [m.get("from") for m in moves if isinstance(m, dict)]
        if srcs and not any(w in srcs for w in weakest):
            errors.append(
                f"the weakest observed area ({', '.join(weakest)}) has no next move, but "
                f"{', '.join(x for x in srcs if x)} do. Advising on the strong areas and leaving "
                f"the weak one alone is how an assessment becomes comfortable. Either move it in, "
                f"or say plainly in \"why\" that it cannot be acted on yet.")
        elif srcs and srcs[0] not in weakest:
            warns.append(
                f"move 01 comes from '{srcs[0]}' but the weakest area is "
                f"{' or '.join(weakest)}. The first move is the one that gets read. "
                f"Lead with the biggest gap unless you have a reason not to.")
    for i, m in enumerate(moves):
        if isinstance(m, str):
            warns.append(f"move[{i}]: no \"from\" field — provenance unchecked. Use "
                         f"{{\"text\": …, \"from\": \"<area id>\"}} so the evidence link is verifiable")
            continue
        src = m.get("from")
        if not m.get("text"):
            errors.append(f"move[{i}]: empty text")
        if src is None:
            warns.append(f"move[{i}]: no \"from\" field — provenance unchecked")
        elif src in unseen:
            errors.append(
                f"move[{i}]: recommends on '{src}', which is marked not observed. "
                f"You cannot advise on something the material didn't show. Move it to "
                f"open_questions, or find the evidence.")
        elif src not in seen:
            warns.append(f"move[{i}]: \"from\" is '{src}', which isn't an area on this card")

    # --- headline: statement, example and moves must not say the same thing ---
    # The example and the moves both reach for the person's most visible
    # behaviour, so left alone they collide, and the reader meets the same
    # observation twice before they have read anything new.
    ex = data.get("example")
    ex_text = (ex.get("text", "") if isinstance(ex, dict) else (ex or "")).strip()
    if ex_text:
        move_srcs = {m.get("from") for m in moves if isinstance(m, dict)}
        ex_from = ex.get("from") if isinstance(ex, dict) else None
        if ex_from and ex_from in move_srcs:
            errors.append(
                f"the example and a next move both come from '{ex_from}'. The reader meets the "
                f"same behaviour twice, once as illustration and once as advice. Draw the example "
                f"from a different area, or drop it.")
        elif not ex_from:
            warns.append('example has no "from" — set {"text": …, "from": "<area id>"} so the '
                         'overlap with the moves can be checked')
        if data.get("statement"):
            warns.append("both a custom statement and an example. A statement written for this "
                         "person already names the specific behaviour; the example then repeats "
                         "it. Keep one.")

    # --- voice ---------------------------------------------------------------
    prose = " ".join([str(data.get("statement") or ""),
                      str(data.get("why") or data.get("straight_talk") or "")] +
                     [ex_text] + [str(a.get("summary") or "") for a in areas] +
                     [str(m if isinstance(m, str) else m.get("text", "")) for m in moves] +
                     [str(q) for q in (data.get("open_questions") or [])])
    if "\u2014" in prose:
        errors.append("em dash in the card text. Not house style, and it is the loudest AI tell "
                      "on the page. Use a comma, a full stop, or rewrite the sentence.")
    if prose.lower().count("not just") + prose.lower().count("rather than") + \
       prose.lower().count("frem for") + prose.lower().count("ikke bare") > 2:
        warns.append("several 'not X but Y' constructions. One is a point; three is a voice. "
                     "Rewrite all but the sharpest as a plain statement.")

    if data.get("open_questions"):
        warns.append(
            "open_questions is no longer rendered. The gap is stated plainly in the "
            "'about this assessment' box, generated from the areas with no score. Handing the "
            "reader a list of questions about the one area the card knows least about was "
            "homework, not honesty.")
    return errors, warns


def stage_key(score):
    """Per-area stage word. Deliberately hard to reach the top: a 4 is still integrated."""
    return "assisted" if score < 3 else ("integrated" if score <= 4 else "transformative")


def overall_stage(areas):
    """Overall stage is gated, not averaged.

    Averaging lets a strong 'how you ask' score carry an uncritical worker into
    transformative, and lets an unobserved area quietly drop out of the mean
    instead of counting against the claim. Both are how an assessment flatters
    people. So: assisted is the default, and each step up has to be earned.

    Returns (stage_key, cap_reason) — cap_reason names, in plain words, the thing
    holding the person at their current stage, or "" if nothing is.
    """
    scored = {a.get("id"): float(a["score"]) for a in areas if a.get("score") is not None}
    if not scored:
        return None, ""
    composite = sum(scored.values()) / len(scored)
    observed_all = len(scored) == 4
    weakest = min(scored.values())
    discernment = scored.get("discernment")

    # --- transformative: everything must be visible, strong, and checked ---
    if composite > 4.0 and observed_all and weakest >= 3 and (discernment or 0) >= 4:
        return "transformative", ""

    # --- what is holding them back? most damning reason first ---
    reason = ""
    if not observed_all:
        reason = "partial"
    elif composite < 3.0:
        reason = "short"
    elif (discernment or 0) < 4:
        reason = "unchecked"
    elif weakest < 3:
        reason = "uneven"
    else:
        reason = "short"

    if composite >= 3.0 and len(scored) >= 3:
        return "integrated", reason
    return "assisted", reason


def pos(score):
    return max(0.0, min(100.0, (score - 1) / 4 * 100))


ZONES = {"assisted": (2.0, 35.0), "integrated": (40.0, 60.0), "transformative": (66.0, 96.0)}


def marker_pos(composite, stage):
    """Keep the marker inside the awarded stage's zone, so label and dot never disagree."""
    lo, hi = ZONES[stage]
    return min(hi, max(lo, pos(composite)))


def build_journey(composite, tr, stage=None):
    PAD, W, Y0, Y1 = 16, 560, 122, 28
    span = W - 2 * PAD

    def cap(t):
        return t ** 0.8

    def xy(t):
        return PAD + t * span, Y0 - cap(t) * (Y0 - Y1)

    pts = [xy(i / 40) for i in range(41)]
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    xa = PAD + 0.375 * span   # assisted|integrated boundary
    xb = PAD + 0.625 * span   # integrated|transformative boundary

    here = ""
    active_key = stage
    if composite is not None and stage is not None:
        mx, my = xy(marker_pos(composite, stage) / 100)
        # position lives on the outer <g> so the CSS pop animation (which sets
        # transform) can't fling the marker back to the origin.
        here = f'''<g transform="translate({mx:.1f} {my:.1f})"><g class="jmarker">
    <circle r="7" class="jhalo"/>
    <circle r="4.5" class="jdot"/>
    <text y="-13" text-anchor="middle" class="jhere">{escape(tr["here"])}</text>
  </g></g>'''

    svg = f'''<svg viewBox="0 0 {W} 132" class="journey" role="img" aria-label="{escape(tr["journey"])}">
  <line x1="{xa:.1f}" y1="18" x2="{xa:.1f}" y2="126" class="jdiv"/>
  <line x1="{xb:.1f}" y1="18" x2="{xb:.1f}" y2="126" class="jdiv"/>
  <path d="{d}" class="jpath" pathLength="1" fill="none"/>
  {here}
</svg>'''

    # stage labels as HTML, so each can carry a real info popover
    def zone(key, mid=False):
        name, meaning = tr["stages"][key]
        on = " on" if key == active_key else ""
        cls = "jz2 mid" if mid else "jz2"
        return (f'<span class="{cls}{on}"><span class="jzt">{escape(name)}</span>'
                f'<button class="info" aria-label="{tr["explain"]}: {escape(name, quote=True)}" '
                f'data-info="{escape(meaning, quote=True)}">'
                f'<svg viewBox="0 0 24 24">{INFO_ICON}</svg></button></span>')

    labels = (f'<div class="jlabels">{zone("assisted")}{zone("integrated", mid=True)}'
              f'{zone("transformative")}</div>')
    return svg + labels


def safe_url(url):
    """Only http/https links are rendered. Anything else (javascript:, data:) is dropped."""
    u = (url or "").strip()
    return u if u.lower().startswith(("http://", "https://")) else ""


def fold(title, body, hint="", open_=False):
    """A section the reader opens only if they want it.

    The card leads with three moves. Everything under them is the grounding for
    those moves, and grounding does not have to be read to be trusted, only to
    be available. Folding it is what keeps the card from reading as a report.
    """
    st = "true" if open_ else "false"
    cls = "fold open" if open_ else "fold"
    hint_html = f'<span class="fold-n">{escape(hint)}</span>' if hint else ""
    return (f'<div class="{cls}">'
            f'<button class="fold-h" aria-expanded="{st}" data-fold>'
            f'<span class="fold-t">{escape(title)}</span>'
            f'<span class="fold-r">{hint_html}<span class="chev" aria-hidden="true"></span></span>'
            f'</button>'
            f'<div class="fold-b"><div class="fold-in">{body}</div></div></div>')


def build_quote(q, tr):
    """Accepts a plain string or {text, url, surface}.

    Earlier versions intercepted the click and, when the sandbox blocked the
    window, printed the raw address into the card. In real runs every tile fell
    back, so the card carried ten naked URLs. Now the link is an ordinary link
    and the fallback is a copy button that says nothing until it is used.
    """
    if isinstance(q, str):
        q = {"text": q}
    text = escape(q.get("text", ""))
    surface = q.get("surface", "")
    label = tr["src"].get(surface, surface)
    url = safe_url(q.get("url", ""))
    tag = f'<span class="qsrc">{escape(label)}</span>' if label else ""
    if url:
        u = escape(url, quote=True)
        return (f'<li><span class="qrow">'
                f'<a class="q" href="{u}" target="_blank" rel="noopener" '
                f'title="{escape(tr["src_hint"], quote=True)}">&ldquo;{text}&rdquo;</a>'
                f'<span class="qmeta">{tag}'
                f'<button class="qcopy" data-url="{u}" data-done="{escape(tr["copied"], quote=True)}" '
                f'aria-label="{escape(tr["copy_hint"], quote=True)}" '
                f'title="{escape(tr["copy_hint"], quote=True)}">'
                f'<svg viewBox="0 0 24 24">{COPY_ICON}</svg></button>'
                f'</span></span></li>')
    return f'<li><span class="q">&ldquo;{text}&rdquo;<span class="qmeta">{tag}</span></span></li>'


def build_area(a, tr, idx):
    aid = a.get("id", "")
    icon = ICONS.get(aid, INFO_ICON)
    raw = a.get("score", None)
    observed = raw is not None
    score = float(raw) if observed else None
    sk = stage_key(score) if observed else "unseen"
    quotes = a.get("quotes", []) or []
    q_html = "".join(build_quote(q, tr) for q in quotes)
    # A self-report answer is real evidence and weak evidence at the same time,
    # so it renders next to the quotes but is labelled as what it is.
    sr = (a.get("self_report") or "").strip()
    if sr:
        q_html += (f'<li class="qself"><span class="q">{escape(sr)}'
                   f'<span class="qmeta"><span class="qsrc">{escape(tr["selfreport"])}</span></span>'
                   f'</span></li>')
    if not q_html:
        q_html = f'<li class="qnone">{escape(tr["unseen_note"] if not observed else tr["thin"])}</li>'
    thin_html = f'<span class="thin">{tr["thin"]}</span>' if a.get("thin") and observed else ""
    info = escape(a.get("info", ""), quote=True)
    delay = 0.15 + idx * 0.08
    pill = tr["stages"][sk][0] if observed else tr["unseen"]
    pill_cls = "stagepill" if observed else "stagepill unseen"
    # A dashed rule where the bar goes reads as a broken bar, which reads as
    # a bad score. Not-observed is not a low score, it is an absence, so it
    # gets a question mark and no track at all.
    if not observed:
        icon = QMARK_ICON
    bar = (f'<div class="bar"><span class="bar-fill" data-w="{pos(score):.1f}"></span>'
           f'<span class="bar-dot" data-x="{pos(score):.1f}"></span></div>') if observed else ""
    return f'''<div class="area stage-{sk}" style="animation-delay:{delay:.2f}s">
  <div class="area-head" role="button" tabindex="0" aria-expanded="false" data-toggle="quotes">
    <span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24">{icon}</svg></span>
    <span class="area-main">
      <span class="area-label">{escape(a.get("label",""))}{thin_html}</span>
      <span class="area-summary">{escape(a.get("summary",""))}</span>
    </span>
    <span class="area-right">
      <span class="{pill_cls}">{escape(pill)}</span>
      <button class="info" aria-label="{tr['explain']}" data-info="{info}"><svg viewBox="0 0 24 24">{INFO_ICON}</svg></button>
      <span class="chev" aria-hidden="true"></span>
    </span>
  </div>
  {bar}
  <div class="quotes"><ul>{q_html}</ul></div>
</div>'''


CSS = """
:root{
  --coral:#D87756; --coral-soft:rgba(216,119,86,0.08); --ink:#1A1A1A;
  --muted:#9B9893; --border:#E8E2D5; --border-soft:#F0ECE3; --track:#F1EDE6; --paper:#fff;
}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);
  font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased;padding:40px 18px}
.card{max-width:640px;margin:0 auto;background:var(--paper);border:1px solid var(--border);
  border-radius:16px;overflow:hidden;
  box-shadow:0 1px 3px rgba(0,0,0,.04),0 12px 40px rgba(0,0,0,.07);
  opacity:0;transform:translateY(14px);transition:opacity .6s ease,transform .6s cubic-bezier(.22,.61,.36,1)}
body.in .card{opacity:1;transform:none}
.stripe{height:4px;background:var(--coral)}
.pad{padding:30px 34px 30px}
.eyebrow{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--coral)}
.top{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:6px}
.date{font-size:11px;color:var(--muted);letter-spacing:.04em}

/* headline statement (replaces the old score block) */
.statement{font-size:25px;line-height:1.28;font-weight:400;letter-spacing:-.01em;margin:20px 0 0;
  max-width:42ch;opacity:0;transform:translateY(6px)}
body.in .statement{animation:fadeup .6s ease forwards .15s}
.example{font-size:14px;line-height:1.55;color:var(--muted);margin:8px 0 0;max-width:56ch;opacity:0}
body.in .example{animation:fadeup .6s ease forwards .3s}
.cap{margin:12px 0 0;font-size:12.5px;line-height:1.55;color:var(--ink);max-width:52ch;
  padding-left:12px;border-left:2px solid var(--coral);opacity:.85}

/* folds — everything below the moves is available, not imposed */
.fold{border-top:1px solid var(--border)}
.sec{margin-top:28px}
.sec-h{display:flex;align-items:baseline;justify-content:space-between;gap:10px;
  padding-bottom:10px;border-bottom:1px solid var(--border-soft);margin-bottom:2px}
.sec-t{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--coral)}
.sec-n{font-size:11px;color:var(--muted)}
.fold-h{display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%;
  background:none;border:none;padding:15px 0;cursor:pointer;text-align:left;color:inherit;font:inherit}
.fold-h:focus-visible{outline:2px solid var(--coral);outline-offset:3px;border-radius:8px}
.fold-t{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--coral)}
.fold-r{display:flex;align-items:center;gap:9px;flex:none}
.fold-n{font-size:11px;color:var(--muted)}
.fold-h .chev{margin:0}
/* display toggle, not a height animation: the body holds popovers and there is
   nothing to gain from clipping it mid-reveal */
.fold-b{display:none}
.fold.open>.fold-b{display:block;animation:foldin .22s ease}
@keyframes foldin{from{opacity:0;transform:translateY(-3px)}to{opacity:1;transform:none}}

/* the "what this is" box — deliberately not fine print */
.about{position:relative;margin-top:22px;border-top:1px solid var(--border)}
.about-h{display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%;
  background:none;border:none;padding:15px 0 14px;cursor:pointer;text-align:left;color:inherit;font:inherit}
.about-h:focus-visible{outline:2px solid var(--coral);outline-offset:3px;border-radius:8px}
.about-conf{font-size:13.5px;line-height:1.4;color:var(--ink)}
.about .fold-b{padding-bottom:16px}
.conf-v{font-weight:700}
.conf-low{color:var(--muted)}
.conf-med{color:var(--coral)}
.conf-high{color:var(--coral)}
.about-line{margin:0 0 5px;font-size:12px;line-height:1.55;color:#6E6A64}
.about-line:last-child{margin-bottom:0}

/* journey */
.j-h{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--coral);margin:30px 0 6px}
.journey{width:100%;height:auto;display:block}
.jpath{stroke:var(--coral);stroke-width:2;stroke-linecap:round;stroke-dashoffset:1;stroke-dasharray:4 5}
body.in .jpath{animation:draw 1.15s ease forwards .25s}
@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
.jdiv{stroke:var(--border);stroke-width:1}
.jlabels{display:flex;padding:0 2.86%;margin-top:2px}
.jz2{flex:0 0 37.5%;display:flex;align-items:center;justify-content:center;gap:1px}
.jz2.mid{flex-basis:25%}
.jzt{font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.jz2.on .jzt{color:var(--coral);font-weight:700}
.jz2 .info{width:18px;height:18px}
.jz2 .info svg{width:12px;height:12px}
.jmarker{opacity:0}
body.in .jmarker{animation:pop .4s ease forwards 1.25s}
@keyframes pop{from{opacity:0;transform:translateY(4px) scale(.6)}to{opacity:1}}
.jdot{fill:var(--coral)}
.jhalo{fill:rgba(216,119,86,.2)}
.jhere{font-size:10px;font-weight:700;fill:var(--coral)}

/* areas */
.sec-h{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:6px;margin:34px 0 6px}
.sec-h .t{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--coral)}
.sec-h .hint{font-size:11px;color:var(--muted)}
.area{border-top:1px solid var(--border-soft);opacity:0;position:relative}
.area:first-of-type{border-top:1px solid var(--border)}
body.in .area{animation:fadeup .5s ease forwards}
@keyframes fadeup{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.area-head{display:flex;align-items:center;gap:12px;padding:13px 0;cursor:pointer}
.area-head:focus-visible{outline:2px solid var(--coral);outline-offset:3px;border-radius:8px}
.ico{width:30px;height:30px;flex:none;display:grid;place-items:center;border-radius:8px;
  background:var(--coral-soft);color:var(--coral)}
.stage-unseen .ico{background:var(--track);color:#A8A49C}
.stage-unseen .area-label,.stage-unseen .area-summary{color:#8C8880}
.stage-unseen .area-head{padding:10px 0}
.ico svg{width:17px;height:17px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.area-main{flex:1;min-width:0}
.area-label{display:block;font-size:14px;font-weight:600}
.thin{display:inline-block;font-size:9px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  color:var(--coral);margin-left:8px;vertical-align:middle}
.area-summary{display:block;font-size:12.5px;color:var(--muted);margin-top:2px;line-height:1.4}
.area-right{display:flex;align-items:center;gap:8px;flex:none}
.stagepill{font-size:11px;color:var(--muted);white-space:nowrap}
.stagepill.unseen{font-size:10px;letter-spacing:.04em;color:#8C8880;background:var(--track);
  border-radius:999px;padding:2px 9px;white-space:nowrap}
.stage-transformative .stagepill{color:var(--coral);font-weight:600}
.info{width:22px;height:22px;flex:none;display:grid;place-items:center;border:none;background:none;
  padding:0;cursor:pointer;color:var(--muted);border-radius:50%;position:relative}
.info:hover,.info:focus-visible{color:var(--coral);outline:none}
.info svg{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.info.open{color:var(--coral);z-index:60}
.pop{position:absolute;right:-6px;bottom:26px;width:216px;background:#fff;border:1px solid var(--border);
  border-radius:10px;padding:10px 12px;font-size:12px;line-height:1.45;color:var(--ink);
  box-shadow:0 -6px 24px rgba(0,0,0,.12),0 2px 6px rgba(0,0,0,.06);z-index:61;display:none;
  text-align:left;font-weight:400;letter-spacing:normal;text-transform:none}
.pop::after{content:"";position:absolute;right:12px;bottom:-6px;width:10px;height:10px;background:#fff;
  border-right:1px solid var(--border);border-bottom:1px solid var(--border);transform:rotate(45deg)}
.info.open .pop{display:block}
.area-head:has(.info.open),.jz2:has(.info.open){position:relative;z-index:60}
.chev{width:9px;height:9px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);
  transform:rotate(45deg);transition:transform .2s;margin-left:2px}
.area-head[aria-expanded=true] .chev{transform:rotate(225deg)}
.bar{position:relative;height:8px;margin:0 0 2px}
.bar::before{content:"";position:absolute;inset:0;background:var(--track);border-radius:999px}
.bar-fill{position:absolute;top:0;left:0;height:8px;border-radius:999px;background:rgba(216,119,86,.28);
  width:0;transition:width .85s cubic-bezier(.22,.61,.36,1) .2s;z-index:1}
.bar-dot{position:absolute;top:50%;left:0;width:11px;height:11px;border-radius:50%;background:var(--coral);
  border:2px solid #fff;box-shadow:0 0 0 1px rgba(216,119,86,.35);transform:translate(-50%,-50%);
  transition:left .85s cubic-bezier(.22,.61,.36,1) .2s;z-index:2}
.quotes{max-height:0;overflow:hidden;transition:max-height .3s ease}
.quotes ul{margin:0;padding:2px 0 14px 42px;list-style:none}
.quotes li{font-size:13px;line-height:1.5;padding:5px 0 5px 12px;border-left:2px solid var(--coral);
  margin-bottom:4px}
.quotes li.qnone{border-left-color:var(--border);color:var(--muted);font-style:italic}
.q{display:block;color:var(--ink);text-decoration:none}
a.q:hover{color:var(--coral)}
.qmeta{display:inline-flex;align-items:center;gap:4px;margin-left:8px;white-space:nowrap;vertical-align:baseline}
.qsrc{font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
a.q:hover .qsrc{color:var(--coral)}
.qlink{width:11px;height:11px;fill:none;stroke:var(--muted);stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
a.q:hover .qlink{stroke:var(--coral)}
.qrow{display:flex;align-items:baseline;gap:8px}
.qrow .q{flex:1;min-width:0}
.qcopy{flex:none;width:20px;height:20px;display:grid;place-items:center;border:none;background:none;
  padding:0;cursor:pointer;color:var(--muted);border-radius:4px}
.qcopy:hover,.qcopy:focus-visible{color:var(--coral);outline:none}
.qcopy svg{width:12px;height:12px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.qcopy.done{color:var(--coral)}
.qself{border-left-style:dashed}
.jz2{position:relative}

/* moves — first thing under the headline, because it is the only part that
   asks the reader to do something. Everything below is the grounding for it. */
.moves{margin-top:26px;padding:18px 20px 14px;background:var(--coral-soft);border-radius:14px;
  opacity:0}
body.in .moves{animation:fadeup .6s ease forwards .35s}
.moves-h{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--coral);margin:0 0 2px}
.move{display:flex;gap:12px;padding:11px 0;border-top:1px solid rgba(216,119,86,.16)}
.move:first-of-type{border-top:none}
.move .n{font-size:12px;font-weight:700;color:var(--coral);width:20px;flex:none;padding-top:2px}
.move .txt{font-size:14px;line-height:1.5}
/* the honest paragraph, demoted from a headline act to the reason the three
   moves are these three. Same content, no announcement. */
.why{margin:10px 0 0;padding-top:12px;border-top:1px solid rgba(216,119,86,.16)}
.why-h{font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:4px}
.why p{margin:0;font-size:12.5px;line-height:1.6;color:var(--ink);opacity:.9}

/* open questions — a named gap, deliberately not advice */



@media (max-width:540px){.pad{padding:26px 20px}.statement{font-size:21px}.area-summary{display:none}.stagepill{display:none}}
@media (prefers-reduced-motion:reduce){
  .card,.jpath,.jmarker,.area,.bar-fill,.bar-dot,.statement,.example,.moves{animation:none!important;transition:none!important}
  .card{opacity:1;transform:none}.jpath{stroke-dashoffset:0}.jmarker{opacity:1}
  .area,.statement,.example,.moves{opacity:1;transform:none}
}
"""

JS = """
(function(){
  function ready(){
    document.body.classList.add('in');
    document.querySelectorAll('.bar-fill').forEach(function(e){ e.style.width = e.dataset.w + '%'; });
    document.querySelectorAll('.bar-dot').forEach(function(e){ e.style.left = e.dataset.x + '%'; });
  }
  function buildPop(btn){ var p=document.createElement('div'); p.className='pop';
    p.textContent = btn.dataset.info || ''; btn.appendChild(p); }
  document.querySelectorAll('.info').forEach(function(btn){ buildPop(btn);
    btn.addEventListener('click', function(ev){ ev.stopPropagation();
      var was = btn.classList.contains('open');
      document.querySelectorAll('.info.open').forEach(function(o){o.classList.remove('open');});
      document.querySelectorAll('.raised').forEach(function(o){o.classList.remove('raised');o.style.zIndex='';});
      if(!was){ btn.classList.add('open');
        var host = btn.closest('.area, .jz2');
        if(host){ host.classList.add('raised'); host.style.position='relative'; host.style.zIndex='60'; }
      }
    });
  });
  document.querySelectorAll('[data-fold]').forEach(function(b){
    b.addEventListener('click', function(){
      var open = b.parentElement.classList.toggle('open');
      b.setAttribute('aria-expanded', String(open));
    });
  });
  document.querySelectorAll('[data-toggle=quotes]').forEach(function(h){
    function toggle(){ var open = h.getAttribute('aria-expanded')==='true';
      h.setAttribute('aria-expanded', String(!open));
      var q = h.parentElement.querySelector('.quotes');
      q.style.maxHeight = open ? '0px' : (q.scrollHeight+4)+'px';
    }
    h.addEventListener('click', toggle);
    h.addEventListener('keydown', function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); toggle(); }});
  });
  // let quote links work without collapsing the panel
  document.querySelectorAll('a.q').forEach(function(a){
    a.addEventListener('click', function(ev){ ev.stopPropagation(); });
  });
  // the fallback for sandboxes that block target=_blank: copy, quietly
  document.querySelectorAll('.qcopy').forEach(function(b){
    b.addEventListener('click', function(ev){
      ev.stopPropagation(); ev.preventDefault();
      var url = b.dataset.url || '';
      function flash(){ b.classList.add('done'); b.setAttribute('title', b.dataset.done||'copied');
        setTimeout(function(){ b.classList.remove('done'); }, 1400); }
      if(navigator.clipboard && navigator.clipboard.writeText){
        navigator.clipboard.writeText(url).then(flash, function(){ prompt('', url); });
      } else { prompt('', url); }
    });
  });
  document.addEventListener('click', function(){ document.querySelectorAll('.info.open').forEach(function(o){o.classList.remove('open');}); });
  document.addEventListener('keydown', function(e){ if(e.key==='Escape'){ document.querySelectorAll('.info.open').forEach(function(o){o.classList.remove('open');}); }});
  if(document.readyState!=='loading') setTimeout(ready,60); else document.addEventListener('DOMContentLoaded', function(){setTimeout(ready,60);});
})();
"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    lax = "--lax" in sys.argv
    if len(args) < 2:
        print("usage: generate_snapshot.py snapshot.json out.html [--lax]", file=sys.stderr)
        sys.exit(1)
    sys.argv = [sys.argv[0]] + args
    data = json.load(open(sys.argv[1], encoding="utf-8"))

    errors, warns = validate(data, lax)
    for w in warns:
        print(f"  warn: {w}", file=sys.stderr)
    for e in errors:
        print(f" ERROR: {e}", file=sys.stderr)
    if errors and not lax:
        print(f"\n{len(errors)} safeguard violation(s). Fix the JSON, or re-run with --lax "
              f"if you know what you're doing.", file=sys.stderr)
        sys.exit(2)
    lang = data.get("lang", "en")
    tr = T.get(lang, T["en"])
    areas = data["areas"]

    scores = [float(a["score"]) for a in areas if a.get("score") is not None]
    composite = sum(scores) / len(scores) if scores else None
    stage, cap_reason = overall_stage(areas)

    if data.get("statement"):
        statement = data["statement"]
    elif stage is not None:
        statement = tr["statements"][stage]
    else:
        statement = tr["statement_none"]

    cap_html = ""
    if cap_reason and stage != "transformative":
        cap_html = f'<p class="cap">{escape(tr["caps"][cap_reason])}</p>' 

    conf = str(data.get("confidence", "low")).lower()
    if conf not in ("low", "med", "high"):
        conf = "low"
    # This block used to be grey fine print, which is the wrong register: it is
    # the part that says what the assessment is and how far it can be trusted,
    # so it reads as a statement in its own box rather than as a disclaimer
    # someone hoped you would skip.
    basis = data.get("basis", "")
    blind = [str(a.get("label", "")).strip() for a in areas if a.get("score") is None]
    blind = [b[0].lower() + b[1:] if b else b for b in blind]
    if len(blind) > 1:
        joined = ", ".join(blind[:-1]) + (" og " if lang == "da" else " and ") + blind[-1]
    else:
        joined = blind[0] if blind else ""
    not_seen = tr["not_seen"].format(areas=joined) if joined else ""

    # The confidence is the one line here that changes how the whole card should
    # be read, so it stays on the surface and doubles as the toggle. Everything
    # under it is detail about where the reading came from.
    #
    # The explanation of the confidence level moves into the body rather than a
    # popover: it is the natural first thing to say once the box is open, and it
    # avoids putting a button inside a button.
    about = (
        f'<div class="about fold">'
        f'<button class="about-h" aria-expanded="false" data-fold>'
        f'<span class="about-conf">{escape(tr["conf_label"])}: '
        f'<span class="conf-v conf-{conf}">{escape(tr["conf"][conf])}</span></span>'
        f'<span class="chev" aria-hidden="true"></span>'
        f'</button>'
        f'<div class="fold-b">'
        f'<p class="about-line">{escape(tr["conf_info"][conf])}</p>'
        + (f'<p class="about-line">{escape(tr["basis_label"])}: {escape(basis)}.</p>' if basis else "")
        + (f'<p class="about-line">{escape(not_seen)}</p>' if not_seen else "")
        + f'<p class="about-line">{escape(tr["limit_note"])}</p>'
        f'</div></div>'
    )

    journey = build_journey(composite, tr, stage)
    area_html = "".join(build_area(a, tr, i) for i, a in enumerate(areas))
    # Not foldable. This is the evidence the three moves rest on; hiding it by
    # default would leave the moves looking like generic advice.
    areas_fold = (f'<div class="sec"><div class="sec-h">'
                  f'<span class="sec-t">{escape(tr["areas"])}</span>'
                  f'<span class="sec-n">{escape(tr["areas_hint"])}</span></div>{area_html}</div>')

    # Moves block. "straight_talk" is kept as an accepted key so older snapshots
    # still render, but it is no longer its own section with its own heading. A
    # heading that announces its own bluntness performs honesty instead of doing
    # it; the same paragraph does real work as the reason these three moves.
    moves = data.get("moves", []) or []
    why = (data.get("why") or data.get("straight_talk") or "").strip()
    moves_html = ""
    if moves:
        items = "".join(
            f'<div class="move"><span class="n">{i+1:02d}</span>'
            f'<span class="txt">{escape(m if isinstance(m, str) else m.get("text", ""))}</span></div>'
            for i, m in enumerate(moves)
        )
        why_html = (f'<div class="why"><div class="why-h">{escape(tr["why_h"])}</div>'
                    f'<p>{escape(why)}</p></div>') if why else ""
        moves_html = (f'<div class="moves"><div class="moves-h">{escape(tr["moves"])}</div>'
                      f'{items}{why_html}</div>')

    # A separate block of reflection questions asked the reader to do homework
    # on the one area the card knows least about. The honest version is a plain
    # statement of what could not be seen, in the box about the assessment.
    oq_html = ""

    ex = data.get("example")
    example = (ex.get("text", "") if isinstance(ex, dict) else (ex or "")).strip()
    example_html = f'<p class="example">{escape(example)}</p>' if example else ""
    person = escape(data.get("person", ""))
    date = escape(data.get("date", ""))

    page = f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(tr["eyebrow"])}</title><style>{CSS}</style></head>
<body>
<div class="card"><div class="stripe"></div><div class="pad">
  <div class="top">
    <span class="eyebrow">{tr["eyebrow"]}{(" &middot; " + person) if person else ""}</span>
    <span class="date">{date}</span>
  </div>

  <p class="statement">{escape(statement)}</p>
  {example_html}

  {moves_html}

  <div class="j-h">{escape(tr["journey"])}</div>
  {journey}
  {cap_html}

  {areas_fold}
  {about}
</div></div>
<script>{JS}</script>
</body></html>'''

    open(sys.argv[2], "w", encoding="utf-8").write(page)
    print("wrote", sys.argv[2])


if __name__ == "__main__":
    main()

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
        "straight_h": "Lige ud af posen",
        "open_h": "Det kunne kortet ikke se",
        "open_note": "Ingen anbefaling her \u2014 der er ikke noget at bygge den p\u00e5. Tag sp\u00f8rgsm\u00e5let med til en kollega i stedet.",
        "explain": "Forklar",
        "epigraph": "Formerne g\u00e5r igen i alt vidensarbejde \u2014 hvor du st\u00e5r, er din egen rejse.",
        "stages": {
            "assisted": ("Assisteret", "Du bruger AI til enkeltopgaver, n\u00e5r du kommer i tanke om det."),
            "integrated": ("Integreret", "AI er en fast del af flere af dine opgaver; du ved hvorn\u00e5r det hj\u00e6lper."),
            "transformative": ("Transformativ", "Du l\u00f8ser opgaver p\u00e5 nye m\u00e5der, fordi AI er der \u2014 ikke bare hurtigere, men anderledes."),
        },
        # the headline sentence — this replaces the old score block
        "statements": {
            "assisted": "Du anvender AI til at assistere dig i enkelte opgaver.",
            "integrated": "Du integrerer AI kontinuerligt i dit arbejde.",
            "transformative": "Du l\u00f8ser opgaver p\u00e5 nye m\u00e5der, fordi AI er en del af dem.",
        },
        "statement_none": "Der er endnu ikke nok at se p\u00e5 til at sige, hvordan du bruger AI.",
        "thin": "tyndt bel\u00e6g",
        "unseen": "ikke observeret",
        "unseen_note": "Intet i materialet viser det her \u2014 hverken godt eller skidt.",
        "basis_label": "Bygget p\u00e5",
        "conf_label": "sikkerhed i analysen",
        "caps": {
            "partial": "Ikke h\u00f8jere, fordi kortet ikke kunne se alle fire omr\u00e5der. Delvist billede, delvis konklusion.",
            "unchecked": "Ikke h\u00f8jere, fordi der er lidt der tyder p\u00e5, at du efterpr\u00f8ver svarene. Hurtigt er ikke det samme som godt.",
            "uneven": "Ikke h\u00f8jere, fordi ét omr\u00e5de tr\u00e6kker tydeligt ned. Kæden er ikke st\u00e6rkere end det svageste led.",
            "short": "Ikke h\u00f8jere endnu \u2014 der er stykke vej igen p\u00e5 tv\u00e6rs af omr\u00e5derne.",
        },
        "conf": {"low": "lav", "med": "middel", "high": "h\u00f8j"},
        "conf_info": {
            "low": "Bygget p\u00e5 f\u00e5 oplysninger \u2014 fx dine egne svar, ikke p\u00e5 hvordan du faktisk arbejder. Tag det som et udgangspunkt, ikke et facit.",
            "med": "Bygget p\u00e5 nogle f\u00e5 rigtige samtaler. Et rimeligt billede, men langtfra fuldt.",
            "high": "Bygget p\u00e5 mange, varierede samtaler \u2014 men stadig kun det, der kunne ses.",
        },
        "limit_note": "Den kan kun se det, der er her \u2014 ikke dit arbejde i andre v\u00e6rkt\u00f8jer eller det, du g\u00f8r uden AI. Brug det som et opl\u00e6g til samtale, ikke en m\u00e5ling.",
        "src": {"chat": "chat", "cc": "Claude Code", "cowork": "Cowork", "refleksion": "refleksion"},
        "src_hint": "\u00c5bn samtalen",
        "blocked": "Linket kan ikke \u00e5bnes herinde \u2014 kopi\u00e9r adressen:",
    },
    "en": {
        "eyebrow": "AI Assessment",
        "journey": "Your journey",
        "here": "you are here",
        "areas": "How you work with AI",
        "areas_hint": "Click a card to see your own words",
        "moves": "Your next moves",
        "straight_h": "Straight talk",
        "open_h": "What the card couldn't see",
        "open_note": "No recommendation here \u2014 there's nothing to base one on. Take the question to a colleague instead.",
        "explain": "Explain",
        "epigraph": "The shapes recur across all knowledge work \u2014 where you stand is your own.",
        "stages": {
            "assisted": ("Assisted", "You use AI for one-off tasks, when it occurs to you."),
            "integrated": ("Integrated", "AI is a fixed part of several of your tasks; you know when it helps."),
            "transformative": ("Transformative", "You solve tasks in new ways because AI is there \u2014 not just faster, but different."),
        },
        "statements": {
            "assisted": "You use AI to assist you on individual tasks.",
            "integrated": "You integrate AI continuously into your work.",
            "transformative": "You solve tasks in new ways because AI is part of them.",
        },
        "statement_none": "There isn't enough here yet to say how you use AI.",
        "thin": "thin evidence",
        "unseen": "not observed",
        "unseen_note": "Nothing in the material shows this \u2014 neither good nor bad.",
        "basis_label": "Built on",
        "conf_label": "confidence in analysis",
        "caps": {
            "partial": "No higher, because the card couldn't see all four areas. A partial picture earns a partial conclusion.",
            "unchecked": "No higher, because there's little sign you verify what you get back. Fast is not the same as good.",
            "uneven": "No higher, because one area is clearly dragging. The chain is only as strong as its weakest link.",
            "short": "Not yet \u2014 there's ground to cover across the areas.",
        },
        "conf": {"low": "low", "med": "medium", "high": "high"},
        "conf_info": {
            "low": "Built on little \u2014 e.g. your own answers, not how you actually work. Treat it as a starting point, not a fact.",
            "med": "Built on a handful of real conversations. A fair picture, but far from complete.",
            "high": "Built on many varied conversations \u2014 but still only what could be seen.",
        },
        "limit_note": "It can only see what's here \u2014 not your work in other tools or what you do without AI. Use it as a conversation starter, not a measurement.",
        "src": {"chat": "chat", "cc": "Claude Code", "cowork": "Cowork", "refleksion": "reflection"},
        "src_hint": "Open the conversation",
        "blocked": "This link can't open in here \u2014 copy the address:",
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
LINK_ICON = '<path d="M7 17 17 7"/><path d="M9 7h8v8"/>'


QUOTE_MAX = 150
VALID_IDS = ("delegation", "description", "discernment", "diligence")
VALID_SURFACES = ("chat", "cc", "cowork", "refleksion")


def word_trunc(text, limit=QUOTE_MAX):
    """Truncate at a word boundary, the only edit the skill permits on a quote."""
    if len(text) <= limit:
        return text
    cut = text[:limit - 1]
    if " " in cut:
        cut = cut[:cut.rfind(" ")]
    return cut.rstrip(" ,.;:-") + "\u2026"


def validate(data, lax=False):
    """Enforce the evidence safeguards in code, not just in prose.

    Returns (errors, warnings). Errors block generation unless --lax is passed,
    because a rule that only lives in the SKILL.md is the first thing to go when
    the model is under pressure to produce a nice-looking card.
    """
    errors, warns = [], []
    areas = data.get("areas") or []
    if not areas:
        errors.append("no areas in snapshot.json")

    scored = 0
    for i, a in enumerate(areas):
        where = f"area[{i}] {a.get('id') or a.get('label') or '?'}"
        if a.get("id") not in VALID_IDS:
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
        quotes = a.get("quotes") or []
        if s is not None and not quotes:
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
    if str(data.get("confidence", "")).lower() not in ("low", "med", "high"):
        warns.append(f"confidence {data.get('confidence')!r} not recognised — falling back to low")
    if not data.get("basis"):
        warns.append("no basis line — the card won't say what it was built on")
    moves = data.get("moves") or []
    unseen = [a.get("id") or a.get("label") or "?" for a in areas if a.get("score") is None]
    seen = [a.get("id") for a in areas if a.get("score") is not None]
    if not moves:
        warns.append("no next moves — the card is a diagnosis with no action")
    if len(moves) > scored:
        errors.append(
            f"{len(moves)} next moves but only {scored} area(s) with evidence. "
            f"Every move must point at something you actually saw. Drop the extra move, "
            f"or put it under open_questions.")
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
    if unseen and not (data.get("open_questions") or []):
        warns.append(
            f"not observed: {', '.join(unseen)} — consider an open_questions entry so the gap "
            f"is named as a question rather than quietly ignored")
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


def build_quote(q, tr):
    """Accepts a plain string or {text, url, surface}. Links back to origin when a url is given."""
    if isinstance(q, str):
        q = {"text": q}
    text = escape(q.get("text", ""))
    surface = q.get("surface", "")
    label = tr["src"].get(surface, surface)
    url = safe_url(q.get("url", ""))
    tag = f'<span class="qsrc">{escape(label)}</span>' if label else ""
    if url:
        return (f'<li><a class="q" href="{escape(url, quote=True)}" target="_blank" rel="noopener" '
                f'title="{escape(tr["src_hint"], quote=True)}">&ldquo;{text}&rdquo;'
                f'<span class="qmeta">{tag}<svg viewBox="0 0 24 24" class="qlink" aria-hidden="true">{LINK_ICON}</svg></span></a>'
                f'<span class="qfall">{escape(tr["blocked"])}<br>{escape(url)}</span></li>')
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
    if not q_html:
        q_html = f'<li class="qnone">{escape(tr["unseen_note"] if not observed else tr["thin"])}</li>'
    thin_html = f'<span class="thin">{tr["thin"]}</span>' if a.get("thin") and observed else ""
    info = escape(a.get("info", ""), quote=True)
    delay = 0.15 + idx * 0.08
    pill = tr["stages"][sk][0] if observed else tr["unseen"]
    pill_cls = "stagepill" if observed else "stagepill unseen"
    bar = (f'<div class="bar"><span class="bar-fill" data-w="{pos(score):.1f}"></span>'
           f'<span class="bar-dot" data-x="{pos(score):.1f}"></span></div>') if observed else \
          '<div class="bar bar-empty"></div>'
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
  max-width:30ch;opacity:0;transform:translateY(6px)}
body.in .statement{animation:fadeup .6s ease forwards .15s}
.example{font-size:13.5px;line-height:1.55;color:var(--muted);margin:10px 0 0;max-width:52ch;
  padding-left:12px;border-left:2px solid var(--coral-soft);opacity:0}
body.in .example{animation:fadeup .6s ease forwards .3s}
.cap{margin:12px 0 0;font-size:12.5px;line-height:1.55;color:var(--ink);max-width:52ch;
  padding-left:12px;border-left:2px solid var(--coral);opacity:.85}
.meta-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:14px}
.conf{display:inline-flex;align-items:center;gap:2px;font-size:11px;font-weight:600;
  border:1px solid var(--border);border-radius:999px;padding:1px 3px 1px 9px;color:var(--muted)}
.conf.med{border-color:rgba(216,119,86,.5);color:var(--coral)}
.conf.high{background:var(--coral);border-color:var(--coral);color:#fff}
.conf .info{width:18px;height:18px}
.conf .info svg{width:13px;height:13px}
.conf.high .info{color:#fff}

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
.stage-unseen .ico{background:var(--border-soft);color:var(--muted)}
.ico svg{width:17px;height:17px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.area-main{flex:1;min-width:0}
.area-label{display:block;font-size:14px;font-weight:600}
.thin{display:inline-block;font-size:9px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  color:var(--coral);margin-left:8px;vertical-align:middle}
.area-summary{display:block;font-size:12.5px;color:var(--muted);margin-top:2px;line-height:1.4}
.area-right{display:flex;align-items:center;gap:8px;flex:none}
.stagepill{font-size:11px;color:var(--muted);white-space:nowrap}
.stagepill.unseen{font-style:italic;opacity:.75}
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
.area-head:has(.info.open),.jz2:has(.info.open),.conf:has(.info.open){position:relative;z-index:60}
.chev{width:9px;height:9px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);
  transform:rotate(45deg);transition:transform .2s;margin-left:2px}
.area-head[aria-expanded=true] .chev{transform:rotate(225deg)}
.bar{position:relative;height:8px;margin:0 0 2px}
.bar::before{content:"";position:absolute;inset:0;background:var(--track);border-radius:999px}
.bar-empty::before{background:repeating-linear-gradient(90deg,var(--track) 0 6px,transparent 6px 11px)}
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
.qfall{display:none;margin-top:6px;font-size:11px;color:var(--muted);word-break:break-all;
  background:var(--border-soft);border-radius:6px;padding:5px 7px;line-height:1.4}
li.blocked .qfall{display:block}
.jz2{position:relative}
.conf{position:relative}

/* straight talk */
.straight{margin-top:34px;padding:16px 18px;background:var(--coral-soft);border-radius:12px}
.straight-h{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--coral);margin-bottom:6px}
.straight p{margin:0;font-size:13.5px;line-height:1.6}

/* moves */
.moves-h{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--coral);margin:34px 0 4px}
.move{display:flex;gap:12px;padding:11px 0;border-top:1px solid var(--border-soft)}
.move:first-of-type{border-top:none}
.move .n{font-size:12px;font-weight:700;color:var(--coral);width:20px;flex:none;padding-top:2px}
.move .txt{font-size:13.5px;line-height:1.5}

/* open questions — a named gap, deliberately not advice */
.openq{margin-top:26px;padding:14px 16px;border:1px dashed var(--border);border-radius:12px}
.openq-h{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.openq ul{margin:0;padding-left:18px}
.openq li{font-size:13.5px;line-height:1.55;margin-bottom:4px}
.openq-note{margin:8px 0 0;font-size:11.5px;color:var(--muted);line-height:1.5}

/* footer */
.foot{margin-top:28px;padding-top:18px;border-top:1px solid var(--border)}
.epigraph{font-size:14px;line-height:1.5;max-width:520px}
.note{font-size:11.5px;color:var(--muted);margin-top:8px;line-height:1.5}

@media (max-width:540px){.pad{padding:26px 20px}.statement{font-size:21px}.area-summary{display:none}.stagepill{display:none}}
@media (prefers-reduced-motion:reduce){
  .card,.jpath,.jmarker,.area,.bar-fill,.bar-dot,.statement,.example{animation:none!important;transition:none!important}
  .card{opacity:1;transform:none}.jpath{stroke-dashoffset:0}.jmarker{opacity:1}
  .area,.statement,.example{opacity:1;transform:none}
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
        var host = btn.closest('.area, .jz2, .conf');
        if(host){ host.classList.add('raised'); host.style.position='relative'; host.style.zIndex='60'; }
      }
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
  // Sandboxed previews block target=_blank. Try to open; if blocked, reveal the raw URL.
  document.querySelectorAll('a.q').forEach(function(a){
    a.addEventListener('click', function(ev){
      ev.stopPropagation();
      var w = null;
      try { w = window.open(a.href, '_blank', 'noopener'); } catch(e) { w = null; }
      if(!w){ ev.preventDefault(); a.parentElement.classList.add('blocked'); }
      else { ev.preventDefault(); }
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
    conf_chip = (
        f'<span class="conf {conf}"><span>{tr["conf_label"]}: {escape(tr["conf"][conf])}</span>'
        f'<button class="info" aria-label="{tr["explain"]}" data-info="{escape(tr["conf_info"][conf], quote=True)}">'
        f'<svg viewBox="0 0 24 24">{INFO_ICON}</svg></button></span>'
    )
    basis = data.get("basis", "")
    basis_line = (f'{tr["basis_label"]}: {escape(basis)}. ' if basis else "") + escape(tr["limit_note"])

    journey = build_journey(composite, tr, stage)
    area_html = "".join(build_area(a, tr, i) for i, a in enumerate(areas))
    moves = data.get("moves", []) or []
    moves_html = ""
    if moves:
        moves_html = f'<div class="moves-h">{escape(tr["moves"])}</div>' + "".join(
            f'<div class="move"><span class="n">{i+1:02d}</span>'
            f'<span class="txt">{escape(m if isinstance(m, str) else m.get("text", ""))}</span></div>'
            for i, m in enumerate(moves)
        )
    oq = data.get("open_questions") or []
    oq_html = ""
    if oq:
        items = "".join(f'<li>{escape(q)}</li>' for q in oq)
        oq_html = (f'<div class="openq"><div class="openq-h">{escape(tr["open_h"])}</div>'
                   f'<ul>{items}</ul><p class="openq-note">{escape(tr["open_note"])}</p></div>')

    straight = data.get("straight_talk", "")
    straight_html = (f'<div class="straight"><div class="straight-h">{escape(tr["straight_h"])}</div>'
                     f'<p>{escape(straight)}</p></div>') if straight else ""
    example = data.get("example", "")
    example_html = f'<p class="example">{escape(example)}</p>' if example else ""
    epigraph = escape(data.get("epigraph") or tr["epigraph"])
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
  {cap_html}
  <div class="meta-row">{conf_chip}</div>

  <div class="j-h">{escape(tr["journey"])}</div>
  {journey}

  <div class="sec-h"><span class="t">{escape(tr["areas"])}</span><span class="hint">{escape(tr["areas_hint"])}</span></div>
  {area_html}

  {straight_html}

  {moves_html}
  {oq_html}

  <div class="foot">
    <div class="epigraph">{epigraph}</div>
    <div class="note">{basis_line}</div>
  </div>
</div></div>
<script>{JS}</script>
</body></html>'''

    open(sys.argv[2], "w", encoding="utf-8").write(page)
    print("wrote", sys.argv[2])


if __name__ == "__main__":
    main()

"""Render the static site into the configured output directory."""
from __future__ import annotations

import datetime as dt
import html
import json
import shutil
import sys

import markdown as md_lib
from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import content as c
from . import validate as validate_mod

RENDER_DIR = c.ROOT / "tools" / "render"

DATE_LABELS = [("rfi", "RFI"), ("draft_rfp", "Draft RFP"),
               ("final_rfp", "Final RFP"), ("proposal_due", "Proposal due"),
               ("award_est", "Award (est.)")]


def md_to_html(text: str) -> str:
    cleaned = c.COMMENT_RE.sub("", text or "").strip()
    if not cleaned:
        return ""
    return md_lib.markdown(cleaned, extensions=["tables"])


def rollup_html(data: dict) -> str:
    tally = data["tally"]
    if not tally["pursuits"]:
        return "<p class=\"subtle\">No recorded pursuits against this competitor yet.</p>"
    parts = [f"we won {tally['we_won']}", f"we lost {tally['we_lost']}"]
    if tally["observed"]:
        parts.append(f"{tally['observed']} observed (no-bid)")
    out = [f"<p><strong>Head-to-head: {tally['pursuits']} pursuits</strong> — "
           f"{', '.join(parts)}.</p>",
           "<table><thead><tr><th>Year</th><th>Opportunity</th><th>Agency</th>"
           "<th>Value</th><th>Outcome</th><th>Their role</th><th>Winner</th>"
           "</tr></thead><tbody>"]
    for row in data["rows"]:
        outcome = {"win": "we won", "loss": "we lost"}.get(row["outcome"],
                                                           row["outcome"])
        out.append(
            "<tr>"
            f"<td>{row['year']}</td>"
            f"<td>{html.escape(str(row['opportunity']))}</td>"
            f"<td>{html.escape(str(row['agency']))}</td>"
            f"<td>{html.escape(str(row['value']))}</td>"
            f"<td>{html.escape(outcome)}</td>"
            f"<td>{html.escape(str(row['their_role']))}</td>"
            f"<td>{html.escape(str(row['winner']))}{' (them)' if row['they_won'] else ''}</td>"
            "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def _card_sections(card, config, records, mode: str):
    """Ordered (name, html) pairs for a render mode: full, call, share-safe."""
    if mode == "call":
        names = [n for n in c.CALL_VIEW_SECTIONS if n in card.sections]
    elif mode == "share-safe":
        omit = set(config.settings.get("share_safe_omit") or [])
        names = [n for n in c.CARD_SECTIONS if n in card.sections and n not in omit]
    else:
        names = [n for n in c.CARD_SECTIONS if n in card.sections]

    pairs = []
    for name in names:
        body = md_to_html(card.sections[name])
        if name == "Win/Loss vs Us" and mode == "full":
            body = rollup_html(c.rollup(records, card.slug)) + body
        if not body:
            if mode != "full":
                continue  # call/share-safe views skip empty sections
            body = "<p class=\"mini\">(not yet written)</p>"
        pairs.append((name, body))
    return pairs


def _write(env, template, out_path, **ctx):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(env.get_template(template).render(**ctx),
                        encoding="utf-8")


def build(quiet: bool = False) -> None:
    config = c.load_config()
    errors, _ = validate_mod.run(config)
    if errors:
        for err in errors:
            print(f"ERROR {err}", file=sys.stderr)
        raise SystemExit(f"build aborted: {len(errors)} validation error(s)")

    cards = c.load_cards()
    opps = c.load_opportunities()
    records = c.load_winloss()
    today = dt.date.today()
    settings = config.settings

    env = Environment(loader=FileSystemLoader(RENDER_DIR),
                      autoescape=select_autoescape(["html"]))
    out = config.output_dir
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / ".nojekyll").touch()
    shutil.copytree(RENDER_DIR / "assets", out / "assets")

    base = dict(settings=settings, banner=settings["banner"], built=str(today))

    # Card pages: full, call view, share-safe
    index_rows = []
    for card in cards:
        stale = card.is_stale(config, today)
        common = dict(base, card=card, stale=stale,
                      age_days=card.days_since_review(today),
                      staleness_days=card.staleness_days(config),
                      tier_label=(config.tiers.get(card.tier) or {}).get("label", ""),
                      root="..")
        _write(env, "card.html", out / "cards" / f"{card.slug}.html",
               title=card.name, active="library", share_safe=False,
               sections=_card_sections(card, config, records, "full"), **common)
        _write(env, "call.html", out / "cards" / f"{card.slug}-call.html",
               title=f"{card.name} (call view)", active="library",
               page_class="call",
               sections=_card_sections(card, config, records, "call"), **common)
        _write(env, "card.html", out / "share-safe" / f"{card.slug}.html",
               title=f"{card.name} (share-safe)", share_safe=True,
               standalone=True,
               sections=_card_sections(card, config, records, "share-safe"),
               **dict(common, banner=settings["share_safe_banner"]))

        index_rows.append({
            "slug": card.slug, "name": card.name, "tier": card.tier,
            "status": card.status, "stale": stale,
            "age_days": card.days_since_review(today),
            "relationship": card.meta.get("relationship", ""),
            "markets": card.meta.get("markets") or [],
            "agencies": card.meta.get("agencies") or [],
            "vehicles": card.meta.get("vehicles") or [],
            "owner": card.meta.get("owner", ""),
            "example": bool(card.meta.get("example")),
            "last_reviewed": str(card.meta.get("last_reviewed") or ""),
            "search": card.searchable_text(),
        })

    data_json = json.dumps(index_rows).replace("</", "<\\/")
    _write(env, "index.html", out / "index.html", title="Library",
           active="library", root=".", cards=cards,
           tiers=sorted(config.tiers), data_json=data_json, **base)
    (out / "data").mkdir(exist_ok=True)
    (out / "data" / "index.json").write_text(json.dumps(index_rows, indent=1),
                                             encoding="utf-8")

    # Opportunity pages
    card_by_slug = {card.slug: card for card in cards}
    for opp in opps:
        competitors = []
        for entry in opp.competitors:
            linked = card_by_slug.get(entry.get("card"))
            factors = [{"label": config.threat_factors[key]["label"],
                        "score": score}
                       for key, score in (entry.get("factors") or {}).items()
                       if key in config.threat_factors]
            competitors.append({
                "card": entry.get("card") if linked else None,
                "display": linked.name if linked else entry.get("name", "?"),
                "role": entry.get("role", ""), "threat": entry.get("threat", ""),
                "factors": factors, "rationale": entry.get("rationale", ""),
            })
        incumbent_card = card_by_slug.get(opp.meta.get("incumbent_card"))
        dates = [(label, str(value)) for key, label in DATE_LABELS
                 if (value := (opp.meta.get("dates") or {}).get(key))]
        sections = [(n, md_to_html(opp.sections[n]))
                    for n in c.ASSESSMENT_SECTIONS if n in opp.sections
                    if md_to_html(opp.sections[n])]
        _write(env, "opportunity.html",
               out / "opportunities" / f"{opp.slug}.html",
               title=opp.title, active="opportunities", root="..", opp=opp,
               competitors=competitors, dates=dates, sections=sections,
               incumbent=(incumbent_card.name if incumbent_card
                          else opp.meta.get("incumbent") or ""), **base)

    _write(env, "opportunities.html", out / "opportunities.html",
           title="Opportunities", active="opportunities", root=".",
           opps=opps, **base)

    # Dashboard
    active = {"tracking", "pursuing", "submitted"}
    stats = {
        "total": len(cards),
        "approved": sum(1 for x in cards if x.status == "approved"),
        "pending": sum(1 for x in cards if x.status != "approved"),
        "stale": sum(1 for x in cards if x.is_stale(config, today)),
        "active_opps": sum(1 for o in opps if o.meta.get("status") in active),
        "wins": sum(1 for r in records if r.outcome == "win"),
        "losses": sum(1 for r in records if r.outcome == "loss"),
    }

    h2h = []
    for card in cards:
        tally = c.rollup(records, card.slug)["tally"]
        if tally["pursuits"]:
            h2h.append({"slug": card.slug, "name": card.name,
                        "won": tally["we_won"], "lost": tally["we_lost"],
                        "observed": tally["observed"]})
    peak = max((max(r["won"], r["lost"]) for r in h2h), default=1) or 1
    for row in h2h:
        row["won_pct"] = round(row["won"] / peak * 100, 1)
        row["lost_pct"] = round(row["lost"] / peak * 100, 1)
    h2h.sort(key=lambda r: r["won"] + r["lost"] + r["observed"], reverse=True)

    tiers = sorted(config.tiers)
    matrix = []
    for market in config.taxonomy["markets"]:
        counts = [sum(1 for x in cards if x.tier == t
                      and market in (x.meta.get("markets") or []))
                  for t in tiers]
        if sum(counts):
            matrix.append({"market": market, "counts": counts,
                           "total": sum(counts)})

    attention = []
    for card in cards:
        issues = []
        if card.is_stale(config, today):
            issues.append(f"stale — {card.days_since_review(today)}d since "
                          f"review (limit {card.staleness_days(config)}d)")
        if card.status != "approved":
            issues.append("not yet approved")
        if issues:
            attention.append({"slug": card.slug, "name": card.name,
                              "tier": card.tier, "status": card.status,
                              "issue": "; ".join(issues)})

    _write(env, "dashboard.html", out / "dashboard.html", title="Dashboard",
           active="dashboard", root=".", stats=stats, h2h=h2h, tiers=tiers,
           matrix=matrix, attention=attention, **base)

    if not quiet:
        print(f"built {out.relative_to(c.ROOT)}: {len(cards)} cards, "
              f"{len(opps)} assessments, {len(records)} win/loss records")

"""Validate library content: schema, vocab, completeness, cross-links."""
from __future__ import annotations

import datetime as dt
import re

from . import content as c

CARD_REQUIRED_META = ["id", "name", "slug", "tier", "status", "relationship",
                      "owner", "last_reviewed"]
OPP_REQUIRED_META = ["id", "title", "slug", "agency", "our_role", "status"]
WL_REQUIRED = ["id", "opportunity", "agency", "award_date", "outcome"]


def run(config=None):
    """Return (errors, warnings) across the whole library."""
    config = config or c.load_config()
    errors: list[str] = []
    warnings: list[str] = []

    try:
        cards = c.load_cards()
        opps = c.load_opportunities()
        records = c.load_winloss()
    except c.ContentError as exc:
        return [str(exc)], warnings

    card_slugs = {card.slug for card in cards}
    for card in cards:
        _check_card(card, config, errors)
    for opp in opps:
        _check_opportunity(opp, config, card_slugs, errors)
    opp_slugs = {o.slug for o in opps}
    for rec in records:
        _check_winloss(rec, config, card_slugs, opp_slugs, errors)
    return errors, warnings


def _err(errors, path, msg):
    errors.append(f"{path.relative_to(c.ROOT)}: {msg}")


def _vocab_check(errors, path, meta, key, allowed, label):
    for value in meta.get(key) or []:
        if value not in allowed:
            _err(errors, path, f"{label} '{value}' not in config/taxonomy.yaml "
                               f"({key}) — add it there first")


def _check_card(card, config, errors):
    meta, path, tax = card.meta, card.path, config.taxonomy

    for field in CARD_REQUIRED_META:
        if meta.get(field) in (None, ""):
            _err(errors, path, f"missing required frontmatter field '{field}'")
    if meta.get("slug") and meta["slug"] != card.slug:
        _err(errors, path, f"slug '{meta['slug']}' does not match folder "
                           f"'{card.slug}'")
    if meta.get("id") and meta.get("slug") and meta["id"] != meta["slug"]:
        _err(errors, path, "id must equal slug")
    if not c.SLUG_RE.match(card.slug):
        _err(errors, path, f"folder name '{card.slug}' is not a valid slug")
    if card.tier not in config.tiers:
        _err(errors, path, f"tier '{card.tier}' not defined in config/tiers.yaml")
    if card.status and card.status not in tax["statuses"]:
        _err(errors, path, f"status '{card.status}' not one of {tax['statuses']} "
                           "(stale is computed, never stored)")
    if meta.get("relationship") not in tax["relationships"]:
        _err(errors, path, f"relationship '{meta.get('relationship')}' not one "
                           f"of {tax['relationships']}")
    if meta.get("size") and meta["size"] not in tax["sizes"]:
        _err(errors, path, f"size '{meta['size']}' not one of {tax['sizes']}")

    _vocab_check(errors, path, meta, "markets", tax["markets"], "market")
    _vocab_check(errors, path, meta, "agencies", tax["agencies"], "agency")
    _vocab_check(errors, path, meta, "vehicles", tax["vehicles"], "vehicle")
    _vocab_check(errors, path, meta, "set_asides", tax["set_asides"], "set-aside")

    reviewed = card.last_reviewed
    if meta.get("last_reviewed") and reviewed is None:
        _err(errors, path, "last_reviewed is not a valid date (YYYY-MM-DD)")
    elif reviewed and reviewed > dt.date.today():
        _err(errors, path, "last_reviewed is in the future")

    # Section structure
    seen = set()
    for heading in card.heading_order:
        if heading not in c.CARD_SECTIONS:
            _err(errors, path, f"unknown section '## {heading}' — use the "
                               "canonical headings from templates/card.md")
        if heading in seen:
            _err(errors, path, f"duplicate section '## {heading}'")
        seen.add(heading)

    # Approval gate: tier completeness + approval metadata
    if card.status == "approved":
        for field in ("approved_by", "approved_date"):
            if meta.get(field) in (None, ""):
                _err(errors, path, f"approved card missing '{field}'")
        tier_def = config.tiers.get(card.tier)
        if tier_def:
            for section in tier_def["required_sections"]:
                if section not in card.sections:
                    _err(errors, path, f"approved Tier {card.tier} card missing "
                                       f"required section '## {section}'")
                elif (section not in config.content_optional
                      and not c.visible_text(card.sections[section])):
                    _err(errors, path, f"approved Tier {card.tier} card has "
                                       f"empty required section '## {section}'")

    # Evidence structure: sources, citations, W/PP blocks, ghost entries
    source_ids = set(c.SOURCE_ID_RE.findall(card.sections.get("Sources", "")))
    weakness_ids, pp_ids = set(), set()
    for prefix, section, bucket in (("W", "Weaknesses", weakness_ids),
                                    ("PP", "Intel & Proof Points", pp_ids)):
        for block_id, title, body in c.split_blocks(card.sections.get(section, "")):
            if not re.fullmatch(rf"{prefix}\d+", block_id):
                _err(errors, path, f"'{section}' block '{block_id}' must be "
                                   f"named {prefix}1, {prefix}2, ...")
                continue
            if block_id in bucket:
                _err(errors, path, f"duplicate {section} block id '{block_id}'")
            bucket.add(block_id)
            if not c.CITATION_RE.search(body):
                _err(errors, path, f"{block_id} ('{title}') cites no source "
                                   "[S#] — every fact needs a citation")

    for section_name, text in card.sections.items():
        for sid in c.CITATION_RE.findall(text):
            if sid not in source_ids:
                _err(errors, path, f"'{section_name}' cites [S{sid}] but "
                                   "Sources has no such entry")

    tokens = c.name_tokens(card)
    for entry in c.parse_ghost_entries(card.sections.get("Ghosting Library", "")):
        gid = entry["id"]
        if not entry["ghost"]:
            _err(errors, path, f"ghost entry {gid} has no 'Ghost:' line")
        if entry["targets"] not in weakness_ids:
            _err(errors, path, f"ghost entry {gid} targets "
                               f"'{entry['targets'] or '(nothing)'}' — must "
                               "reference an existing W# block")
        if entry["proof"] not in pp_ids:
            _err(errors, path, f"ghost entry {gid} proof "
                               f"'{entry['proof'] or '(nothing)'}' — must "
                               "reference an existing PP# block")
        ghost_lower = entry["ghost"].lower()
        for token in tokens:
            if token in ghost_lower:
                _err(errors, path, f"ghost entry {gid} names the competitor "
                                   f"('{token}') — ghost text must never "
                                   "identify them")


def _check_opportunity(opp, config, card_slugs, errors):
    meta, path, tax = opp.meta, opp.path, config.taxonomy

    for field in OPP_REQUIRED_META:
        if meta.get(field) in (None, ""):
            _err(errors, path, f"missing required frontmatter field '{field}'")
    if meta.get("slug") and meta["slug"] != opp.slug:
        _err(errors, path, f"slug '{meta['slug']}' does not match filename "
                           f"'{opp.slug}'")
    if meta.get("agency") and meta["agency"] not in tax["agencies"]:
        _err(errors, path, f"agency '{meta['agency']}' not in taxonomy")
    if meta.get("vehicle") and meta["vehicle"] not in tax["vehicles"]:
        _err(errors, path, f"vehicle '{meta['vehicle']}' not in taxonomy")
    if meta.get("our_role") and meta["our_role"] not in tax["our_roles"]:
        _err(errors, path, f"our_role '{meta['our_role']}' not one of "
                           f"{tax['our_roles']}")
    if meta.get("status") and meta["status"] not in tax["pursuit_statuses"]:
        _err(errors, path, f"status '{meta['status']}' not one of "
                           f"{tax['pursuit_statuses']}")
    if meta.get("incumbent_card") and meta["incumbent_card"] not in card_slugs:
        _err(errors, path, f"incumbent_card '{meta['incumbent_card']}' has no "
                           "card folder")

    for heading in opp.heading_order:
        if heading not in c.ASSESSMENT_SECTIONS:
            _err(errors, path, f"unknown section '## {heading}' — use the "
                               "headings from templates/assessment.md")

    for i, entry in enumerate(opp.competitors, 1):
        label = f"competitors[{i}]"
        if not entry.get("card") and not entry.get("name"):
            _err(errors, path, f"{label} needs 'card' (slug) or 'name'")
        if entry.get("card") and entry["card"] not in card_slugs:
            _err(errors, path, f"{label} card '{entry['card']}' has no card "
                               "folder — create it or use 'name'")
        if entry.get("role") not in tax["competitor_roles"]:
            _err(errors, path, f"{label} role '{entry.get('role')}' not one of "
                               f"{tax['competitor_roles']}")
        if entry.get("threat") not in tax["threat_levels"]:
            _err(errors, path, f"{label} threat '{entry.get('threat')}' not one "
                               f"of {tax['threat_levels']}")
        if not entry.get("rationale"):
            _err(errors, path, f"{label} has no rationale — every rating needs "
                               "one")
        for factor, score in (entry.get("factors") or {}).items():
            if factor not in config.threat_factors:
                _err(errors, path, f"{label} unknown threat factor '{factor}' "
                                   "(see config/threat-factors.yaml)")
            if score not in config.threat_scores:
                _err(errors, path, f"{label} factor '{factor}' score '{score}' "
                                   f"not one of {config.threat_scores}")


def _check_winloss(rec, config, card_slugs, opp_slugs, errors):
    data, path, tax = rec.data, rec.path, config.taxonomy

    for field in WL_REQUIRED:
        if data.get(field) in (None, ""):
            _err(errors, path, f"missing required field '{field}'")
    if rec.outcome and rec.outcome not in tax["outcomes"]:
        _err(errors, path, f"outcome '{rec.outcome}' not one of {tax['outcomes']}")
    if data.get("agency") and data["agency"] not in tax["agencies"]:
        _err(errors, path, f"agency '{data['agency']}' not in taxonomy")
    if data.get("award_date") and rec.award_date is None:
        _err(errors, path, "award_date is not a valid date (YYYY-MM-DD)")
    if rec.outcome in ("win", "loss") and not data.get("our_role"):
        _err(errors, path, "our_role required when outcome is win/loss")
    if data.get("opportunity_slug") and data["opportunity_slug"] not in opp_slugs:
        _err(errors, path, f"opportunity_slug '{data['opportunity_slug']}' has "
                           "no assessment file")
    if not rec.winner.get("card") and not rec.winner.get("name"):
        _err(errors, path, "winner needs 'card' (slug) or 'name'")
    if rec.winner.get("card") and rec.winner["card"] not in card_slugs:
        _err(errors, path, f"winner card '{rec.winner['card']}' has no card "
                           "folder")
    for i, entry in enumerate(rec.competitors, 1):
        if not entry.get("card") and not entry.get("name"):
            _err(errors, path, f"competitors[{i}] needs 'card' or 'name'")
        if entry.get("card") and entry["card"] not in card_slugs:
            _err(errors, path, f"competitors[{i}] card '{entry['card']}' has "
                               "no card folder")

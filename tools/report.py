"""Library health report: staleness, pending reviews, completeness gaps."""
from __future__ import annotations

import datetime as dt

from . import content as c


def run() -> None:
    config = c.load_config()
    cards = c.load_cards()
    opps = c.load_opportunities()
    records = c.load_winloss()
    today = dt.date.today()

    print(f"Library health — {today}")
    print(f"  {len(cards)} cards · {len(opps)} assessments · "
          f"{len(records)} win/loss records\n")

    stale = [x for x in cards if x.is_stale(config, today)]
    print(f"STALE ({len(stale)})")
    for card in sorted(stale, key=lambda x: -(x.days_since_review(today) or 9999)):
        age = card.days_since_review(today)
        limit = card.staleness_days(config)
        age_s = f"{age}d since review" if age is not None else "never reviewed"
        print(f"  T{card.tier} {card.slug:30s} {age_s} (limit {limit}d) "
              f"— run /refresh {card.slug}")
    if not stale:
        print("  none")

    pending = [x for x in cards if x.status != "approved"]
    print(f"\nPENDING APPROVAL ({len(pending)})")
    for card in pending:
        print(f"  T{card.tier} {card.slug:30s} {card.status:10s} "
              f"owner: {card.meta.get('owner') or '—'}")
    if not pending:
        print("  none")

    print("\nCOMPLETENESS GAPS (required sections empty or missing)")
    gaps = False
    for card in cards:
        tier_def = config.tiers.get(card.tier)
        if not tier_def:
            continue
        missing = [s for s in tier_def["required_sections"]
                   if s not in config.content_optional
                   and not c.visible_text(card.sections.get(s, ""))]
        if missing:
            gaps = True
            print(f"  T{card.tier} {card.slug:30s} missing: {', '.join(missing)}")
    if not gaps:
        print("  none")

    active = [o for o in opps
              if o.meta.get("status") in ("tracking", "pursuing", "submitted")]
    print(f"\nACTIVE PURSUITS ({len(active)})")
    for opp in active:
        due = (opp.meta.get("dates") or {}).get("proposal_due") or "no due date"
        print(f"  {opp.slug:34s} {opp.meta.get('status'):10s} due: {due}")
    if not active:
        print("  none")

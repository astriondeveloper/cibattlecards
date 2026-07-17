---
name: refresh
description: Re-research a competitor on the web and propose card updates as a draft diff. Use for stale cards, or whenever asked to refresh or update a competitor.
---

# Refresh a competitor card

Argument: competitor slug or name, e.g. `/refresh meridian-federal`.
`python3 -m tools report` lists who needs this.

## Steps

1. Read the current card and its `sources/` notes; note `last_reviewed`.
2. Research what changed since that date: new awards and losses
   (USASpending/FPDS, SAM.gov), press and news, leadership changes,
   acquisitions, protest activity, vehicle wins.
3. Apply updates as a draft:
   - Facts: update or add `PP#` blocks and Recent Developments bullets,
     each with a new dated `[S#]` source.
   - If new evidence contradicts existing analysis (a weakness got fixed, a
     strength eroded), flag the conflict in your summary and propose the
     edit — do not silently rewrite approved positioning.
   - If the card was `approved`, set status back to `draft`.
4. Save a research note to `competitors/<slug>/sources/refresh-<yyyy-mm>.md`.
5. Do **not** bump `last_reviewed` — that happens when a human approves via
   `/review` (it records that a person verified currency).
6. Run `python3 -m tools validate`, then present a short diff summary:
   what changed, what's newly stale-relevant, what needs a human call.

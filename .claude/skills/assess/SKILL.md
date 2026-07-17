---
name: assess
description: Create or update a per-pursuit opportunity assessment with a scored competitor field (threat ratings, factor scores, rationale). Use for bid/no-bid prep, black hat setup, or "assess <opportunity>".
---

# Opportunity assessment

Argument: opportunity name or slug, plus anything known (agency, value,
dates, suspected bidders).

## Steps

1. Scaffold `opportunities/<slug>.md` from `templates/assessment.md` (or
   open the existing one to update).
2. Fill pursuit facts. Research the procurement itself on SAM.gov (notices,
   draft RFP attachments list, incumbent contract end dates) and cite what
   you find in the body text.
3. Build the competitor field:
   - Link each likely bidder with `card: <slug>`; for firms without cards,
     use `name:` or offer `/new-card`.
   - Score every factor in `config/threat-factors.yaml` high/medium/low,
     grounded in the competitor's card (incumbency footprint, vehicles,
     win/loss history vs us at this agency) plus pursuit-specific research.
   - Write a rationale for each rating: why this level, what would change it.
4. Draft the body sections: landscape, likely teaming, our positioning
   (reference specific W#/G# entries from the cards), black hat notes.
5. Run `python3 -m tools validate` and `python3 -m tools build`.
6. Summarize for the capture manager: the top threat, the teaming move that
   most changes the field, and the two or three discriminators to lead with.

Assessments are analysis, not cards — they have no approval workflow, but
threat ratings still need rationales (the validator enforces this).

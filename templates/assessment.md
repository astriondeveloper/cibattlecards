---
id: OPP-SLUG                 # same as slug
title: Opportunity Title
slug: opp-slug               # lowercase, hyphens; must match the filename
agency: usaf-aftc            # value from config/taxonomy.yaml
office: ""                   # buying office / directorate
vehicle: null                # taxonomy value, or null if standalone
naics: ""
value_est: ""                # e.g. "$120M ceiling, 5 yr"
dates:
  rfi: null
  draft_rfp: null
  final_rfp: null
  proposal_due: null
  award_est: null
incumbent: ""                # free text; also set incumbent_card if we have a card
incumbent_card: null         # competitor slug, validated if set
our_role: undecided          # prime | sub | undecided
capture_manager: ""
status: tracking             # tracking | pursuing | submitted | won | lost | no-bid
example: false
external_ids: {}             # reserved: {govwin: "...", crm: "..."}

# One entry per known/likely competitor. `card` links to competitors/<slug>/
# and is validated; use `name` alone for one-offs that don't merit a card.
competitors:
  - card: company-name
    role: prime              # prime | sub | teammate-candidate
    threat: high             # high | medium | low
    factors:                 # keys from config/threat-factors.yaml
      incumbency: high
      customer_intimacy: high
      vehicle_position: medium
      price_aggressiveness: medium
      past_performance_fit: high
    rationale: >-
      One paragraph: why this rating, what would change it.
---

## Competitive Landscape

<!-- The field as we understand it: who is really in, who is noise. -->

## Likely Teaming

<!-- Probable prime/sub arrangements, including JVs, and what they solve. -->

## Our Positioning

<!-- How we win this one: discriminators to lead with, ghosts to run. -->

## Black Hat Notes

<!-- Outputs of black hat sessions: their most likely solution, price
posture, and proposal strategy against us. -->

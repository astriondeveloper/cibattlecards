---
id: SLUG                     # same as slug; stable ID for cross-references
name: Company Name           # legal/common name, no suffixes like (EXAMPLE)
slug: company-name           # lowercase, hyphens; must match the folder name
aliases: []                  # former names, d/b/a, common abbreviations
tier: 3                      # 1 priority | 2 active | 3 watch (see config/tiers.yaml)
status: draft                # draft | in-review | approved (stale is computed, never stored)
relationship: competitor     # competitor | teammate | both
owner: ""                    # who maintains this card
last_reviewed: 2026-01-01    # bump whenever content is verified current
approved_by: null            # set by /review on approval
approved_date: null
example: false               # true only for fictional demo cards
markets: []                  # values from config/taxonomy.yaml
agencies: []                 # where they are entrenched (incumbency footprint)
vehicles: []                 # contract vehicles they hold
size: large                  # large | small
set_asides: []               # 8a, wosb, mentor-protege-jv, ...
parent: null                 # parent company, if any
jv_partners: []              # named JVs / mentor-protégé arrangements
hq: ""
revenue_est: ""              # e.g. "$450M (2025, est.)"
employees_est: ""
website: ""
external_ids: {}             # reserved: {govwin: "...", crm: "..."}
---

## Overview

<!-- Who they are, footprint, and strategy in 5–8 sentences. Where do we
actually collide with them? Required for every tier. -->

## Threat Summary

<!-- Where and how they hurt us most, in plain language a new hire gets in
30 seconds. Required for every tier. -->

## Their Discriminators

<!-- What genuinely differentiates them in the customer's eyes — not their
marketing claims, the real reasons customers pick them. -->

## Strengths

<!-- Honest list. Each bullet cites a source like [S1] where it rests on a
fact rather than team judgment. -->

## Weaknesses

<!-- One h3 block per weakness so ghosting entries can target it by ID.
Every block must cite at least one source [S#]. -->

### W1 — Short weakness title

Evidence and detail here. [S1]

## Our Counter-Positioning

<!-- How we position against each strength, and how we exploit each
weakness. Reference W# IDs where useful. -->

## Objection Handling

<!-- Customer pushback we actually hear, with the response that works. -->

- **They say:** "..." **We say:** "..."

## Trap-Setting Questions

<!-- Questions our team plants with the customer that expose a competitor
weakness without naming the competitor. -->

## Ghosting Library

<!-- Proposal-safe language. One h3 block per entry. Rules: never name the
competitor; every entry targets a W# and cites a PP#. -->

### G1 — Short ghost theme

- Ghost: "Offerors should describe how they will ..."
- Targets: W1
- Proof: PP1
- Used in: (optional — proposal/volume where this ran)

## Pricing Posture

<!-- Rate position, LPTA behavior, buy-in history, wrap-rate intel. -->

## Win/Loss vs Us

<!-- AUTO-GENERATED at build time from winloss/ records. Optional prose
below the marker adds context; leave empty otherwise. -->

## Intel & Proof Points

<!-- Cited, dated facts we can deploy: awards, protests, key departures,
recompete dates. One h3 block per proof point; each cites a source [S#]. -->

### PP1 — Short proof point title

Fact with date and citation. [S2]

## Recent Developments

<!-- Dated bullets, newest first. Refresh runs append here. -->

## Sources

<!-- Master citation list. Every factual claim above points here. -->

- [S1] Description — origin/URL (accessed 2026-01-01)
- [S2] Description — internal document, location (dated 2026-01-01)

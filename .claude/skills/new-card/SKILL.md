---
name: new-card
description: Create a new competitor battle card — web-research the company, scaffold from the template, draft content as status draft for human review. Use when asked to add a competitor to the library.
---

# New competitor card

Argument: competitor name, e.g. `/new-card Vantage Systems Group`. Optional
hints: tier, relationship, markets.

## Steps

1. Derive the slug (lowercase, hyphens). If `competitors/<slug>/` exists,
   stop and suggest `/refresh <slug>` instead.
2. Research the open web and record every source with URL and access date:
   company site and leadership pages, SAM.gov entity registration,
   USASpending/FPDS award history, GAO protest docket, recent news and press
   releases, LinkedIn-visible personnel moves. This is public-source
   collection only — nothing improper, nothing behind another company's NDA.
3. Copy `templates/card.md` to `competitors/<slug>/card.md`. Fill the
   frontmatter: `status: draft`, `last_reviewed:` today, tier (default 3
   unless told otherwise), relationship, taxonomy tags. If a market, agency,
   or vehicle value is missing from `config/taxonomy.yaml`, add it there
   first.
4. Draft every section you have evidence for. Rules:
   - Every factual claim cites `[S#]` resolving to the Sources section.
   - Weaknesses are `### W# — title` blocks, proof points `### PP# — title`,
     each citing at least one source.
   - Ghost entries need `Targets: W#` and `Proof: PP#` and must never name
     the competitor.
   - Where you lack evidence (pricing posture, objection handling), leave
     the section with a short note of what's needed rather than guessing.
5. Save the research notes to
   `competitors/<slug>/sources/<topic>-<yyyy-mm>.md`.
6. Run `python3 -m tools validate` and fix any errors.
7. Report: what's drafted, what needs human input (usually
   counter-positioning and pricing), and remind the owner to run
   `/review <slug>` when ready.

## Hard rules

Never set status beyond `draft`. Never fabricate win/loss history, pricing
intel, or customer sentiment. If research surfaces CUI or source-selection
material, stop and tell the user (see CLAUDE.md).

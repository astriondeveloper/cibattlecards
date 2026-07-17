# Battle Card Library — Operating Rules

This repo is Astrion's competitive intelligence battle card library for
federal capture/BD. Content is company competition-sensitive. These rules
bind every Claude session working in this repo.

## Layout

- `competitors/<slug>/card.md` — one battle card per competitor (frontmatter + 14 canonical `##` sections)
- `competitors/<slug>/sources/` — cached research notes backing the card's citations
- `opportunities/<slug>.md` — per-pursuit competitive assessments with threat ratings
- `winloss/<year>-<slug>.yaml` — structured win/loss records; roll up onto cards at build
- `intake/` — drop zone for source documents; `/ingest` processes and moves them to `intake/processed/`
- `config/` — taxonomy (controlled vocab), tiers (staleness + completeness), threat factors, settings (banners, share-safe list)
- `templates/` — authoring templates; always scaffold from these
- `tools/` — Python build layer; `docs/` — the committed built site
- `.claude/skills/` — the workflow commands (new-card, ingest, refresh, assess, winloss, review, ask, publish, status)

## Commands

```
python3 -m tools validate          # schema, vocab, completeness, link checks
python3 -m tools build             # validate + render static site into docs/
python3 -m tools report            # staleness, pending drafts, coverage gaps
python3 -m tools export pdf --all  # PDFs via headless Chromium (also: <slug>, --share-safe)
python3 -m tools export docx <slug> [--share-safe]
python3 -m tools export pack <slug>  # ghosting & discriminator pack (DOCX)
```

## Hard rules

1. **Draft-only authoring.** Content you write or update always lands with
   `status: draft`. Never set `in-review` or `approved`, and never fill
   `approved_by`/`approved_date` yourself — only `/review`, driven by a human
   decision, does that. No exceptions, including "small" edits to approved cards:
   editing an approved card resets its status to `draft`.
2. **Every factual claim cites a source.** Facts carry a `[S#]` reference
   resolving to the card's Sources section, with a date. Team judgment and
   analysis need no citation, but don't dress judgment up as fact.
3. **Ghosting discipline.** Ghost text never names a competitor (the
   validator enforces this). Every ghosting entry targets a weakness (`W#`)
   and cites a proof point (`PP#`).
4. **No CUI, ever.** This repo is not a CUI enclave. If intake material or
   research output appears to contain CUI, source-selection information, or
   another company's proprietary data obtained improperly, stop, do not copy
   it in, and tell the user what you found and where.
5. **Controlled vocabulary.** Tag values (markets, agencies, vehicles,
   set-asides) must exist in `config/taxonomy.yaml`. Add the vocab entry
   first if a new value is genuinely needed.
6. **Web research provenance.** When drafting from web research, record each
   source with URL and access date, both in the Sources section and as a note
   under `competitors/<slug>/sources/`.
7. **Validate before publishing.** `/publish` must run
   `python3 -m tools build` (which validates) and stop on any error.

## Conventions

- Slugs: lowercase, hyphens, `[a-z0-9-]`; folder and filename match the slug.
- Section headings are canonical — exact names, in template order. The parser
  and validator reject unknown headings.
- Weaknesses are `### W1 — title` blocks; proof points are `### PP1 — title`
  blocks; ghosting entries are `### G1 — theme` blocks with `Ghost:`,
  `Targets:`, `Proof:` lines.
- `Win/Loss vs Us` is auto-generated at build; only add prose beneath it,
  never hand-write the record table.
- Staleness is computed from `last_reviewed` + tier thresholds, never stored.
  Bump `last_reviewed` only when content was actually verified current.
- Seed/demo content carries `example: true` and fictional company names.

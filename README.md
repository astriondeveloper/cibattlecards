# Battle Card Library

Astrion's competitive intelligence battle card library for federal
capture/BD: one evergreen card per competitor, per-pursuit opportunity
assessments with scored threat ratings, and structured win/loss records that
roll up into head-to-head history — all validated, versioned in git, and
rendered to a static site plus PDF/DOCX exports.

**All content is company competition-sensitive.** Every rendered output
carries the marking banner from `config/settings.yaml`. The library must
never contain CUI or source-selection information.

## For consumers (read the cards)

Pull the repo and open **`docs/index.html`** in a browser. No server, no
install.

- **Library** — filter by market, agency, vehicle, tier, status, staleness;
  keyword search across all card content.
- **Card** — the full battle card. **Call view** — one-screen quick
  reference for live conversations. **Share-safe** — sanitized edition with
  counter-positioning, objections, traps, ghosting, pricing, and win/loss
  omitted (safe for teaming partners).
- **Opportunities** — pursuit assessments with the scored competitor field.
- **Dashboard** — portfolio health: coverage, staleness, head-to-head record.

Trust signals on every card: status (`draft` means unvetted), a red stale
flag when a card is past its review window, and `EXAMPLE` on fictional demo
content.

## For the CI owner (run the library)

Setup once: `pip install -r requirements.txt` (PDF export also needs any
Chromium/Chrome, or set `CHROME_BIN`).

The workflow runs through Claude Code skills in this repo:

| Command | What it does |
|---|---|
| `/new-card <name>` | Research + scaffold + draft a new competitor card |
| `/ingest` | Turn files dropped in `intake/` into draft card updates with provenance |
| `/refresh <slug>` | Re-research a competitor, propose updates as a draft diff |
| `/assess <opportunity>` | Build a pursuit assessment with threat ratings |
| `/winloss` | Record an outcome; rollups update automatically |
| `/review <slug>` | Guided human approval — the only path to `approved` |
| `/ask <question>` | Q&A across the library with citations |
| `/publish` | Validate, rebuild `docs/`, commit |
| `/status` | Staleness, pending approvals, gaps, next actions |

CLI equivalents: `python3 -m tools validate | build | report | export ...`

**The trust model in one paragraph:** Claude drafts, humans approve.
Anything Claude writes lands as `draft`. Every factual claim carries a
dated `[S#]` citation. Ghost language never names a competitor and must
link a weakness (`W#`) and a proof point (`PP#`) — the validator enforces
all of this and the build refuses to ship violations. Approval (`/review`)
records who and when, and staleness is computed from `last_reviewed`
against per-tier windows: Tier 1 — 90 days, Tier 2 — 180, Tier 3 — 365.

## Repo map

```
competitors/<slug>/card.md    the cards (frontmatter + 14 canonical sections)
opportunities/<slug>.md       pursuit assessments
winloss/<year>-<slug>.yaml    outcome records
intake/                       drop zone → /ingest → processed/ + LOG.md
config/                       taxonomy, tiers, threat factors, banners
templates/                    authoring templates
tools/                        python build layer     docs/  built site
.claude/skills/               the workflow commands
```

Operating rules for Claude sessions live in `CLAUDE.md`. Controlled
vocabulary (markets, agencies, vehicles) lives in `config/taxonomy.yaml` —
add values there before tagging cards with them.

## Example data

The three competitors (Meridian Federal Solutions, Cobalt Ridge
Technologies, Ironvale Group), one assessment, and two win/loss records are
**fictional** demonstrations, flagged `example: true`. Remove them when
seeding real data:

```
rm -rf competitors/meridian-federal competitors/cobalt-ridge competitors/ironvale
rm winloss/*example* opportunities/example-*.md
python3 -m tools build
```

---
name: publish
description: Validate, rebuild the site, and commit — the release step that makes edits visible to consumers. Use for "publish", "rebuild", or after approvals.
---

# Publish the library

## Steps

1. Run `python3 -m tools build`. It validates first and aborts on any
   error — fix the content, never bypass validation to get a build out.
2. Sanity-check the result: the summary line's card/assessment/record
   counts should match expectations; spot-open a changed page in `docs/`
   if the change was structural.
3. Optionally regenerate exports for changed cards
   (`python3 -m tools export pdf <slug>`, `docx`, `pack`). `exports/` is
   gitignored — hand those files out directly.
4. Commit everything (content + `docs/`) with a message that lists the
   cards/assessments touched and why, e.g.
   `Refresh meridian-federal (2026-07 awards); approve cobalt-ridge`.
5. Push only when the user wants the remote updated:
   `git push -u origin <current branch>`.

Consumers read the committed `docs/` — an unpublished edit doesn't exist
for them. Never hand-edit files in `docs/`; they're overwritten on every
build.

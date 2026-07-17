---
name: winloss
description: Record a win/loss outcome as a structured record that rolls up onto competitor cards. Use after an award decision, a debrief, or "log the loss on X".
---

# Record a win/loss

Argument: opportunity name and outcome if known. Source material can be a
debrief file in `intake/` or facts from the conversation.

## Steps

1. Gather the facts: opportunity, agency, vehicle, value, award date,
   outcome (`win` / `loss` / `no-bid` observed), our role, who won, who else
   competed and in what role, why it went that way (factor tags plus a short
   narrative from the debrief), and lessons.
2. Create `winloss/<award-year>-<opp-slug>.yaml` from
   `templates/winloss.yaml`. Convention: when we won, `winner:` is
   `{card: null, name: "Astrion (us)"}`. Reference competitor cards by slug
   so the rollup finds them.
3. If an assessment exists in `opportunities/`, set `opportunity_slug` and
   update its `status` to `won` / `lost`.
4. Push durable insights onto the involved cards (as drafts): debrief
   language about their weaknesses becomes `PP#` evidence; add a Recent
   Developments bullet.
5. Run `python3 -m tools validate` and `python3 -m tools build` — the
   head-to-head tables and dashboard update automatically.
6. Summarize the record and any card changes needing `/review`.

Quote debrief language faithfully — the customer's own words are the most
reusable proof points. Never embellish the outcome narrative.

---
name: status
description: Library health check — staleness, pending approvals, completeness gaps, active pursuits — with prioritized next actions. Use for "status", "what's stale", or a weekly check-in.
---

# Library status

## Steps

1. Run `python3 -m tools report`.
2. Interpret it, don't just paste it. Priority order:
   - Stale Tier 1 cards (these are the cards people actually fight with).
   - Cards stuck in `draft`/`in-review` that an active pursuit depends on —
     cross-check `opportunities/` with near-term dates.
   - Completeness gaps blocking approval.
   - Tier 3 cards whose world changed (check Recent Developments dates).
3. Recommend the short list of next actions with the exact commands:
   `/refresh <slug>`, `/review <slug>`, `/assess <opp>`.
4. If asked, execute them — refreshes can run back-to-back in one session.

Keep the output tight: a team lead should read it in thirty seconds.

---
name: ask
description: Answer questions across the whole library with citations to cards, assessments, and win/loss records. Use for questions like "who beats us on price at AFTC" or "which competitors hold OASIS+".
---

# Ask the library

Argument: the question, e.g. `/ask who do we keep losing to at AFTC and why?`

## Steps

1. Search the library, not your memory: grep across `competitors/`,
   `opportunities/`, and `winloss/`, then read the relevant cards and
   records in full. Frontmatter tags answer filter-type questions (vehicles,
   agencies, set-asides); sections and win/loss records answer the rest.
2. Synthesize a direct answer. For every claim, cite where it lives:
   `competitors/<slug>/card.md` (section or W#/PP# id),
   `winloss/<record>.yaml`, or `opportunities/<slug>.md`.
3. Distinguish clearly between cited fact, the card's recorded team
   judgment, and your own synthesis across cards.
4. Flag reliability: content from `draft` or stale cards gets a caveat;
   note `last_reviewed` when it matters to the answer.
5. If the library can't answer, say exactly that and offer the fix:
   `/refresh <slug>`, `/new-card <name>`, or targeted research.

Never invent intel that is neither in the library nor from fresh research
you did in this session (and label fresh research as such).

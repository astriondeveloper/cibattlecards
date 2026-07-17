---
name: ingest
description: Process files dropped into intake/ (win/loss debriefs, capture notes, past proposals, black hat outputs, GovWin/BGov exports) into draft card updates with provenance. Use when asked to ingest or process intake.
---

# Ingest intake documents

Argument: optional filename. Without one, process everything in `intake/`
except `README.md` and `processed/`.

## Steps

1. **Screen first.** Before extracting anything, check each document for CUI
   banners, "Controlled Unclassified Information", source-selection
   information (FAR 3.104), or another company's proprietary markings. If
   found: stop for that file, leave it in place, and tell the user exactly
   what you saw. Do not copy any of its content into the library.
2. Read the document and identify competitor-relevant intel: evidence of
   strengths/weaknesses, pricing signals, ghosting language that worked,
   evaluator sentiment, personnel moves, teaming arrangements.
3. For each affected competitor:
   - Update `competitors/<slug>/card.md` as a draft. If the card was
     `approved`, set it back to `draft` and say so.
   - New facts land as `### W#` or `### PP#` blocks (or updates to them)
     citing a new `[S#]` Sources entry that points at the processed file
     path and date.
   - Add a dated bullet to Recent Developments where relevant.
   - No card yet? Offer `/new-card`.
4. If the document is a debrief for a decided pursuit, offer to record it
   via `/winloss`.
5. Move the file to `intake/processed/` and append an entry to
   `intake/processed/LOG.md` (date, type, what was extracted, cards
   touched).
6. Run `python3 -m tools validate`, then summarize per-card changes and
   remind the owner to `/review`.

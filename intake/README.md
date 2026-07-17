# Intake

Drop source files here for ingestion: win/loss debriefs, capture call notes,
black hat outputs, past proposal excerpts, GovWin/BGov exports (PDF, DOCX,
CSV, TXT, MD).

Then run `/ingest` in Claude Code. Each file is parsed, relevant card updates
are proposed as drafts for your review, and the file moves to `processed/`
with an entry in `processed/LOG.md` recording what was extracted and which
cards it touched.

**Do not drop CUI or source-selection material here.** This library is for
company competition-sensitive analysis only. Ingestion stops and warns if a
document appears to carry CUI or source-selection markings.

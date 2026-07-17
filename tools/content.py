"""Load, parse, and model the battle card library content."""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
COMPETITORS_DIR = ROOT / "competitors"
OPPORTUNITIES_DIR = ROOT / "opportunities"
WINLOSS_DIR = ROOT / "winloss"

CARD_SECTIONS = [
    "Overview",
    "Threat Summary",
    "Their Discriminators",
    "Strengths",
    "Weaknesses",
    "Our Counter-Positioning",
    "Objection Handling",
    "Trap-Setting Questions",
    "Ghosting Library",
    "Pricing Posture",
    "Win/Loss vs Us",
    "Intel & Proof Points",
    "Recent Developments",
    "Sources",
]

CALL_VIEW_SECTIONS = [
    "Threat Summary",
    "Their Discriminators",
    "Our Counter-Positioning",
    "Objection Handling",
    "Trap-Setting Questions",
]

ASSESSMENT_SECTIONS = [
    "Competitive Landscape",
    "Likely Teaming",
    "Our Positioning",
    "Black Hat Notes",
]

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
BLOCK_HEADING_RE = re.compile(r"^###\s+([A-Z]+\d+)\s*(?:[—–-]\s*)?(.*)$", re.MULTILINE)
SOURCE_ID_RE = re.compile(r"^\s*-\s*\[S(\d+)\]", re.MULTILINE)
CITATION_RE = re.compile(r"\[S(\d+)\]")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

# Generic corporate words ignored when checking that ghost text doesn't name
# a competitor.
GENERIC_NAME_WORDS = {
    "the", "and", "of", "inc", "llc", "corp", "corporation", "company",
    "group", "federal", "solutions", "services", "systems", "technologies",
    "technology", "sciences", "international", "global", "national",
}


class ContentError(Exception):
    """Raised when a file cannot be parsed at all."""


@dataclass
class Config:
    settings: dict
    taxonomy: dict
    tiers: dict
    content_optional: list
    threat_factors: dict
    threat_scores: list

    @property
    def output_dir(self) -> Path:
        return ROOT / self.settings.get("output_dir", "docs")


def _load_yaml(path: Path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_config() -> Config:
    tiers_raw = _load_yaml(CONFIG_DIR / "tiers.yaml")
    factors_raw = _load_yaml(CONFIG_DIR / "threat-factors.yaml")
    return Config(
        settings=_load_yaml(CONFIG_DIR / "settings.yaml"),
        taxonomy=_load_yaml(CONFIG_DIR / "taxonomy.yaml"),
        tiers={int(k): v for k, v in tiers_raw["tiers"].items()},
        content_optional=list(tiers_raw.get("content_optional") or []),
        threat_factors=factors_raw["factors"],
        threat_scores=list(factors_raw["scores"]),
    )


def parse_document(path: Path):
    """Parse a frontmatter+markdown doc into (meta, sections, heading_order)."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ContentError(f"{path}: missing YAML frontmatter block")
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise ContentError(f"{path}: invalid YAML frontmatter: {exc}") from exc

    sections: dict[str, str] = {}
    order: list[str] = []
    current = None
    lines: list[str] = []
    for line in text[match.end():].splitlines():
        if line.startswith("## ") and not line.startswith("###"):
            if current is not None:
                sections[current] = "\n".join(lines).strip()
            current = line[3:].strip()
            order.append(current)
            lines = []
        elif current is not None:
            lines.append(line)
    if current is not None:
        sections[current] = "\n".join(lines).strip()
    return meta, sections, order


def visible_text(section_text: str) -> str:
    """Section content with HTML comments (template guidance) stripped."""
    return COMMENT_RE.sub("", section_text or "").strip()


def split_blocks(section_text: str):
    """Split a section into (id, title, body) on '### W1 — title' headings."""
    blocks = []
    matches = list(BLOCK_HEADING_RE.finditer(section_text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section_text)
        blocks.append((match.group(1), match.group(2).strip(),
                       section_text[match.start():end]))
    return blocks


def parse_ghost_entries(section_text: str):
    """Parse Ghosting Library blocks into structured entries."""
    entries = []
    for gid, title, body in split_blocks(section_text):
        entry = {"id": gid, "title": title, "ghost": "", "targets": "",
                 "proof": "", "used_in": ""}
        for label, key in (("Ghost", "ghost"), ("Targets", "targets"),
                           ("Proof", "proof"), ("Used in", "used_in")):
            m = re.search(rf"^\s*-\s*{label}:\s*(.+)$", body,
                          re.MULTILINE | re.IGNORECASE)
            if m:
                entry[key] = m.group(1).strip().strip('"')
        entries.append(entry)
    return entries


def coerce_date(value):
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


@dataclass
class Card:
    slug: str
    path: Path
    meta: dict
    sections: dict
    heading_order: list

    @property
    def name(self) -> str:
        return str(self.meta.get("name") or self.slug)

    @property
    def tier(self):
        return self.meta.get("tier")

    @property
    def status(self) -> str:
        return str(self.meta.get("status") or "")

    @property
    def last_reviewed(self):
        return coerce_date(self.meta.get("last_reviewed"))

    def days_since_review(self, today: dt.date):
        reviewed = self.last_reviewed
        return (today - reviewed).days if reviewed else None

    def staleness_days(self, config: Config):
        tier = config.tiers.get(self.tier) if isinstance(self.tier, int) else None
        return tier["staleness_days"] if tier else None

    def is_stale(self, config: Config, today: dt.date) -> bool:
        age = self.days_since_review(today)
        threshold = self.staleness_days(config)
        if age is None or threshold is None:
            return True  # unknown review date/tier is treated as stale
        return age > threshold

    def searchable_text(self) -> str:
        parts = [self.name, " ".join(self.meta.get("aliases") or [])]
        parts += [visible_text(t) for t in self.sections.values()]
        return re.sub(r"\s+", " ", " ".join(parts)).lower()


@dataclass
class Opportunity:
    slug: str
    path: Path
    meta: dict
    sections: dict
    heading_order: list

    @property
    def title(self) -> str:
        return str(self.meta.get("title") or self.slug)

    @property
    def competitors(self) -> list:
        return list(self.meta.get("competitors") or [])


@dataclass
class WinLossRecord:
    path: Path
    data: dict

    @property
    def rec_id(self) -> str:
        return str(self.data.get("id") or self.path.stem)

    @property
    def outcome(self) -> str:
        return str(self.data.get("outcome") or "")

    @property
    def award_date(self):
        return coerce_date(self.data.get("award_date"))

    @property
    def winner(self) -> dict:
        return self.data.get("winner") or {}

    @property
    def competitors(self) -> list:
        return list(self.data.get("competitors") or [])

    def competitor_cards(self) -> set:
        cards = {c.get("card") for c in self.competitors if c.get("card")}
        if self.winner.get("card"):
            cards.add(self.winner["card"])
        return cards

    def involves(self, slug: str) -> bool:
        return slug in self.competitor_cards()


def load_cards() -> list:
    cards = []
    if not COMPETITORS_DIR.is_dir():
        return cards
    for folder in sorted(COMPETITORS_DIR.iterdir()):
        if not folder.is_dir():
            continue
        card_path = folder / "card.md"
        if not card_path.is_file():
            raise ContentError(f"{folder}: competitor folder has no card.md")
        meta, sections, order = parse_document(card_path)
        cards.append(Card(slug=folder.name, path=card_path, meta=meta,
                          sections=sections, heading_order=order))
    cards.sort(key=lambda c: c.name.lower())
    return cards


def load_opportunities() -> list:
    opps = []
    if not OPPORTUNITIES_DIR.is_dir():
        return opps
    for path in sorted(OPPORTUNITIES_DIR.glob("*.md")):
        meta, sections, order = parse_document(path)
        opps.append(Opportunity(slug=path.stem, path=path, meta=meta,
                                sections=sections, heading_order=order))
    return opps


def load_winloss() -> list:
    records = []
    if not WINLOSS_DIR.is_dir():
        return records
    for path in sorted(WINLOSS_DIR.glob("*.yaml")):
        data = _load_yaml(path)
        if not isinstance(data, dict):
            raise ContentError(f"{path}: expected a YAML mapping")
        records.append(WinLossRecord(path=path, data=data))
    records.sort(key=lambda r: (r.award_date or dt.date.min), reverse=True)
    return records


def rollup(records: list, slug: str) -> dict:
    """Head-to-head history for one competitor across all win/loss records."""
    rows = []
    tally = {"pursuits": 0, "we_won": 0, "we_lost": 0, "observed": 0}
    for rec in records:
        if not rec.involves(slug):
            continue
        tally["pursuits"] += 1
        if rec.outcome == "win":
            tally["we_won"] += 1
        elif rec.outcome == "loss":
            tally["we_lost"] += 1
        else:
            tally["observed"] += 1
        their_role = next((c.get("role", "") for c in rec.competitors
                           if c.get("card") == slug), "")
        winner = rec.winner.get("card") or rec.winner.get("name") or ""
        rows.append({
            "year": rec.award_date.year if rec.award_date else "",
            "opportunity": rec.data.get("opportunity", rec.rec_id),
            "agency": rec.data.get("agency", ""),
            "value": rec.data.get("value", ""),
            "outcome": rec.outcome,
            "their_role": their_role,
            "winner": winner,
            "they_won": winner == slug,
        })
    return {"tally": tally, "rows": rows}


def name_tokens(card: Card) -> set:
    """Distinctive words from a competitor's name/aliases, for ghost checks."""
    words = card.name.split()
    for alias in card.meta.get("aliases") or []:
        words += str(alias).split()
    return {
        w.lower().strip(".,()") for w in words
        if len(w) > 3 and w.lower().strip(".,()") not in GENERIC_NAME_WORDS
    }

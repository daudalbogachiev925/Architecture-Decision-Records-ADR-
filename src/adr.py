from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from enum import Enum
import re

class ADRStatus(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEPRECATED = "deprecated"
    SUPERSEDED = "superseded"

@dataclass
class ADR:
    id: str
    title: str
    status: ADRStatus
    date: str
    context: str = ""
    decision: str = ""
    consequences: str = ""
    alternatives: str = ""
    related: list = field(default_factory=list)
    superseded_by: str = ""
    authors: list = field(default_factory=list)

    def to_markdown(self):
        lines = [
            f"# {self.id}. {self.title}",
            "",
            f"- Status: {self.status.value}",
            f"- Date: {self.date}",
            f"- Authors: {', '.join(self.authors) if self.authors else '-'}",
        ]
        if self.related:
            lines.append(f"- Related: {', '.join(self.related)}")
        if self.superseded_by:
            lines.append(f"- Superseded by: {self.superseded_by}")
        lines += [
            "",
            "## Context",
            self.context,
            "",
            "## Decision",
            self.decision,
            "",
            "## Alternatives",
            self.alternatives,
            "",
            "## Consequences",
            self.consequences,
        ]
        return "\n".join(lines)

    @classmethod
    def from_markdown(cls, path):
        text = Path(path).read_text(encoding="utf-8")
        lines = text.split("\n")
        header = lines[0]
        m = re.match(r"#\s+(\d+)\.\s+(.+)", header)
        adr_id = m.group(1) if m else "0000"
        title = m.group(2) if m else "Untitled"

        meta = {}
        for line in lines[1:30]:
            mm = re.match(r"-\s+(\w[\w\s]*):\s*(.*)", line)
            if mm:
                meta[mm.group(1).strip().lower()] = mm.group(2).strip()

        def section(name):
            try:
                i = text.index(f"## {name}")
                j = text.find("## ", i + 3)
                block = text[i + len(name) + 3: j if j != -1 else len(text)]
                return block.strip()
            except ValueError:
                return ""

        return cls(
            id=adr_id, title=title,
            status=ADRStatus(meta.get("status", "proposed").lower()),
            date=meta.get("date", ""),
            authors=[a.strip() for a in meta.get("authors", "").split(",") if a.strip()],
            related=[r.strip() for r in meta.get("related", "").split(",") if r.strip()],
            superseded_by=meta.get("superseded by", ""),
            context=section("Context"),
            decision=section("Decision"),
            alternatives=section("Alternatives"),
            consequences=section("Consequences"),
        )

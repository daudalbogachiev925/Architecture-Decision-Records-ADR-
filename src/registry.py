from pathlib import Path
from src.adr import ADR

class ADRRegistry:
    def __init__(self, folder="adr"):
        self.folder = Path(folder)
        self.folder.mkdir(exist_ok=True)
        self.adrs = []

    def load(self):
        self.adrs = []
        for p in sorted(self.folder.glob("*.md")):
            try:
                self.adrs.append(ADR.from_markdown(p))
            except Exception as e:
                print(f"Failed to load {p}: {e}")
        return self.adrs

    def next_id(self):
        self.load()
        if not self.adrs:
            return "0001"
        return f"{int(max(a.id for a in self.adrs)) + 1:04d}"

    def create(self, title, status="proposed", authors=None):
        adr_id = self.next_id()
        from datetime import datetime
        adr = ADR(
            id=adr_id, title=title, status=status,
            date=datetime.utcnow().date().isoformat(),
            authors=authors or [],
        )
        path = self.folder / f"{adr_id}-{self._slug(title)}.md"
        path.write_text(adr.to_markdown(), encoding="utf-8")
        return adr

    def _slug(self, s):
        import re
        return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

    def find(self, adr_id):
        self.load()
        return next((a for a in self.adrs if a.id == adr_id), None)

    def by_status(self, status):
        self.load()
        return [a for a in self.adrs if a.status == status]

    def stats(self):
        self.load()
        counts = {}
        for a in self.adrs:
            counts[a.status.value] = counts.get(a.status.value, 0) + 1
        return {"total": len(self.adrs), "by_status": counts}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.registry import ADRRegistry
from src.search import ADRSearch
from src.export import to_json, to_index_markdown

app = FastAPI(title="ADR Registry")
registry = ADRRegistry("adr")

class ADRCreate(BaseModel):
    title: str
    status: str = "proposed"
    authors: List[str] = []

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/adrs")
def list_adrs(status: Optional[str] = None):
    registry.load()
    adrs = registry.adrs if not status else registry.by_status(status)
    return [a.__dict__ for a in adrs]

@app.get("/adrs/{adr_id}")
def get_adr(adr_id: str):
    a = registry.find(adr_id)
    if not a:
        raise HTTPException(404, "ADR not found")
    return a.__dict__

@app.post("/adrs")
def create_adr(data: ADRCreate):
    adr = registry.create(data.title, data.status, data.authors)
    return adr.__dict__

@app.get("/search")
def search(q: str, top_k: int = 5):
    registry.load()
    return ADRSearch(registry.adrs).search(q, top_k)

@app.get("/stats")
def stats():
    return registry.stats()

@app.get("/export/markdown")
def export_md():
    registry.load()
    return {"content": to_index_markdown(registry.adrs)}

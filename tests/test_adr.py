from src.adr import ADR, ADRStatus
from src.registry import ADRRegistry
import tempfile, os

def test_adr_to_markdown():
    a = ADR("0001", "Test", ADRStatus.ACCEPTED, "2025-01-01",
            context="c", decision="d", consequences="con")
    md = a.to_markdown()
    assert "# 0001. Test" in md
    assert "accepted" in md

def test_registry_create():
    tmp = tempfile.mkdtemp()
    r = ADRRegistry(tmp)
    adr = r.create("New decision", "accepted", ["Alice"])
    assert adr.id == "0001"
    assert adr.status == "accepted"

def test_registry_next_id():
    tmp = tempfile.mkdtemp()
    r = ADRRegistry(tmp)
    r.create("First", "accepted")
    r.create("Second", "accepted")
    assert r.next_id() == "0003"

from eudract import Eudract
import tempfile
import sqlite3
import json
from pathlib import Path


def test_search():
    eu = Eudract()
    assert eu.search("gutihkkùml") == []
    x = eu.search("covid", size=10)
    assert len(x) == 10
    x = eu.search("EFC14280")
    assert json.dumps(x) == Path("tests/data/full.json").read_text()


def test_fetch_study():
    eu = Eudract()
    x = eu.fetch_study("2015-001314-10")
    assert json.dumps(x) == Path("tests/data/one_study.json").read_text()
    assert eu.fetch_study("fake_id") is None
    assert eu.fetch_study("2021-123456-12") is None


def test_search_cache():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db_file = tmp.name
    eu = Eudract()
    eu.search("covid", size=10, cache_file=db_file)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(
        """ SELECT COUNT(*) from results """,
    )
    rows = cur.fetchone()[0]
    assert rows == 10


def test_fetch_study_cache():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db_file = tmp.name
    eu = Eudract()
    eu.search("EFC14280", cache_file=db_file)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(
        """ SELECT COUNT(*) from results """,
    )
    rows = cur.fetchone()[0]
    assert rows == 1
    x = eu.search("EFC14280", cache_file=db_file)
    y = eu.search("EFC14280", cache_file=db_file)
    assert x == y

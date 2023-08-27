from eudract import Eudract
import tempfile
import sqlite3
import json
from pathlib import Path


def test_search():
    eu = Eudract()
    x = eu.search("EFC14280", "summary")
    assert json.dumps(x[0]) == Path("tests/data/one_study_summary.json").read_text()
    assert eu.search("gutihkkùml") == []
    x = eu.search("covid", size=10)
    assert len(x) == 10
    assert len(set([i["EudraCT Number"] for i in x])) == 10
    x = eu.search("EFC14280", "full")
    assert json.dumps(x) == Path("tests/data/full.json").read_text()


def test_info():
    eu = Eudract()
    assert eu.info("jffs") is None
    x = eu.info("2015-001314-10", "summary")
    assert json.dumps(x) == Path("tests/data/one_study_summary.json").read_text()
    assert eu.info("fake_id", "summary") is None
    assert eu.info("2021-123456-12", "summary") is None


def test_info_full():
    eu = Eudract()
    x = eu.info("2015-001314-10", "full")
    assert json.dumps(x) == Path("tests/data/one_study_full.json").read_text()
    assert eu.info("fake_id", "full") is None
    assert eu.info("2021-123456-12", "full") is None


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


def test_info_cache():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db_file = tmp.name
    eu = Eudract()
    eu.search("EFC14280", "summary", cache_file=db_file)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(
        """ SELECT COUNT(*) from results """,
    )
    rows = cur.fetchone()[0]
    assert rows == 1
    x = eu.search("EFC14280", "full", cache_file=db_file)
    y = eu.search("EFC14280", "full", cache_file=db_file)
    assert x == y

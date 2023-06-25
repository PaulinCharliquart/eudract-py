from eudract import Eudract
import tempfile
import sqlite3
import json
from pathlib import Path


def test_search():
    eu = Eudract()
    x = eu.search("EFC14280", "summary", False)
    x[0] = x[0].replace("\r", "").replace("\n", "")
    assert x[0] == Path("tests/data/one_study_summary.txt").read_text()
    x = eu.search("EFC14280", "summary", True)
    assert json.dumps(x[0]) == Path("tests/data/one_study_summary.json").read_text()
    assert eu.search("gutihkkùml") == []
    x = eu.search("covid", size=10, to_dict=True)
    assert len(x) == 10
    assert len(set([i["EudraCT Number"] for i in x])) == 10
    x = eu.search("EFC14280", "full", to_dict=True)
    assert json.dumps(x) == Path("tests/data/full.json").read_text()


def test_info():
    eu = Eudract()
    assert eu.info("jffs") == ""
    x = eu.info("2015-001314-10", "summary", False)
    x = x.replace("\r", "").replace("\n", "")
    assert x == Path("tests/data/one_study_summary.txt").read_text()
    x = eu.info("2015-001314-10", "summary", True)
    assert json.dumps(x) == Path("tests/data/one_study_summary.json").read_text()


def test_info_full():
    eu = Eudract()
    x = eu.info("2015-001314-10", "full", to_dict=False)
    x = x.replace("\r", "").replace("\n", "")
    assert x == Path("tests/data/one_study_full.txt").read_text()
    x = eu.info("2015-001314-10", "full", to_dict=True)
    assert json.dumps(x) == Path("tests/data/one_study_full.json").read_text()


def test_search_cache():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db_file = tmp.name
    eu = Eudract()
    x = eu.search("covid", size=10, to_dict=True, cache_file=db_file)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(
        """ SELECT COUNT(*) from results """,
    )
    rows = cur.fetchone()[0]
    assert rows == 10
    x = eu.search("covid", size=10, to_dict=False, cache_file=db_file)
    cur.execute(
        """ SELECT COUNT(*) from results """,
    )
    rows = cur.fetchone()[0]
    assert rows == 20


def test_info_cache():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db_file = tmp.name
    eu = Eudract()
    x = eu.search("EFC14280", "summary", to_dict=True, cache_file=db_file)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(
        """ SELECT COUNT(*) from results """,
    )
    rows = cur.fetchone()[0]
    assert rows == 1
    x = eu.search("EFC14280", "summary", to_dict=False, cache_file=db_file)
    cur.execute(
        """ SELECT COUNT(*) from results """,
    )
    rows = cur.fetchone()[0]
    assert rows == 2


def test_info_cache():
    eu = Eudract()
    x = eu.search("EFC14280", "full", to_dict=True, cache_file="test.db")
    y = eu.search("EFC14280", "full", to_dict=True, cache_file="test.db")
    assert x == y

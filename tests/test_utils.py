from eudract.utils import create_connection, create_table, write_cache, read_cache
import pytest


def test_db_create():
    db = create_connection("e")
    assert db != None


def test_db_create_failed():
    with pytest.raises(Exception) as e:
        assert create_connection()


def test_db_create_table():
    db = create_connection("e")
    res = create_table(db)
    assert res == True


def test_write_cache():
    db = create_connection("e1")
    create_table(db)
    res = write_cache(db, "x1", "test")
    assert res == True


def test_read_cache():
    db = create_connection("e2")
    create_table(db)
    write_cache(db, "x1", "test")
    res = read_cache(db, "x1")
    assert res == "test"


def test_read_cache_no_key():
    db = create_connection("e")
    create_table(db)
    write_cache(db, "x1", "test")
    res = read_cache(db, "zzzzz")
    assert res == None

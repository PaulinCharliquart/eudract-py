from eudract.utils import (
    create_connection,
    create_table,
    write_cache,
    read_cache,
    validate_id,
)
import pytest
import tempfile


def test_db_create():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db = create_connection(tmp.name)
    assert db is not None


def test_db_create_failed():
    with pytest.raises(Exception) as e:
        assert create_connection()


def test_db_create_table():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db = create_connection(tmp.name)
    res = create_table(db)
    assert res is True


def test_write_cache():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db = create_connection(tmp.name)
    create_table(db)
    res = write_cache(db, "x1", "test")
    assert res is True


def test_read_cache():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db = create_connection(tmp.name)
    create_table(db)
    write_cache(db, "x1", "test")
    res = read_cache(db, "x1")
    assert res == "test"


def test_read_cache_no_key():
    tmp = tempfile.NamedTemporaryFile(delete=False)
    db = create_connection(tmp.name)
    create_table(db)
    write_cache(db, "x1", "test")
    res = read_cache(db, "zzzzz")
    assert res is None


def test_validate_id():
    assert validate_id("eekzpoe") is False
    assert validate_id("2015-001314-10") is True
    assert validate_id("2099-001314-10") is False

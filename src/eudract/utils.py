import logging
import re
import sqlite3
from datetime import datetime

logger = logging.getLogger(__name__)


def create_connection(db_file: str):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        logger.error("Failed to connect to %s: %s", db_file, e)
    return conn


def create_table(conn):
    q = """
    CREATE TABLE if not EXISTS results (
        id text PRIMARY KEY,
        data TEXT NOT NULL,
        create_date NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """
    try:
        cur = conn.cursor()
        cur.execute(q)
        res = True
    except sqlite3.Error as e:
        logger.error("Failed to create table: %s", e)
        res = False
    return res


def write_cache(conn, key, data):
    q = """ INSERT INTO results(id, data) VALUES(?,?) """
    try:
        cur = conn.cursor()
        cur.execute(q, (key, data))
        conn.commit()
        res = True
    except sqlite3.Error as e:
        logger.error("Failed to write cache for %s: %s", key, e)
        res = False
    return res


def read_cache(conn, key):
    try:
        cur = conn.cursor()
        cur.execute(""" SELECT data from results where id = ? """, (key,))
        rows = cur.fetchone()
        res = rows[0] if rows else None
    except sqlite3.Error as e:
        logger.error("Failed to read cache for %s: %s", key, e)
        res = None
    return res


def validate_id(eudract_id: str):
    """
    Validate Eudract Id
    """
    test_id = re.match(r"^20\d{2}-\d{6}-\d{2}$", eudract_id)
    if test_id is None:
        return False
    today_year = datetime.now().year
    try:
        eudract_year = int(eudract_id[0:4])
    except ValueError:
        eudract_year = 0
    return eudract_year in range(2000, today_year)

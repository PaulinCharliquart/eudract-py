import sqlite3
import re
from datetime import datetime


def create_connection(db_file: str):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
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
        print(e)
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
        print(e)
        res = False
    return res


def read_cache(conn, key):
    try:
        cur = conn.cursor()
        cur.execute(""" SELECT data from results where id = ? """, (key,))
        rows = cur.fetchone()
        res = rows[0] if rows else None
    except sqlite3.Error as e:
        print(e)
        res = None
    return res


def validate_id(eudract_id: str):
    """
    Validate Eudract Id
    """
    test_id = re.match("^20\d{2}-\d{6}-\d{2}$", eudract_id)
    if test_id is None:
        return False
    today_year = datetime.now().year
    try:
        eudract_year = int(eudract_id[0:4])
    except ValueError:
        eudract_year = 0
    if eudract_year not in range(2000, today_year):
        return False
    return True

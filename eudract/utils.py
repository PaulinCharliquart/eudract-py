import sqlite3


def create_connection(db_file):
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

import mysql.connector as m
from mysql.connector import Error

conn = m.connect(
    host="localhost",
    user="root",
    passwd="12345",
    db="LibPro"
)

def fAll(query, params=None):
    cur = conn.cursor(buffered=True)
    try:
        cur.execute(query, params or ())
        return cur.fetchall()
    except Error as e:
        print(f"Error fetching all data: {e}")
        return None
    finally:
        cur.close()

def fOne(query, params=None):
    cur = conn.cursor(buffered=True)
    try:
        cur.execute(query, params or ())
        return cur.fetchone()
    except Error as e:
        print(f"Error fetching one row: {e}")
        return None
    finally:
        cur.close()

def fMany(query, size, params=None):
    cur = conn.cursor()
    try:
        cur.execute(query, params or ())
        return cur.fetchmany(size)
    except Error as e:
        print(f"Error fetching many rows: {e}")
        return None
    finally:
        cur.close()

def execQy(query, params=None):
    cur = conn.cursor()
    try:
        cur.execute(query, params or ())
        conn.commit()
    except Error as e:
        print(f"Error executing query: {e}")
        conn.rollback()
    finally:
        cur.close()

def closeCon():
    try:
        conn.close()
    except Error as e:
        print(f"Error closing connection: {e}")

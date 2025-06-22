import sqlite3
import os
from datetime import datetime

from photo_importer.appconfig import AppConfig

def initializeDatabase():
    dbpath = os.path.expanduser(AppConfig.DATABASE)
    # ensure the containing directory exists
    directory = os.path.dirname(dbpath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    # connect (will create file if it doesn't exist)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    initializeRemovableStorage(cursor)

    conn.commit()
    conn.close()

def initializeRemovableStorage(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS removable_storage (
            md5 TEXT,
            path TEXT,
            lmd INTEGER -- epoch seconds
        );
    """)

def initializeLocalStorage(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS local_storage (
            md5 TEXT,
            path TEXT
        );
    """)

def initializeHistory(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            time INTEGER, -- epoch seconds
            action TEXT
        );
    """)

def retrieveLastImported():
    dbpath = os.path.expanduser(AppConfig.DATABASE)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    lastExecuted = cursor.execute(
        """SELECT max(time) FROM history WHERE action = 'import'"""
    ).fetchone()[0]

    conn.commit()
    conn.close()
    if lastExecuted is None:
        return datetime.fromtimestamp(0)
    else:
        return datetime.fromtimestamp(int(lastExecuted))

def insertLastImported(action = 'import'):
    dbpath = os.path.expanduser(AppConfig.DATABASE)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO history (time, action) VALUES (?, ?)""", (datetime.now().timestamp(), action)
    ).fetchone()

    conn.commit()
    conn.close()

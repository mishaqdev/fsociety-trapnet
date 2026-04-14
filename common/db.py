import sqlite3

DB_NAME = 'honeypot.db'

def getDbConnection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initDb():
    conn = getDbConnection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        requestPath TEXT,
        username TEXT,
        password TEXT,
        user_agent TEXT,
        status TEXT,  -- success / failed
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    
def insertAttack(data):
    conn = getDbConnection()
    cursor = conn.cursor()

    cursor.execute  ("""
    INSERT INTO attacks (ip, requestPath, username, password, user_agent, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (data["ip"], data["requestPath"], data["username"], data["password"], data["user_agent"], data["status"]))

    conn.commit()
    conn.close()
    
def getAttacks():
    conn = getDbConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attacks ORDER BY timestamp DESC")
    attacks = cursor.fetchall()

    conn.close()
    return attacks

def deleteAllAttacks():
    conn = getDbConnection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM attacks")

    conn.commit()
    conn.close()
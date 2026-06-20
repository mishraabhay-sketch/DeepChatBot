import sqlite3
import bcrypt

DB_NAME = "data/chatbot.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS imported_files(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT UNIQUE,
        file_hash TEXT UNIQUE,
        imported_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS knowledge(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat_history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        user_message TEXT,
        bot_reply TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_versions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        knowledge_id INTEGER,
        old_answer TEXT,
        new_answer TEXT,
        changed_by TEXT,
        changed_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS memory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        memory_key TEXT,
        memory_value TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversation_memory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        user_message TEXT,
        bot_reply TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        theme TEXT DEFAULT 'dark',
        language TEXT DEFAULT 'English',
        voice TEXT DEFAULT 'female',
        model TEXT DEFAULT 'qwen2.5:3b'
    )
    """)
    
    cur.execute("""
    SELECT COUNT(*)
    FROM settings
    """)
    
    count = cur.fetchone()[0]

    if count == 0:

        cur.execute("""
        INSERT INTO settings(
            theme,
            language,
            voice,
            model
        )
        VALUES(
            'dark',
            'English',
            'female',
            'qwen2.5:3b'
        )
        """)

    cur.execute("""
    SELECT COUNT(*)
    FROM users
    WHERE role='founder'
    """)

    founder_count = cur.fetchone()[0]

    if founder_count == 0:

        hashed = bcrypt.hashpw(
            "123456".encode(),
            bcrypt.gensalt()
        )

        cur.execute("""
        INSERT INTO users(
            username,
            password,
            role
        )
        VALUES (?,?,?)
        """, (
            "abhay",
            hashed.decode(),
            "founder"
        ))
    
    # print(cur.fetchall())
    
    conn.commit()
    conn.close()


def add_pdf_data(question, answer):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO knowledge(question, answer)
        VALUES (?, ?)
        """,
        (question, answer)
    )

    conn.commit()
    conn.close()
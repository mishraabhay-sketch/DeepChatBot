import sqlite3
import bcrypt
import os
import re
DB = "data/chatbot.db"

def connect():
    return sqlite3.connect(DB)

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
    CREATE TABLE IF NOT EXISTS audit_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        action TEXT,

        username TEXT,

        details TEXT,

        created_at DATETIME
        DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_tags(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        knowledge_id INTEGER,
        tag TEXT
    ) 
    """) 
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS learning_queue(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        suggested_answer TEXT,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("PRAGMA table_info(knowledge)")
    info = cur.fetchall()

    print(info)

    columns = [row[1] for row in info]

    if "source_file" not in columns:
        pass
        # cur.execute("""
        # ALTER TABLE knowledge
        # ADD COLUMN source_file TEXT
        # """)


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
            "@sahil_founder",
            hashed.decode(),
            "founder"
        ))
    
    # print(cur.fetchall())
    
    conn.commit()
    conn.close()


def add_pdf_data(question, answer, source_file):

    question = normalize_question(question)
    answer = answer.strip()
    
    if not question or not answer:
        return
    
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id,answer
        FROM knowledge
        WHERE LOWER(question)=LOWER(?)
        """,
        (question,)
    )

    row = cur.fetchone()

    # Question already exists
    if row:

        knowledge_id = row[0]
        old_answer = row[1]

        # Answer changed
        if old_answer != answer:

            cur.execute(
                """
                INSERT INTO knowledge_versions(
                    knowledge_id,
                    old_answer,
                    new_answer,
                    changed_by
                )
                VALUES (?,?,?,?)
                """,
                (
                    knowledge_id,
                    old_answer,
                    answer,
                    "File Upload"
                )
            )

            cur.execute(
                """
                UPDATE knowledge
                SET answer=?,
                    source_file=?
                WHERE id=?
                """,
                (
                    answer,
                    source_file,
                    knowledge_id
                )
            )

            print(
                "UPDATED:",
                question
            )

    else:

        cur.execute(
            """
            INSERT INTO knowledge(
                question,
                answer,
                source_file
            )
            VALUES (?,?,?)
            """,
            (
                question,
                answer,
                source_file
            )
        )

        print(
            "NEW ENTRY:",
            question
        )

    conn.commit()
    conn.close()

def update_knowledge(
    knowledge_id,
    new_answer,
    changed_by,
    question
):
    
    add_audit_log(
        "UPDATE KNOWLEDGE",
        changed_by,
        f"{question}"
    )
    
    
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT answer
        FROM knowledge
        WHERE id=?
        """,
        (knowledge_id,)
    )

    row = cur.fetchone()

    if not row:
        conn.close()
        return False

    old_answer = row[0]

    cur.execute(
        """
        UPDATE knowledge
        SET answer=?
        WHERE id=?
        """,
        (
            new_answer,
            knowledge_id
        )
    )

    cur.execute(
        """
        INSERT INTO knowledge_versions(
            knowledge_id,
            old_answer,
            new_answer,
            changed_by
        )
        VALUES (?,?,?,?)
        """,
        (
            knowledge_id,
            old_answer,
            new_answer,
            changed_by
        )
    )

    conn.commit()
    conn.close()

    return True

def get_knowledge_history(knowledge_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
        old_answer,
        new_answer,
        changed_by,
        changed_at
        FROM knowledge_versions
        WHERE knowledge_id=?
        ORDER BY id DESC
        """,
        (knowledge_id,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows

def get_imported_files():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id,file_name
        FROM imported_files
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def delete_imported_file(file_name):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    
    add_audit_log(
        "DELETE FILE",
        "Founder",
        file_name
    )
    
    cur.execute(
        """
        DELETE FROM knowledge
        WHERE source_file=?
        """,
        (file_name,)
    )

    cur.execute(
        """
        DELETE FROM imported_files
        WHERE file_name=?
        """,
        (file_name,)
    )

    conn.commit()
    conn.close()

    print("Deleted:", file_name)


def get_user_role(username):

        conn = sqlite3.connect("data/chatbot.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT role FROM users WHERE username=?",
            (username,)
        )

        row = cur.fetchone()

        conn.close()

        if row:
            return row[0]

        return "user"


def find_knowledge_by_question(question):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, answer
        FROM knowledge
        WHERE question=?
        """,
        (question,)
    )

    row = cur.fetchone()

    conn.close()

    return row

def show_versions():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM knowledge_versions
    """)

    rows = cur.fetchall()

    for row in rows:
        print(row)

    conn.close()

def normalize_question(text):

    text = text.lower().strip()

    text = re.sub(r'[^\w\s]', '', text)

    text = " ".join(text.split())

    return text


def add_audit_log(
    action,
    username,
    details
):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO audit_log(
            action,
            username,
            details
        )
        VALUES (?,?,?)
        """,
        (
            action,
            username,
            details
        )
    )

    conn.commit()
    conn.close()

def get_audit_logs():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM audit_log
    ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def add_tag(
    knowledge_id,
    tag
):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO knowledge_tags(
            knowledge_id,
            tag
        )
        VALUES (?,?)
        """,
        (
            knowledge_id,
            tag
        )
    )

    conn.commit()
    conn.close()

def get_tags():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT DISTINCT tag
    FROM knowledge_tags
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def add_learning_queue(
    question,
    ai_answer
):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO learning_queue(
            question,
            ai_answer
        )
        VALUES (?,?)
        """,
        (
            question,
            ai_answer
        )
    )

    conn.commit()
    conn.close()

def get_learning_queue():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM learning_queue
    WHERE status='pending'
    ORDER BY id DESC
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def approve_learning(
    queue_id
):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT question,
               ai_answer
        FROM learning_queue
        WHERE id=?
        """,
        (queue_id,)
    )

    row = cur.fetchone()

    if row:

        add_pdf_data(
            row[0],
            row[1],
            "AI Learning"
        )

        cur.execute(
            """
            UPDATE learning_queue
            SET status='approved'
            WHERE id=?
            """,
            (queue_id,)
        )

    conn.commit()
    conn.close()
import sqlite3
from utils import normalize_question
DB = "data/chatbot.db"


def add_knowledge(question, answer):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    question = normalize_question(question)
    cur.execute(
        """
        INSERT INTO knowledge(question, answer)
        VALUES (?, ?)
        """,
        (question, answer)
    )

    conn.commit()
    conn.close()


def get_all_knowledge():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT id, question, answer
    FROM knowledge
    ORDER BY id DESC
    """)

    rows = cur.fetchall()
    
    conn.close()

    return rows


def delete_knowledge(record_id):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM knowledge WHERE id=?",
        (record_id,)
    )

    conn.commit()
    conn.close()

def update_knowledge(
    knowledge_id,
    question,
    new_answer,
    changed_by
):
    question = normalize_question(question)
    
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT answer
        FROM knowledge
        WHERE id=?
        """,
        (knowledge_id,)
    )

    result = cur.fetchone()

    if not result:
        conn.close()
        print("Knowledge record not found")
        return False
    
    print("Result =", result)
    old_answer = result[0]
    
    if old_answer == new_answer:

        conn.close()
        return True
    
    

    print("OLD =", old_answer)
    print("NEW =", new_answer)
    
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

    cur.execute(
        """
        UPDATE knowledge
        SET question=?,
            answer=?
        WHERE id=?
        """,
        (
            question,
            new_answer,
            knowledge_id
        )
    )

    conn.commit()
    conn.close()


def get_knowledge_history(knowledge_id):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT old_answer,
           new_answer,
           changed_by,
           changed_at
    FROM knowledge_versions
    WHERE knowledge_id=?
    ORDER BY id DESC
    """, (knowledge_id,))

    rows = cur.fetchall()

    conn.close()

    return rows


def get_latest_version_by_question(question):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            kv.old_answer,
            kv.new_answer
        FROM knowledge_versions kv
        JOIN knowledge k
        ON kv.knowledge_id = k.id
        WHERE LOWER(k.question)=LOWER(?)
        ORDER BY kv.id DESC
        LIMIT 1
    """,(question,))

    row = cur.fetchone()

    conn.close()

    return row


def get_latest_change(question):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT
            kv.old_answer,
            kv.new_answer
        FROM knowledge_versions kv
        JOIN knowledge k
        ON kv.knowledge_id = k.id
        WHERE LOWER(k.question)=LOWER(?)
        ORDER BY kv.id DESC
        LIMIT 1
    """,(question,))

    row = cur.fetchone()

    conn.close()

    return row

def get_latest_version_by_question(question):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT
        kv.old_answer,
        kv.new_answer
    FROM knowledge_versions kv
    JOIN knowledge k
    ON kv.knowledge_id = k.id
    WHERE LOWER(k.question)=LOWER(?)
    ORDER BY kv.id DESC
    LIMIT 1
    """,(question,))

    row = cur.fetchone()

    conn.close()

    return row
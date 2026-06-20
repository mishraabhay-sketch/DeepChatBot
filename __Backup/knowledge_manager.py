import sqlite3

DB = "data/chatbot.db"


def add_knowledge(question, answer):

    conn = sqlite3.connect(DB)
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
    new_answer
):

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
        return

    old_answer = result[0]

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
            "Founder"
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
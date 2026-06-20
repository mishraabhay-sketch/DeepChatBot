import sqlite3

DB = "data/chatbot.db"

def save_memory(username, key, value):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO memory(
        username,
        memory_key,
        memory_value
    )
    VALUES (?,?,?)
    """, (username, key, value))

    conn.commit()
    conn.close()


def get_memory(username, key):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT memory_value
    FROM memory
    WHERE username=?
    AND memory_key=?
    ORDER BY id DESC
    LIMIT 1
    """, (username, key))

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return None

def save_conversation(
    username,
    user_message,
    bot_reply
):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO conversation_memory(
        username,
        user_message,
        bot_reply
    )
    VALUES (?,?,?)
    """, (
        username,
        user_message,
        bot_reply
    ))

    conn.commit()
    conn.close()

def get_recent_context(
    username,
    limit=10
):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT user_message,
           bot_reply
    FROM conversation_memory
    WHERE username=?
    ORDER BY id DESC
    LIMIT ?
    """, (
        username,
        limit
    ))

    rows = cur.fetchall()

    conn.close()

    rows.reverse()

    context = ""

    for user_msg, bot_msg in rows:

        context += (
            f"User: {user_msg}\n"
            f"AI: {bot_msg}\n"
        )

    return context

def get_memory_history(username, key):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT memory_value
    FROM memory
    WHERE username=?
    AND memory_key=?
    ORDER BY id DESC
    """, (username, key))

    rows = cur.fetchall()

    conn.close()

    return [row[0] for row in rows]
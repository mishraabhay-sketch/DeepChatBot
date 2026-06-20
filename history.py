import sqlite3

DB = "data/chatbot.db"

def save_chat(username, user_message, bot_reply):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO chat_history
        (username, user_message, bot_reply)
        VALUES (?,?,?)
        """,
        (username, user_message, bot_reply)
    )
    
    conn.commit()
    conn.close()


def get_history(username):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id,
               user_message,
               bot_reply,
               timestamp
        FROM chat_history
        WHERE username=?
        ORDER BY id DESC
        """,
        (username,)
    )

    rows = cur.fetchall()

    conn.close()

    return rows
import sqlite3

DB = "data/chatbot.db"

def save_settings(theme, language, voice, model):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM settings")

    cur.execute("""
    INSERT INTO settings(
        theme,
        language,
        voice,
        model
    )
    VALUES (?, ?, ?, ?)
    """, (
        theme,
        language,
        voice,
        model
    ))

    conn.commit()
    conn.close()


def load_settings():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT theme,
           language,
           voice,
           model
    FROM settings
    LIMIT 1
    """)

    row = cur.fetchone()

    conn.close()

    return row
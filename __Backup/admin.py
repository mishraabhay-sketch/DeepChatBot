import sqlite3

DB = "data/chatbot.db"

def add_knowledge(question, answer):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO knowledge(question,answer) VALUES(?,?)",
        (question, answer)
    )

    conn.commit()
    conn.close()
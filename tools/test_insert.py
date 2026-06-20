import sqlite3

conn = sqlite3.connect("data/chatbot.db")
cur = conn.cursor()

cur.execute(
    """
    INSERT INTO knowledge(question, answer)
    VALUES (?, ?)
    """,
    (
        "test question",
        "test answer"
    )
)

conn.commit()
conn.close()

print("Inserted")
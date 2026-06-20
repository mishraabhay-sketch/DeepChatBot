import sqlite3

conn = sqlite3.connect("data/chatbot.db")
cur = conn.cursor()

cur.execute("""
PRAGMA table_info(chat_history)
""")

for row in cur.fetchall():
    print(row)

conn.close()
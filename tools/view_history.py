import sqlite3

conn = sqlite3.connect("data/chatbot.db")

cur = conn.cursor()

cur.execute("""
SELECT user_message,
       bot_reply,
       timestamp
FROM chat_history
""")

rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
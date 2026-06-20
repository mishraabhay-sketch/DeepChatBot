# check_history.py

import sqlite3

conn = sqlite3.connect("data/chatbot.db")
cur = conn.cursor()

cur.execute("""
SELECT username,
       user_message
FROM chat_history
ORDER BY id DESC
""")

for row in cur.fetchall():
    print(row)

conn.close()
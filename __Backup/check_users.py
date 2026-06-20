# check_users.py

import sqlite3

conn = sqlite3.connect("data/chatbot.db")
cur = conn.cursor()

cur.execute("""
SELECT id,
       username,
       role
FROM users
""")

for row in cur.fetchall():
    print(row)

conn.close()
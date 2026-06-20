import sqlite3

conn = sqlite3.connect("data/chatbot.db")
cur = conn.cursor()

cur.execute("""
SELECT username, role
FROM users
""")

rows = cur.fetchall()

for row in rows:
    print(row)

conn.close()
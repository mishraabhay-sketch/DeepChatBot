import sqlite3

conn = sqlite3.connect("data/chatbot.db")
cur = conn.cursor()

cur.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

for row in cur.fetchall():
    print(row)

conn.close()
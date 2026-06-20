import sqlite3

conn = sqlite3.connect("data/chatbot.db")
cur = conn.cursor()

cur.execute("""
SELECT id, question, answer
FROM knowledge
""")

rows = cur.fetchall()

print(rows)

conn.close()
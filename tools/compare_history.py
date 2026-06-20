import sqlite3

conn = sqlite3.connect("data/chatbot.db")
cur = conn.cursor()

print("===== history =====")

cur.execute("""
SELECT *
FROM history
""")

for row in cur.fetchall():
    print(row)

print("\n===== chat_history =====")

cur.execute("""
SELECT *
FROM chat_history
""")

for row in cur.fetchall():
    print(row)

conn.close()
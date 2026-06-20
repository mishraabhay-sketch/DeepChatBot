import sqlite3

conn = sqlite3.connect("data/chatbot.db")
cur = conn.cursor()

cur.execute("SELECT * FROM settings")

rows = cur.fetchall()

print(rows)

conn.close()
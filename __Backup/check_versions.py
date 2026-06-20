# check_versions.py

import sqlite3

conn = sqlite3.connect("data/chatbot.db")
cur = conn.cursor()

cur.execute("SELECT * FROM knowledge_versions")

print(cur.fetchall())

conn.close()
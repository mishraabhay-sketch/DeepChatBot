import sqlite3

conn = sqlite3.connect("data/chatbot.db")
cur = conn.cursor()

cur.execute("""
UPDATE users
SET role='founder'
WHERE username='abhay'
""")

conn.commit()
conn.close()

print("Founder Set Successfully")
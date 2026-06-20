import sqlite3
import bcrypt

DB = "data/chatbot.db"

new_password = bcrypt.hashpw(
    "123456".encode(),
    bcrypt.gensalt()
).decode()

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
UPDATE users
SET password=?
WHERE username='@sahil_founder'
""", (new_password,))

conn.commit()
conn.close()

print("Founder Password Reset Done")
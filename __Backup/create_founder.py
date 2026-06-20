import sqlite3
import bcrypt

DB = "data/chatbot.db"

username = "abhay"
password = "123456"
role = "founder"

hashed = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
INSERT INTO users(
    username,
    password,
    role
)
VALUES (?,?,?)
""", (
    username,
    hashed.decode(),
    role
))

conn.commit()
conn.close()

print("Founder Created Successfully")
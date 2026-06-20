import sqlite3
import bcrypt

DB = "data/chatbot.db"

username = "@sahil_founder"
password = "@sahadi1710"
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
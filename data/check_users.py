# # check_users.py

# import sqlite3
# DB = "data/chatbot.db"
# conn = sqlite3.connect("data/chatbot.db")
# cur = conn.cursor()

# cur.execute("""
# SELECT id,
#        username,
#        role
# FROM users
# """)

# for row in cur.fetchall():
#     print(row)

# conn.close()


# import sqlite3

# conn = sqlite3.connect("data/chatbot.db")
# cur = conn.cursor()

# cur.execute("PRAGMA table_info(imported_files)")
# print("IMPORTED FILES")
# print(cur.fetchall())

# cur.execute("PRAGMA table_info(knowledge)")
# print("KNOWLEDGE")
# print(cur.fetchall())

# conn.close()


# import sqlite3

# conn = sqlite3.connect("data/chatbot.db")
# cur = conn.cursor()

# cur.execute("""
# SELECT COUNT(*)
# FROM knowledge
# WHERE source_file IS NOT NULL
# """)

# print(cur.fetchone())

# conn.close()

# import sqlite3

# conn = sqlite3.connect("data/chatbot.db")
# cur = conn.cursor()

# cur.execute("""
# SELECT DISTINCT source_file
# FROM knowledge
# """)

# for row in cur.fetchall():
#     print(row)

# conn.close()

# import sqlite3

# conn = sqlite3.connect("data/chatbot.db")
# cur = conn.cursor()

# cur.execute("""
# SELECT question, source_file
# FROM knowledge
# LIMIT 20
# """)

# for row in cur.fetchall():
#     print(row)

# conn.close()

# import sqlite3

# conn = sqlite3.connect("data/chatbot.db")
# cur = conn.cursor()

# cur.execute("""
# SELECT COUNT(*)
# FROM knowledge
# WHERE source_file IS NULL
# """)

# print("NULL =", cur.fetchone())

# cur.execute("""
# SELECT COUNT(*)
# FROM knowledge
# WHERE source_file IS NOT NULL
# """)

# print("NOT NULL =", cur.fetchone())

# conn.close()


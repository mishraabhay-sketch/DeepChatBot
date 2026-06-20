import sqlite3
import bcrypt

DB = "data/chatbot.db"

def register_user(username, password, role="user"):

    conn = sqlite3.connect(DB)

    try:

        cur = conn.cursor()

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )

        cur.execute(
            """
            INSERT INTO users(username,password,role)
            VALUES(?,?,?)
            """,
            (username, hashed.decode(), role)
        )

        conn.commit()
    finally:
        conn.close()


def login_user(username, password):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT password, role
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    row = cur.fetchone()

    conn.close()

    if not row:
        return None

    saved_password, role = row

    if bcrypt.checkpw(
        password.encode(),
        saved_password.encode()
    ):
        return role

    return None

def get_all_users():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, username, role
        FROM users
        ORDER BY id
        """
    )

    rows = cur.fetchall()

    conn.close()

    return rows

def get_super_admins():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT id, username, role
    FROM users
    WHERE role='super_admin'
    """)

    rows = cur.fetchall()

    conn.close()

    return rows

def delete_user(user_id):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

def update_role(user_id, new_role):


    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET role=?
        WHERE id=?
        """,
        (new_role, user_id)
    )

    conn.commit()
    conn.close()

def get_admins():

    import sqlite3

    conn = sqlite3.connect(DB)

    cur = conn.cursor()

    cur.execute("""
    SELECT id, username, role
    FROM users
    WHERE role='admin'
    """)

    rows = cur.fetchall()

    conn.close()

    return rows
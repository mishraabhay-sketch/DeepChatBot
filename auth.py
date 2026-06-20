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

def change_password(
    username,
    old_password,
    new_password
):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT password
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    row = cur.fetchone()

    if not row:
        conn.close()
        return False

    saved_password = row[0]

    if not bcrypt.checkpw(
        old_password.encode(),
        saved_password.encode()
    ):
        conn.close()
        return False

    new_hash = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    )

    cur.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (
            new_hash.decode(),
            username
        )
    )

    conn.commit()
    conn.close()

    return True

def reset_password(
    user_id,
    new_password
):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    new_hash = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    )

    cur.execute(
        """
        UPDATE users
        SET password=?
        WHERE id=?
        """,
        (
            new_hash.decode(),
            user_id
        )
    )

    conn.commit()
    conn.close()

    return True

def change_username(
    old_username,
    new_username
):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE users
            SET username=?
            WHERE username=?
            """,
            (
                new_username,
                old_username
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()

def update_password(user_id, new_password):

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    hashed = bcrypt.hashpw(
        new_password.encode(),
        bcrypt.gensalt()
    )

    cur.execute(
        """
        UPDATE users
        SET password=?
        WHERE id=?
        """,
        (
            hashed.decode(),
            user_id
        )
    )

    conn.commit()
    conn.close()

def get_only_users():

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT id, username, role
    FROM users
    WHERE role='user'
    """)

    rows = cur.fetchall()

    conn.close()

    return rows




# def reset_password(self):

#     user_id = self.get_selected_id()

#     if user_id is None:
#         return

#     new_password, ok = QInputDialog.getText(
#         self,
#         "Reset Password",
#         "New Password:",
#         QLineEdit.EchoMode.Password
#     )

#     if not ok or not new_password:
#         return

#     update_password(
#         user_id,
#         new_password
#     )

#     QMessageBox.information(
#         self,
#         "Success",
#         "Password Updated"
#     )
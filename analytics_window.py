from PyQt6.QtWidgets import *
import sqlite3
DB = "data/chatbot.db"

class AnalyticsWindow(QWidget):

    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator

        self.setWindowTitle("📊 Analytics Dashboard")
        self.resize(700, 500)

        layout = QVBoxLayout()

        self.btn_back = QPushButton("⬅ Back")
        self.btn_back.clicked.connect(self.go_back)
        
        self.stats = QTextEdit()
        self.stats.setReadOnly(True)
        layout.addWidget(self.btn_back)
        layout.addWidget(self.stats)

        self.setLayout(layout)

        self.load_stats()

    def load_stats(self):

        conn = sqlite3.connect(
            "data/chatbot.db"
        )

        cur = conn.cursor()

        # Users

        cur.execute(
            "SELECT COUNT(*) FROM users"
        )
        total_users = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM users WHERE role='admin'"
        )
        admins = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM users WHERE role='super_admin'"
        )
        super_admins = cur.fetchone()[0]

        cur.execute(
            "SELECT COUNT(*) FROM users WHERE role='founder'"
        )
        founders = cur.fetchone()[0]

        # Knowledge

        cur.execute(
            "SELECT COUNT(*) FROM knowledge"
        )
        knowledge = cur.fetchone()[0]

        # Chat History

        cur.execute(
            "SELECT COUNT(*) FROM chat_history"
        )
        chats = cur.fetchone()[0]

        conn.close()

        report = f"""
📊 ChatBot ANALYTICS

👤 Accounts
--------------------------
Total Users      : {total_users}
Admins           : {admins}
Super Admins     : {super_admins}
Founders         : {founders}

🧠 Knowledge Base
--------------------------
Knowledge Records : {knowledge}

💬 Chat System
--------------------------
Total Chats : {chats}

🟢 Database Status : Online
"""

        self.stats.setText(report)

    def go_back(self):

        if self.navigator:
            self.navigator.go_back()

    def get_total_users():

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
        SELECT COUNT(*)
        FROM users
        """)

        total = cur.fetchone()[0]

        conn.close()

        return total


    def get_total_knowledge():

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
        SELECT COUNT(*)
        FROM knowledge
        """)

        total = cur.fetchone()[0]

        conn.close()

        return total


    def get_total_files():

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
        SELECT COUNT(*)
        FROM imported_files
        """)

        total = cur.fetchone()[0]

        conn.close()

        return total


    def get_total_chats():

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
        SELECT COUNT(*)
        FROM chat_history
        """)

        total = cur.fetchone()[0]

        conn.close()

        return total

    def get_today_chats():

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
        SELECT COUNT(*)
        FROM chat_history
        WHERE DATE(timestamp)=DATE('now')
        """)

        total = cur.fetchone()[0]

        conn.close()

        return total

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
        SELECT COUNT(*)
        FROM chat_history
        WHERE DATE(timestamp)=DATE('now')
        """)

        total = cur.fetchone()[0]

        conn.close()

        return total

    def get_top_questions():

        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        cur.execute("""
        SELECT
            user_message,
            COUNT(*)
        FROM chat_history
        GROUP BY user_message
        ORDER BY COUNT(*) DESC
        LIMIT 5
        """)

        rows = cur.fetchall()

        conn.close()

        return rows
    


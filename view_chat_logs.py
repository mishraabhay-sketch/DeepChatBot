from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QHeaderView
import sqlite3


class ViewChatLogs(QWidget):

    def __init__(self, navigator=None):
        super().__init__()
        
        self.navigator = navigator
        
        self.setWindowTitle("📋 Chat Logs")
        self.resize(900, 600)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "Search Question..."
        )

        self.btn_search = QPushButton(
            "🔍 Search"
        )
        
        self.table = QTableWidget()

        self.btn_search.clicked.connect(
            self.search_logs
        )

        self.btn_back = QPushButton("⬅ Back")
        self.btn_back.clicked.connect(self.go_back)
        
        layout = QVBoxLayout()

        layout.addWidget(self.search_box)
        layout.addWidget(self.btn_search)
        layout.addWidget(self.table)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

        self.load_logs()

    def load_logs(self):

        conn = sqlite3.connect(
            "data/chatbot.db"
        )

        cur = conn.cursor()

        cur.execute("""
        SELECT id,
                user_message,
                bot_reply,
                timestamp
        FROM chat_history
        ORDER BY id DESC
        """)

        rows = cur.fetchall()

        conn.close()

        self.show_data(rows)

    def search_logs(self):

        keyword = self.search_box.text()

        conn = sqlite3.connect(
            "data/chatbot.db"
        )

        cur = conn.cursor()

        cur.execute("""
        SELECT ID,
                user_message,
                bot_reply,
                timestamp
        FROM chat_history
        WHERE user_Message LIKE ?
        ORDER BY id DESC
        """, (f"%{keyword}%",))

        rows = cur.fetchall()

        conn.close()

        self.show_data(rows)

    def show_data(self, rows):

        self.table.setColumnCount(4)

        self.table.horizontalHeader().setStretchLastSection(True)
        
        self.table.setHorizontalHeaderLabels(
            ["ID", "user_message", "bot_reply", "timestamp"]
        )

        self.table.setRowCount(len(rows))

        for row_num, row_data in enumerate(rows):

            for col_num, value in enumerate(row_data):

                self.table.setItem(
                    row_num,
                    col_num,
                    QTableWidgetItem(str(value))
                )
        
        self.table.resizeColumnsToContents()

    def go_back(self):

        if self.navigator:
            self.navigator.go_back()   
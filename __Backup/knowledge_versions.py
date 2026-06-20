from PyQt6.QtWidgets import *
import sqlite3


class KnowledgeVersionsWindow(QWidget):

    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator

        self.setWindowTitle(
            "📚 Knowledge Version History"
        )

        self.resize(1000, 600)

        self.btn_back = QPushButton(
            "⬅ Back"
        )

        self.btn_back.clicked.connect(
            self.go_back
        )

        self.table = QTableWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.btn_back)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_data()

    def load_data(self):

        conn = sqlite3.connect(
            "data/chatbot.db"
        )

        cur = conn.cursor()

        cur.execute("""
        SELECT
            id,
            knowledge_id,
            old_answer,
            new_answer,
            changed_by,
            changed_at
        FROM knowledge_versions
        ORDER BY id DESC
        """)

        rows = cur.fetchall()
        print("ROWS =", len(rows))
        conn.close()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Knowledge ID",
            "Old Answer",
            "New Answer",
            "Changed By",
            "Changed At"
        ])

        self.table.setRowCount(len(rows))

        for row_num, row_data in enumerate(rows):

            for col_num, value in enumerate(row_data):

                self.table.setItem(
                    row_num,
                    col_num,
                    QTableWidgetItem(str(value))
                )

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.repaint()
        self.table.update()
    def go_back(self):

        if self.navigator:
            self.navigator.go_back()
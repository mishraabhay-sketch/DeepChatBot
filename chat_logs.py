from PyQt6.QtWidgets import *
from history import get_history


class ChatLogsWindow(QWidget):

    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator

        self.setWindowTitle("Chat Logs")
        self.resize(900, 600)

        self.table = QTableWidget()

        self.btn_back = QPushButton("⬅ Back")
        self.btn_back.clicked.connect(self.go_back)
        
        layout = QVBoxLayout()
        layout.addWidget(self.btn_back)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_logs()

    def load_logs(self):

        data = get_history()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            ["ID", "Question", "Answer"]
        )

        self.table.setRowCount(len(data))

        for row_num, row_data in enumerate(data):

            for col_num, value in enumerate(row_data):

                self.table.setItem(
                    row_num,
                    col_num,
                    QTableWidgetItem(str(value))
                )

    def go_back(self):

        if self.navigator:
            self.navigator.go_back()
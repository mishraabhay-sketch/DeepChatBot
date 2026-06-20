from PyQt6.QtWidgets import *
from knowledge_manager import *

class KnowledgeWindow(QWidget):

    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator
        
        self.setWindowTitle(
            "ChatBot Knowledge Manager"
        )

        self.resize(900, 600)

        self.question = QLineEdit()
        self.question.setPlaceholderText(
            "Enter Question"
        )

        self.answer = QTextEdit()

        self.btn_add = QPushButton(
            "➕ Add Knowledge"
        )

        self.btn_edit = QPushButton(
            "✏ Edit Selected"
        )

        self.btn_delete = QPushButton(
            "🗑 Delete Selected"
        )
        
        self.btn_back = QPushButton(
            "⬅ Back"
        )
        
        self.btn_back.clicked.connect(self.go_back)

        self.btn_edit.clicked.connect(
            self.edit_data
        )

        self.btn_delete.clicked.connect(
            self.delete_data
        )

        self.btn_add.clicked.connect(
            self.add_data
        )

        self.table = QTableWidget()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Question"))
        layout.addWidget(self.question)
        layout.addWidget(self.btn_back)
        layout.addWidget(QLabel("Answer"))
        layout.addWidget(self.answer)

        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_delete)

        layout.addWidget(self.table)

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.setLayout(layout)

        self.load_data()


    def add_data(self):

        q = self.question.text()
        a = self.answer.toPlainText()

        print("QUESTION =", q)
        print("ANSWER =", a)

        if not q or not a:
            return

        add_knowledge(q, a)

        print("SAVED")
        QMessageBox.information(
            self,
            "Success",
            "Knowledge Added"
        )

        self.question.clear()
        self.answer.clear()

        self.load_data()

    def load_data(self):

        data = get_all_knowledge()

        self.table.setColumnCount(3)

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

    def delete_data(self):

        row = self.table.currentRow()

        if row < 0:
            return

        record_id = int(
            self.table.item(row, 0).text()
        )

        delete_knowledge(record_id)

        QMessageBox.information(
            self,
            "Success",
            "Knowledge Deleted"
        )

        self.load_data()

    def edit_data(self):

        row = self.table.currentRow()

        if row < 0:
            return

        record_id = int(
            self.table.item(row, 0).text()
        )

        old_question = self.table.item(
            row,
            1
        ).text()

        old_answer = self.table.item(
            row,
            2
        ).text()

        new_question, ok1 = QInputDialog.getText(
            self,
            "Edit Question",
            "Question:",
            text=old_question
        )

        if not ok1:
            return

        new_answer, ok2 = QInputDialog.getMultiLineText(
            self,
            "Edit Answer",
            "Answer:",
            old_answer
        )

        if not ok2:
            return

        update_knowledge(
            record_id,
            new_question,
            new_answer
        )

        QMessageBox.information(
            self,
            "Success",
            "Knowledge Updated"
        )

        self.load_data()

    def go_back(self):
        
        if self.navigator:
        
            self.navigator.go_back()
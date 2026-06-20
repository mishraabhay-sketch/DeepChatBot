from PyQt6.QtWidgets import *
from auth import get_all_users
from about_window import AboutWindow
from auth import reset_password
from auth import get_only_users
class UserManager(QWidget):

    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator

        self.setWindowTitle(
            "Users"
        )

        self.resize(700, 500)

        self.table = QTableWidget()
        
        self.btn_about = QPushButton("ℹ About ChatBot")
        self.btn_back = QPushButton("⬅ Back")

        self.btn_back.clicked.connect(
            self.go_back
        )
        self.btn_about.clicked.connect(
            self.open_about
        )

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.btn_back)
        layout.addWidget(self.btn_about)
        self.setLayout(layout)

        self.load_users()

    def load_users(self):

        users = get_only_users()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(
            ["ID", "Username", "Role", "Actions"]
        )

        self.table.setRowCount(len(users))

        for row_num, row_data in enumerate(users):

            user_id = row_data[0]

            for col_num, value in enumerate(row_data):

                self.table.setItem(
                    row_num,
                    col_num,
                    QTableWidgetItem(str(value))
                )

            btn_reset = QPushButton(
                "🔐 Reset Password"
            )

            btn_reset.clicked.connect(
                lambda checked,
                uid=user_id:
                self.reset_user_password(uid)
            )

            self.table.setCellWidget(
                row_num,
                3,
                btn_reset
            )

    def go_back(self):

        if self.navigator:
            self.navigator.go_back()

    def open_about(self):

        self.navigator.show_page(
            AboutWindow(self.navigator)
        )

    def reset_user_password(self,user_id):

        new_password, ok = QInputDialog.getText(
            self,
            "Reset Password",
            "Enter New Password:",
            QLineEdit.EchoMode.Password
        )

        if not ok:
            return

        if not new_password:
            return

        reset_password(
            user_id,
            new_password
        )

        QMessageBox.information(
            self,
            "Success",
            "Password Reset Successfully"
        )
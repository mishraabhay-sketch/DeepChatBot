from PyQt6.QtWidgets import *
from auth import register_user
from gui import ChatBotGUI

class RegisterWindow(QWidget):

    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator

        self.setWindowTitle(" ChatBot Register")
        self.resize(400, 300)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText(
            "Confirm Password"
        )
        self.confirm.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.btn_register = QPushButton(
            "Create Account"
        )

        self.btn_register.clicked.connect(
            self.register
        )


        self.btn_back = QPushButton("⬅ Back")
        self.btn_back.clicked.connect(self.go_back)
        
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)
        layout.addWidget(self.btn_back)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)

        layout.addWidget(QLabel("Confirm Password"))
        layout.addWidget(self.confirm)

        layout.addWidget(self.btn_register)

        self.setLayout(layout)

    def register(self):

        username = self.username.text()
        password = self.password.text()
        confirm = self.confirm.text()

        if password != confirm:

            QMessageBox.warning(
                self,
                "Error",
                "Passwords do not match"
            )
            return

        try:

            register_user(
                username,
                password,
                "user"
            )

            QMessageBox.information(
                self,
                "Success",
                "Account Created"
            )

            self.navigator.show_page(
                ChatBotGUI(
                    self.navigator,
                    username
                )
            )

            self.close()

        except Exception as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )

    def go_back(self):

        if self.navigator:
            self.navigator.go_back()
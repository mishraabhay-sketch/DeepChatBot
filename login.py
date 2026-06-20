from PyQt6.QtWidgets import *
from auth import login_user
from gui import ChatBotGUI
from admin_panel import AdminPanel
from founder_panel import FounderPanel
from super_admin_panel import SuperAdminPanel
from register import RegisterWindow

class LoginWindow(QWidget):

    def __init__(self, navigator=None, username=None):
        super().__init__()
        self.username = username
        self.navigator = navigator

        self.setWindowTitle("Login Chat Bot")
        self.resize(400, 250)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.returnPressed.connect(
            self.login
        )

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.returnPressed.connect(
            self.login
        )

        self.login_btn = QPushButton("Login")

        self.register_btn = QPushButton(
            "Create Account"
        )

        self.login_btn.clicked.connect(
            self.login
        )       

        self.register_btn.clicked.connect(
            self.open_register
        )
        
        self.login_btn.setAutoDefault(True)

        
        
        # self.setTabOrder(
        #     self.username,
        #     self.password
        # )

        # self.setTabOrder(
        #     self.password,
        #     self.login_btn
        # )

        # self.setTabOrder(
        #     self.login_btn,
        #     self.register_btn
        # )

        

        

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username)

        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password)
        
        layout.addWidget(self.login_btn)

        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def login(self):

        username = self.username.text()
        password = self.password.text()

        role = login_user(username, password)

        if role == "founder":

            self.navigator.show_page(
                FounderPanel(self.navigator, username)
            )

            self.close()

        elif role == "super_admin":
            
            self.navigator.show_page(
                SuperAdminPanel(self.navigator, username)
            )
            

            self.close()

        elif role == "admin":

            self.navigator.show_page(
                AdminPanel(self.navigator, username)
            )
            self.close()

        elif role == "user":
            
            self.navigator.show_page(
                ChatBotGUI(
                    self.navigator,
                    username
                )
            )
            
            self.close()

        else:

            QMessageBox.warning(
                self,
                "Error",
                "Invalid Username or Password"
            )

    def open_register(self):
        
        self.navigator.show_page(
            RegisterWindow(self.navigator)
        )
        # self.register_window = RegisterWindow()
        # self.register_window.show()


    def go_back(self):

        if self.navigator:
            self.navigator.go_back()
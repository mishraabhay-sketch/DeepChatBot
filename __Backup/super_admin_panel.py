from PyQt6.QtWidgets import *
from auth import register_user
from knowledge_window import KnowledgeWindow
from import_manager import import_any_file
from user_manager import UserManager
from manage_admins import ManageAdmins
from gui import ChatBotGUI
from settings_window import SettingsWindow
from about_window import AboutWindow

class SuperAdminPanel(QWidget):

    def __init__(self, navigator=None, username=None):
        super().__init__()

        self.navigator = navigator
        self.username = username
        self.setWindowTitle("Super Admin")
        self.resize(800, 600)

        title = QLabel("⭐ SUPER ADMIN")
        title.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
            color:#00ffff;
        """)
        
        self.btn_chat = QPushButton("🤖 AI Chat")
        
        self.btn_create_admin = QPushButton("🛡 Create Admin")

        self.btn_manage_admins = QPushButton("👥 Manage Admins")

        self.btn_manage_users = QPushButton("👤 Manage Users")

        self.btn_pdf = QPushButton("📄 Upload File")

        self.btn_knowledge = QPushButton("🧠 Knowledge Manager")
        
        self.btn_settings = QPushButton("⚙ Settings")

        self.btn_back = QPushButton("⬅ Back")

        self.btn_about = QPushButton("ℹ About ChatBot")
        
        self.btn_chat.clicked.connect(
            self.open_chat
        )
        self.btn_create_admin.clicked.connect(
            self.create_admin
        )
        
        self.btn_knowledge.clicked.connect(
            self.open_knowledge
        )

        self.btn_manage_admins.clicked.connect(
            self.open_admins
        )

        self.btn_pdf.clicked.connect(
            self.import_file
        )

        self.btn_manage_users.clicked.connect(
            self.open_users
        )

        self.btn_settings.clicked.connect(
            self.open_settings
        )

        self.btn_back.clicked.connect(
            self.go_back
        )

        self.btn_about.clicked.connect(
            self.open_about
        )

        layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(self.btn_chat)
        layout.addWidget(self.btn_create_admin)
        layout.addWidget(self.btn_manage_admins)
        layout.addWidget(self.btn_manage_users)
        layout.addWidget(self.btn_pdf)
        layout.addWidget(self.btn_knowledge)
        layout.addWidget(self.btn_settings)
        layout.addWidget(self.btn_back)
        layout.addWidget(self.btn_about)
        self.setLayout(layout)
        
    def create_admin(self):

        username, ok1 = QInputDialog.getText(
            self,
            "Create Admin",
            "Username:"
        )

        if not ok1 or not username:
            return

        password, ok2 = QInputDialog.getText(
            self,
            "Create Admin",
            "Password:"
        )

        if not ok2 or not password:
            return

        try:

            register_user(
                username,
                password,
                "admin"
            )

            QMessageBox.information(
                self,
                "Success",
                "Admin Created"
            )

        except Exception as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )

    def open_knowledge(self):

        self.navigator.show_page(
            KnowledgeWindow(self.navigator)
        )

    def import_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "Supported Files (*.pdf *.docx *.txt *.xlsx)"
        )

        if file_path:

            import_any_file(file_path)

            QMessageBox.information(
                self,
                "Success",
                "File Imported Successfully"
            )

    def open_users(self):

        self.navigator.show_page(
            UserManager(self.navigator)
        )

    def open_admins(self):

        QMessageBox.information(
            self,
            "Manage Admins",
            "Manage Admins Window Opening"
        )
        
    def open_admins(self):

        self.navigator.show_page(
            ManageAdmins(self.navigator)
        )

    def open_chat(self):

        self.navigator.show_page(
            ChatBotGUI(self.navigator, self.username)
        )

    def open_settings(self):

        self.navigator.show_page(
            SettingsWindow(self.navigator)
        )

    def go_back(self):

        if self.navigator:
            self.navigator.go_back()

    def open_about(self):

        self.navigator.show_page(
            AboutWindow(self.navigator)
        )
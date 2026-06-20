from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QMessageBox
)

from gui import ChatBotGUI
from knowledge_window import KnowledgeWindow
from user_manager import UserManager
from view_chat_logs import ViewChatLogs
from about_window import AboutWindow
from settings_window import SettingsWindow
from import_manager import import_any_file


class AdminPanel(QWidget):

    def __init__(self, navigator=None, username=None):
        super().__init__()

        self.navigator = navigator
        self.username = username

        self.setWindowTitle("Chat Bot - Admin Panel")
        self.resize(700, 500)

        title = QLabel("👑 Chat Bot ADMIN")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #00ffff;
        """)

        self.btn_chat = QPushButton("🤖 ChatBot")
        self.btn_users = QPushButton("👥 Manage Users")
        self.btn_pdf = QPushButton("📄 Upload File")
        self.btn_knowledge = QPushButton("🧠 Knowledge Manager")
        self.btn_logs = QPushButton("📜 View Chat Logs")
        self.btn_settings = QPushButton("⚙ Settings")
        self.btn_about = QPushButton("ℹ About ChatBot")
        self.btn_back = QPushButton("⬅ Back")

        self.btn_chat.clicked.connect(self.open_chat)
        self.btn_users.clicked.connect(self.open_users)
        self.btn_pdf.clicked.connect(self.import_file)
        self.btn_knowledge.clicked.connect(self.open_knowledge)
        self.btn_logs.clicked.connect(self.open_chat_logs)
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_about.clicked.connect(self.open_about)
        self.btn_back.clicked.connect(self.go_back)

        layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(self.btn_chat)
        layout.addWidget(self.btn_users)
        layout.addWidget(self.btn_pdf)
        layout.addWidget(self.btn_knowledge)
        layout.addWidget(self.btn_logs)
        layout.addWidget(self.btn_settings)
        layout.addWidget(self.btn_about)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

        self.setStyleSheet("""
        QWidget {
            background: #0f0f0f;
            color: white;
        }

        QPushButton {
            background: #161616;
            border: 2px solid #00ffff;
            border-radius: 10px;
            padding: 12px;
            font-size: 14px;
        }

        QPushButton:hover {
            border: 2px solid #00ff99;
        }
        """)

    def open_chat(self):
        self.navigator.show_page(
            ChatBotGUI(self.navigator, self.username)
        )

    def open_users(self):
        self.navigator.show_page(
            UserManager(self.navigator)
        )

    def open_knowledge(self):
        self.navigator.show_page(
            KnowledgeWindow(self.navigator)
        )

    def open_chat_logs(self):
        self.navigator.show_page(
            ViewChatLogs(self.navigator)
        )

    def open_settings(self):
        self.navigator.show_page(
            SettingsWindow(self.navigator, self.username)
        )

    def open_about(self):
        self.navigator.show_page(
            AboutWindow(self.navigator)
        )

    def import_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "Supported Files (*.pdf *.docx *.txt *.xlsx *.jpg *.jpeg *.png *.bmp)"
        )

        if not file_path:
            return

        import_any_file(file_path)

        QMessageBox.information(
            self,
            "Success",
            "File Imported Successfully"
        )

    def go_back(self):
        if self.navigator:
            self.navigator.go_back()
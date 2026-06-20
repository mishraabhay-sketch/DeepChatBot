from PyQt6.QtWidgets import *
from auth import register_user
from knowledge_window import KnowledgeWindow
from import_manager import import_any_file
from user_manager import UserManager
from manage_super_admins import ManageSuperAdmins
from gui import ChatBotGUI
from analytics_window import AnalyticsWindow
from navigator import Navigator
from settings_window import SettingsWindow
from about_window import AboutWindow
from knowledge_versions import KnowledgeVersionsWindow

class FounderPanel(QWidget):
   
    def __init__(self, navigator=None, username=None):
        super().__init__()
        
        self.navigator = navigator
        self.username = username
        self.setWindowTitle(" ChatBot - Founder Panel")
        self.resize(800, 600)

        title = QLabel("👑 FOUNDER ")
        title.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
            color:#00ffff;
        """)
       
        self.btn_chat = QPushButton("🤖 AI Chat")

        self.btn_create_super = QPushButton("⭐ Create Super Admin")
        
        self.btn_manage_super = QPushButton("🛡 Manage Super Admins")

        self.btn_users = QPushButton("👥 View Users")

        self.btn_analytics = QPushButton("📊 Analytics")

        self.btn_knowledge = QPushButton("🧠 Knowledge Manager")
 
        self.btn_versions = QPushButton("📚 Knowledge History")

        self.btn_pdf = QPushButton("📄 Upload File")
        
        self.btn_settings = QPushButton("⚙ Settings")
        
        self.btn_back = QPushButton("⬅ Back")
        
        self.btn_about = QPushButton("ℹ About ChatBot")
        
        self.btn_chat.clicked.connect(
            self.open_chat
        )
        
        self.btn_knowledge.clicked.connect(
            self.open_knowledge
        )

        self.btn_create_super.clicked.connect(
            self.create_super_admin
        )

        self.btn_users.clicked.connect(
            self.open_users
        )
        
        self.btn_manage_super.clicked.connect(
            self.manage_super_admins
        )

        self.btn_pdf.clicked.connect(
            self.import_file
        )

        self.btn_analytics.clicked.connect(
            self.open_analytics
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

        self.btn_versions.clicked.connect(
            self.open_versions
        )

        layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(self.btn_chat)
        layout.addWidget(self.btn_create_super)
        layout.addWidget(self.btn_manage_super)
        
        layout.addWidget(self.btn_users)
        layout.addWidget(self.btn_analytics)
        layout.addWidget(self.btn_knowledge)
        layout.addWidget(self.btn_versions)
        layout.addWidget(self.btn_pdf)
        layout.addWidget(self.btn_settings)
        layout.addWidget(self.btn_back)
        layout.addWidget(self.btn_about)
        self.setLayout(layout)

        self.setStyleSheet("""
        QWidget{
            background:#0f0f0f;
            color:white;
        }

        QPushButton{
            padding:12px;
            border:2px solid #00ffff;
            border-radius:10px;
            font-size:14px;
        }

        QPushButton:hover{
            border:2px solid #00ff99;
        }
        """)
    
    def create_super_admin(self):

        username, ok1 = QInputDialog.getText(
            self,
            "Create Super Admin",
            "Username:"
    )

        if not ok1 or not username:
            return

        password, ok2 = QInputDialog.getText(
            self,
            "Create Super Admin",
            "Password:"
    )

        if not ok2 or not password:
            return

        try:

            register_user(
                username,
                password,
                "super_admin"
            )

            QMessageBox.information(
                self,
                "Success",
                "Super Admin Created"
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

    # def import_any_file(self):

    #     file_path, _ = QFileDialog.getOpenFileName(
    #         self,
    #         "Select File",
    #         "",
    #         "Supported Files (*.pdf *.docx *.txt *.xlsx)"
    #     )

    #     if file_path:

    #         import_pdf(file_path)

    #         QMessageBox.information(
    #             self,
    #             "Success",
    #             "File Imported Successfully"
    #         )

    def open_users(self):

        self.navigator.show_page(
            UserManager(self.navigator)
        )
    

    def manage_super_admins(self):

        self.navigator.show_page(
            ManageSuperAdmins(self.navigator)
        )
    
    def open_analytics(self):

        self.navigator.show_page(
            AnalyticsWindow(self.navigator)
        )

    def open_settings(self):

        self.navigator.show_page(
            SettingsWindow(self.navigator)
        )

    def open_chat(self):

    

        self.navigator.show_page(
            ChatBotGUI(self.navigator, self.username)
        )

    def go_back(self):
        
        if self.navigator:
        
            self.navigator.go_back()

    def open_about(self):

        self.navigator.show_page(
            AboutWindow(self.navigator)
        )

    def import_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            "Supported Files (*.pdf *.docx *.txt *.xlsx)"
        )

        if not file_path:
            return

        result = import_any_file(file_path)

        if result == "duplicate":

            QMessageBox.warning(
                self,
                "Duplicate",
                "This file is already imported."
            )

            return

        QMessageBox.information(
            self,
            "Success",
            "File Imported Successfully"
        )
    
    def open_versions(self):

        self.navigator.show_page(
            KnowledgeVersionsWindow(
                self.navigator
            )
        )

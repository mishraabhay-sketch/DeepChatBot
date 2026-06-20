from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

class SuperAdminDashboard(QWidget):
    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator

        self.setWindowTitle("ChatBot - Super Admin")
        self.resize(1000, 650)

        layout = QVBoxLayout()

        # Header
        title = QLabel("⭐ Super Admin Control Panel")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # Buttons (core features)
        self.btn_create_admin = QPushButton("🛡 Create Admin")
        self.btn_manage_admin = QPushButton("⚙ Manage Admins")
        self.btn_view_users = QPushButton("👤 View Users")
        self.btn_upload_pdf = QPushButton("📄 Upload PDF")
        self.btn_back = QPushButton("⬅ Back")
        

        layout.addWidget(self.btn_create_admin)
        layout.addWidget(self.btn_manage_admin)
        layout.addWidget(self.btn_view_users)
        layout.addWidget(self.btn_upload_pdf)

        self.setLayout(layout)
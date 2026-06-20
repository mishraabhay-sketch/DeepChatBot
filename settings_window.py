from PyQt6.QtWidgets import *
from settings_manager import *
from auth import change_password
class SettingsWindow(QWidget):

    def __init__(self, navigator=None, username=None):
        super().__init__()

        self.navigator = navigator
        self.username = username
        self.setWindowTitle("⚙ Settings")

        self.theme_box = QComboBox()
        self.theme_box.addItems([
            "Dark",
            "Light",
            "Cyber Blue"
        ])

        self.language_box = QComboBox()
        self.language_box.addItems([
            "English",
            "Hindi",
            "Hinglish",
            "Roman Hindi"
        ])

        self.voice_box = self.voice_box = QComboBox()
        self.voice_box.addItems([
            "Female",
            "Male",
            "Off"
        ])
        self.old_password = QLineEdit()
        self.old_password.setEchoMode(
    QLineEdit.EchoMode.Password
)

        self.old_password.setPlaceholderText(
            "Old Password"
        )

        self.new_password = QLineEdit()
        self.new_password.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.new_password.setPlaceholderText(
    "New Password"
)

        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        self.confirm_password.setPlaceholderText(
            "Confirm Password"
        )

        self.btn_change_password = QPushButton(
            "🔐 Change Password"
        )

        self.btn_change_password.clicked.connect(
            self.change_password
        )
        
        self.model_box = QComboBox()
        self.model_box.addItems([
            "qwen2.5:3b"
        ])

        self.btn_save = QPushButton(
            "💾 Save Settings"
        )

        self.btn_back = QPushButton(
            "⬅ Back"
        )

        self.btn_back.clicked.connect(
            self.go_back
        )
        
        self.btn_save.clicked.connect(
            self.save_settings
        )
        
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Theme"))
        layout.addWidget(self.theme_box)

        layout.addWidget(QLabel("Language"))
        layout.addWidget(self.language_box)
        
        layout.addWidget(QLabel("Voice"))
        layout.addWidget(self.voice_box)
        layout.addWidget(QLabel("Change Password"))

        layout.addWidget(self.old_password)

        layout.addWidget(self.new_password)

        layout.addWidget(self.confirm_password)

        layout.addWidget(self.btn_change_password)
        layout.addWidget(QLabel("AI Model"))
        layout.addWidget(self.model_box)

        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_back)

        self.setLayout(layout)

        self.load_saved_settings()
    
    def go_back(self):

        if self.navigator:
            self.navigator.go_back()

   
    def save_settings(self):

        save_settings(

            self.theme_box.currentText(),

            self.language_box.currentText(),

            self.voice_box.currentText(),

            self.model_box.currentText()
        )

        QMessageBox.information(
            self,
            "Saved",
            "Settings Saved Successfully"
        )

        

    def load_saved_settings(self):

        data = load_settings()

        if not data:
            return

        theme, language, voice, model = data

        self.theme_box.setCurrentText(theme)

        self.language_box.setCurrentText(language)

        self.voice_box.setCurrentText(voice)   

        self.model_box.setCurrentText(model)

    def change_password(self):

        old_password = self.old_password.text()

        new_password = self.new_password.text()

        confirm_password = self.confirm_password.text()

        if not old_password:
            QMessageBox.warning(
             self,
                "Error",
                "Enter old password"
            )
            return

        if not new_password:
            QMessageBox.warning(
                self,
                "Error",
                "Enter new password"
            )
            return

        if new_password != confirm_password:

            QMessageBox.warning(
                self,
                "Error",
                "Passwords do not match"
            )

            return

        success = change_password(
            self.username,
            old_password,
            new_password
        )

        if success:

            QMessageBox.information(
                self,
                "Success",
                "Password changed successfully"
            )

            self.old_password.clear()
            self.new_password.clear()
            self.confirm_password.clear()

        else:

            QMessageBox.warning(
                self,
                "Error",
                "Old password is incorrect"
            )
from PyQt6.QtWidgets import *
from settings_manager import *

class SettingsWindow(QWidget):

    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator

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

        self.voice_check = QCheckBox(
            "Enable Voice"
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

        layout.addWidget(self.voice_check)

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

            int(
                self.voice_check.isChecked()
            ),

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

        self.voice_check.setChecked(
            bool(voice)
    )   

        self.model_box.setCurrentText(model)

        
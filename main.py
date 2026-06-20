import sys
from PyQt6.QtWidgets import QApplication
from navigator import Navigator
from login import LoginWindow
from database import create_tables
from settings_manager import load_settings
from theme_manager import get_theme
from ollama_manager import ensure_ollama
import ollama

try:

    ollama.show("qwen2.5:3b")

except:

    print("Downloading model...")

    # ollama.pull("qwen2.5:7b")

create_tables()

ensure_ollama()

app = QApplication(sys.argv)

data = load_settings()

if data:

    theme, language, voice, model = data

    app.setStyleSheet(
        get_theme(theme)
    )

navigator = Navigator()

login = LoginWindow(navigator)

navigator.addWidget(login)
navigator.show()

sys.exit(app.exec())


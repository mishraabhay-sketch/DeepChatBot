from PyQt6.QtWidgets import *
from chatbot import get_answer
from voice import speak
print(speak)
from voice_input import listen
from history import save_chat, get_history
from import_manager import (import_any_file, get_imported_files, delete_imported_file)
from PyQt6.QtWidgets import QComboBox
from settings_manager import (save_settings,load_settings,get_setting)
from settings_window import SettingsWindow
from about_window import AboutWindow
from memory_manager import save_conversation
from memory_extractor import extract_memory
from memory_manager import save_memory
from ai_brain import detect_language
from PyQt6.QtCore import Qt
from database import get_user_role
import sys
import threading


class ChatBotGUI(QWidget):

    def __init__(self, navigator=None, username=None):
        super().__init__()
        print("CURRENT USER =", username)
        self.navigator = navigator
        self.username = username
        self.setWindowTitle("🤖 Chat Bot")
        self.resize(1000, 650)
        self.role = get_user_role(
            self.username
        )

        print(
            "CURRENT ROLE =",
            self.role
        )
        self.file_box = QComboBox()
        
        self.file_list = QListWidget()

        self.load_files()
        # =====================
        # Sidebar
        # =====================

        self.history_list = QListWidget()
        self.history_list.setMaximumWidth(250)

        self.new_chat_btn = QPushButton("➕ New Chat")
        self.new_chat_btn.clicked.connect(self.new_chat)

        # self.pdf_btn = QPushButton("📄 Import PDF")
        # self.pdf_btn.clicked.connect(self.import_pdf_file)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(QLabel("🕒 Chat History"))
        sidebar_layout.addWidget(self.history_list)
        sidebar_layout.addWidget(self.new_chat_btn)
        # sidebar_layout.addWidget(self.pdf_btn)
        if self.role in [
            "founder",
            "super_admin",
            "admin"
        ]:

            sidebar_layout.addWidget(
                QLabel("📁 Imported Files")
            )

            sidebar_layout.addWidget(
                self.file_list
            )
        
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)


        # =====================
        # Chat Area
        # =====================

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        self.chat.append(
        "<p style='color:yellow'>🤖 AI is thinking...</p>"
        )
        QApplication.processEvents()

        self.language_box = QComboBox()

        self.language_box.addItems([
            "English",
            "Hindi",
            "Hinglish",
            "Roman Hindi"]       
        )

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type your message...")

        self.input.returnPressed.connect(
            self.send_message
        )

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)

        self.mic_btn = QPushButton("🎤")
        self.mic_btn.clicked.connect(self.voice_input)

        self.btn_back = QPushButton("⬅ Back")
        self.btn_settings = QPushButton("⚙")
        self.btn_about = QPushButton("ℹ")
        
        if self.role in [
            "founder",
            "super_admin",
            "admin"
        ]:

            self.btn_delete = QPushButton("Delete File")

            self.btn_delete.clicked.connect(
                self.delete_selected_file
            )
        
        self.btn_back.clicked.connect(
            self.close
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
        

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.input)
        bottom_layout.addWidget(self.mic_btn)
        bottom_layout.addWidget(self.send_btn)
        
        
        if self.role in [
            "founder",
            "super_admin",
            "admin"
        ]:
            bottom_layout.addWidget(self.file_box)

            bottom_layout.addWidget(self.btn_delete)
        
        bottom_layout.addWidget(self.btn_settings)
        bottom_layout.addWidget(self.btn_back)
        bottom_layout.addWidget(self.btn_about)
        
        chat_layout = QVBoxLayout()
        chat_layout.addWidget(self.chat)
        chat_layout.addLayout(bottom_layout)
        chat_layout.addWidget(self.language_box)
        chat_widget = QWidget()
        chat_widget.setLayout(chat_layout)

        # =====================
        # Main Layout
        # =====================

        main_layout = QHBoxLayout()

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(chat_widget)

        self.setLayout(main_layout)

        # =====================
        # Theme
        # =====================

        self.setStyleSheet("""
QWidget{
background-color:#0f0f0f;
color:white;
font-family:'Segoe UI';
}

QTextEdit{
    background-color:#161616;
    border:2px solid #00ffff;
    border-radius:15px;
    color:#00ffff;
    padding:10px;
}

QLineEdit{
    background-color:#1a1a1a;
    border:2px solid #00ff99;
    border-radius:15px;
    color:white;
    padding:8px;
}

QPushButton{
    background-color:#111111;
    border:2px solid #00ffff;
    border-radius:15px;
    color:#00ffff;
    padding:8px;
    font-weight:bold;
}

QPushButton:hover{
    border:2px solid #00ff99;
}

QListWidget{
    background-color:#161616;
    border:2px solid #00ffff;
    border-radius:15px;
    color:white;
}
""")

        self.load_history()

    # =====================
    # Load History
    # =====================

    def load_history(self):

        self.history_list.clear()

        rows = get_history(self.username)

        for row in rows:

            chat_id = row[0]
            question = row[1]

            self.history_list.addItem(
                f"{chat_id}: {question[:30]}"
            )

    # =====================
    # New Chat
    # =====================

    def new_chat(self):

        self.chat.clear()

        self.chat.append("""
            <h2 style='color:#00ffff'>
            🤖 AI Online
            </h2>
        """)

    # =====================
    # Voice Input
    # =====================

    def voice_input(self):
        # print("STARTING VOICE THREAD")

        # threading.Thread(
        #     target=speak,
        #     args=(answer, voice),
        #     daemon=True
        #     ).start()

        print("VOICE THREAD STARTED")
        print("MIC BUTTON PRESSED")

        question = listen()

        print("RECEIVED =", question)

        if question:

            self.input.setText(question)

            self.send_message()

    # =====================
    # Send Message
    # =====================

    def send_message(self):
        
        print("SEND MESSAGE USER =", self.username)

        question = self.input.text().strip()

        detected_language = detect_language(question)

        selected_language = self.language_box.currentText()

        if selected_language == "Auto":
            language = detected_language
        else:
            language = selected_language
        
        # language = detect_language(question)
        
        if self.language_box.currentText() != "Auto":
            language = self.language_box.currentText()
        
        print("DETECTED LANGUAGE =", language)
        
        memories = extract_memory(question)
        
        for key, value in memories:

            save_memory(
                self.username,
                key,
                value
            )

            print(
                "MEMORY SAVED:",
                key,
                value
            )
        
        if not question:
            return


        print("GUI LANGUAGE =", language)
        print("FINAL LANGUAGE BEFORE GET_ANSWER =", language)
        
        answer = get_answer(
            question,
            language,
            self.username,
        )
        
        print("VOICE =", get_setting("voice"))
        
        voice = get_setting("voice") # pyright: ignore[reportUndefinedVariable]
        print("VOICE =", voice)
        print("STARTING VOICE THREAD")
        threading.Thread(
            target=speak,
            args=(answer, voice),
            daemon=True
        ).start()
        print("VOICE THREAD STARTED")
        
        save_chat(self.username, question, answer)
        print("SAVING CHAT FOR =", self.username)
        save_conversation(
            self.username,
            question,
            answer
        )
        
        speak(answer)

        language = self.language_box.currentText()

        self.chat.append(
            f"<p style='color:#00ff99'><b>👤 You:</b> {question}</p>"
        )

        self.chat.append(
            f"<p style='color:#00ffff'><b>🤖 AI:</b> {answer}</p>"
        )

        self.input.clear()

        self.load_history()
    

    def go_back(self):

        if self.navigator:

            self.navigator.go_back()
    
    def open_about(self):

        self.navigator.show_page(
            AboutWindow(self.navigator)
        )
    

    def delete_selected_file(self):

        file_name = self.file_box.currentText()
        
        if not file_name:
            return

        reply = QMessageBox.question(
            self,
            "Delete",
            f"Delete {file_name} ?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            delete_imported_file(file_name)

            QMessageBox.information(
                self,
                "Success",
                "File Deleted Successfully"
            )

            self.load_files()

    def load_files(self):

        self.file_list.clear()

        files = get_imported_files()

        for file_id, file_name in files:

            item = QListWidgetItem(file_name)

            item.setData(
                Qt.ItemDataRole.UserRole,
                file_id
            )

            self.file_list.addItem(item)
            self.file_box.addItem(file_name)
    
    def open_settings(self):

        self.navigator.show_page(
            SettingsWindow(self.navigator, self.username)
        )

if __name__ == "__main__":
    import sys


    app = QApplication(sys.argv)

    window = ChatBotGUI()
    window.show()

    sys.exit(app.exec())
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout
)


class AboutWindow(QWidget):

    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator

        self.setWindowTitle("About ChatBot")
        self.resize(700, 500)

        title = QLabel("🤖 ChatBot")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00ffff;
        """)

        info = QTextEdit()
        info.setReadOnly(True)

        info.setHtml("""
        <h2>ChatBot</h2>

        <p>
        A Personal Artificial Intelligence Assistant
        developed for intelligent conversation,
        knowledge management and administration.
        </p>

        <hr>

        <h3>Founder & Creator</h3>
        <p><b>Sahil & Abhay Mishra</b></p>

        <h3>Original Idea By</h3>
        <p><b>Sahil</b></p>

        <h3>Project Type</h3>
        <p>Desktop AI Assistant Platform</p>

        <h3>Version</h3>
        <p>Version 1.0</p>

        <h3>Technology Stack</h3>

        <ul>
            <li>Python</li>
            <li>PyQt6</li>
            <li>SQLite</li>
            <li>Ollama</li>
            <li>Qwen AI</li>
        </ul>

        <hr>

        <p>
        This software was originally conceived,
        designed and developed by
        <b>Abhay Mishra</b>.
        </p>

        <p>
        Creator information is permanently embedded
        as part of the project identity.
        </p>
        """)

        btn_back = QPushButton("⬅ Back")
        btn_back.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(btn_back)

        self.setLayout(layout)

    def go_back(self):
        if self.navigator:
            self.navigator.go_back()
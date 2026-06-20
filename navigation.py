from PyQt6.QtWidgets import *

class NavigationWindow(QWidget):

    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator
        
        self.resize(1200, 800)

        self.stack = QStackedWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.stack)

        self.setLayout(layout)

    def add_page(self, page):
        self.stack.addWidget(page)

    def show_page(self, page):
        self.stack.setCurrentWidget(page)
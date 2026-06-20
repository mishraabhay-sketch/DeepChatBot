from PyQt6.QtWidgets import QStackedWidget


class Navigator(QStackedWidget):

    def __init__(self, navigator=None):
        super().__init__()

        
        self.history = []

    def show_page(self, page):

        current = self.currentWidget()

        if current:
            self.history.append(current)

        self.addWidget(page)

        self.setCurrentWidget(page)

    def go_back(self):

        if not self.history:
            return

        page = self.history.pop()

        self.setCurrentWidget(page)
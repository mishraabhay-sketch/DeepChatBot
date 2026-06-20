from PyQt6.QtWidgets import *
from auth import get_super_admins
from auth import (get_super_admins,delete_user,update_role)

class ManageSuperAdmins(QWidget):

    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator

        self.setWindowTitle(
            "Manage Super Admins"
        )

        self.resize(700, 500)

        self.btn_delete = QPushButton(
            "🗑 Delete Selected Super Admin"
        )

        self.btn_demote = QPushButton(
            "⬇ Demote To Admin"
        )

        self.btn_back = QPushButton("⬅ Back")
        self.btn_back.clicked.connect(self.go_back)
        
        
        self.btn_delete.clicked.connect(
            self.delete_selected
        )
        
        self.btn_demote.clicked.connect(
            self.demote_admin
        )

        

        self.table = QTableWidget()

        layout = QVBoxLayout()

        layout.addWidget(self.table)
        
        layout.addWidget(self.btn_demote)
        
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):

        data = get_super_admins()

        self.table.setColumnCount(3)

        self.table.setHorizontalHeaderLabels(
            ["ID", "Username", "Role"]
        )

        self.table.setRowCount(len(data))

        for row_num, row_data in enumerate(data):

            for col_num, value in enumerate(row_data):

                self.table.setItem(
                    row_num,
                    col_num,
                    QTableWidgetItem(str(value))
                )

    def delete_selected(self):

        row = self.table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Error",
                "Select a Super Admin"
            )
            return

        user_id = int(
             self.table.item(row, 0).text()
        )

        delete_user(user_id)

        QMessageBox.information(
            self,
            "Success",
            "Super Admin Deleted"
        )

        self.load_data()

    def demote_admin(self):

        row = self.table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Error",
                "Select Super Admin"
            )
            return

        user_id = int(
            self.table.item(row, 0).text()
        )

        update_role(
            user_id,
            "admin"
        )

        QMessageBox.information(
            self,
            "Success",
            "Converted To Admin"
        )

        self.load_data()

    def go_back(self):
        
        if self.navigator:
        
            self.navigator.go_back()
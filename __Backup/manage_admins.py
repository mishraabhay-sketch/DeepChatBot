from PyQt6.QtWidgets import *

from auth import (
get_admins,
delete_user,
update_role
)

class ManageAdmins(QWidget):


    def __init__(self, navigator=None):
        super().__init__()

        self.navigator = navigator

        self.setWindowTitle(
        "Manage Admins"
        )

        self.resize(800, 600)

        self.table = QTableWidget()

        self.btn_delete = QPushButton(
            "🗑 Delete Admin"
        )

        self.btn_promote = QPushButton(
            "⬆ Promote To Super Admin"
        )

        self.btn_demote = QPushButton(
            "⬇ Demote To User"
        )

        self.btn_delete.clicked.connect(
            self.delete_admin
        )

        self.btn_promote.clicked.connect(
            self.promote_admin
        )

        self.btn_demote.clicked.connect(
            self.demote_admin
        )
        
        self.btn_back = QPushButton("⬅ Back")
        self.btn_back.clicked.connect(self.go_back)
        

        layout = QVBoxLayout()

        layout.addWidget(self.table)

        layout.addWidget(self.btn_promote)
        layout.addWidget(self.btn_demote)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_back)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):

        data = get_admins()

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

    def get_selected_id(self):

        row = self.table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Error",
                "Select Admin"
            )

            return None

        return int(
            self.table.item(row, 0).text()
        )   

    def delete_admin(self):

        user_id = self.get_selected_id()

        if user_id is None:
            return

        delete_user(user_id)

        QMessageBox.information(
            self,
            "Success",
            "Admin Deleted"
        )

        self.load_data()

    def promote_admin(self):

        user_id = self.get_selected_id()

        if user_id is None:
            return

        update_role(
            user_id,
            "super_admin"
        )

        self.load_data()

    def demote_admin(self):

        user_id = self.get_selected_id()

        if user_id is None:
            return

        update_role(
            user_id,
            "user"
        )

        self.load_data()


    def go_back(self):

        if self.navigator:
            self.navigator.go_back()

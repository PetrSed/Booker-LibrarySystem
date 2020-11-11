import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMainWindow, \
    QCompleter, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sqlite3
import datetime


class AddAuthorToBaseForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(700, 300, 320, 85)
        self.setWindowTitle('Добавление автора в базу')

        name_label = QLabel(self)
        name_label.setText("Фамилия И.О.: ")
        name_label.move(40, 20)
        self.name_input = QLineEdit(self)
        self.name_input.move(130, 19)

        add_button = QPushButton('Добавить', self)
        add_button.resize(add_button.sizeHint())
        add_button.move(125, 50)
        add_button.clicked.connect(self.add_author_to_base)

    def add_author_to_base(self):
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        author_name = self.name_input.text()

        db_cur.execute(f"""INSERT INTO Authors (name)
                           VALUES ('{author_name}');""")
        db.commit()
        db.close()
        self.open_success_form()

    def open_success_form(self):
        self.form = SuccessForm(self)
        self.form.show()

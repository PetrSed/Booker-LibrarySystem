import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMainWindow, \
    QCompleter, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sqlite3
import datetime


class GiveBookForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 300, 415)
        self.setWindowTitle('Выдача книги')
        self.give_barcodes = []

        full_name_label = QLabel(self)
        full_name_label.setText("ФИО Ученика: ")
        full_name_label.move(40, 20)
        self.full_name_input = QLineEdit(self)
        self.full_name_input.move(132, 19)
        completer = QCompleter(self.get_students(), self.full_name_input)
        self.full_name_input.setCompleter(completer)

        self.table = QTableWidget(self)
        self.table.setColumnCount(1)
        self.table.setRowCount(10)
        self.table.move(20, 50)
        self.table.setFixedSize(260, 325)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.table.setHorizontalHeaderLabels(["Штрихкод книги"])
        self.table.itemChanged.connect(self.add_barcode)
        self.table.setRangeSelected(QTableWidgetSelectionRange(0, 1, 1, 1), True)

        add_button = QPushButton('Выдать', self)
        add_button.resize(add_button.sizeHint())
        add_button.move(110, 385)
        add_button.clicked.connect(self.add_issue_to_base)

    def add_barcode(self, item):
        self.give_barcodes.append((item.text()))

    def get_students(self):
        students = list()
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        result = db_cur.execute("""SELECT name, surname, patronymic, id FROM Students""").fetchall()
        for elem in result:
            students.append(f'{elem[1]} {elem[0]} {elem[2]} ({elem[3]})')
        db.close()
        return students

    def add_issue_to_base(self):
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        for book_barcode in self.give_barcodes:
            book_id = self.get_book_id(book_barcode)
            student_id = self.get_student_id(self.full_name_input.text())
            issue_date = datetime.datetime.now().strftime("%d-%m-%Y")
            issue_status_id = 1
            db_cur.execute(f"""INSERT INTO Issue (bookID, studentID, issueDate, issueStatusID)
                           VALUES ('{book_id}', '{student_id}', '{issue_date}', '{issue_status_id}');""")
            db.commit()
        db.close()
        self.open_success_form()

    def open_success_form(self):
        self.form = SuccessForm(self)
        self.form.show()

    def get_book_id(self, book_barcode):

        db = sqlite3.connect(base_name)
        db_cur = db.cursor()

        result = db_cur.execute(f"""SELECT id FROM Books
                                    WHERE barcode = '{book_barcode}'""")
        for elem in result:
            return elem[0]

    def get_student_id(self, student_label):
        student_id_start = student_label.find('(')
        student_id_final = student_label.find(')')
        student_id = student_label[student_id_start + 1:student_id_final]
        return student_id

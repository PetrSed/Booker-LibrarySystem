import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMainWindow, \
    QCompleter, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sqlite3
import datetime
from windows import *


class ReturnBookForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 300, 415)
        self.setWindowTitle('Возврат книги')
        self.return_barcodes = []

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

        return_button = QPushButton('Возврат', self)
        return_button.resize(return_button.sizeHint())
        return_button.move(110, 385)
        return_button.clicked.connect(self.return_book)

    def add_barcode(self, item):
        self.return_barcodes.append((item.text()))

    def open_success_form(self):
        self.form = Success.SuccessForm(self)
        self.form.show()

    def return_book(self):
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        student_id = self.get_student_id(self.full_name_input.text())
        for book_barcode in self.return_barcodes:
            get_book_id = db_cur.execute(f"""Select id from Books
                                             WHERE barcode = {book_barcode}""").fetchall()
            get_issues_id = db_cur.execute(f"""Select id from Issue
                                             WHERE bookID = {get_book_id[0][0]} and studentID = {student_id}\
                                              and issueStatusId = 1""").fetchall()
            db_cur.execute(f'''UPDATE Issue
                              SET issueStatusId = 0
                              WHERE id = {get_issues_id[0][0]}''')
            db.commit()
        self.open_success_form()

    def get_students(self):
        students = list()
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        result = db_cur.execute("""SELECT name, surname, patronymic, id FROM Students""").fetchall()
        for elem in result:
            students.append(f'{elem[1]} {elem[0]} {elem[2]} ({elem[3]})')
        db.close()
        return students

    def get_student_id(self, student_label):
        student_id_start = student_label.find('(')
        student_id_final = student_label.find(')')
        student_id = student_label[student_id_start + 1:student_id_final]
        return student_id

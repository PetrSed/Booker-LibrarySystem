import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMainWindow, \
    QCompleter, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sqlite3
import datetime


class ViewIssuesForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(0, 0, 1000, 450)
        self.setWindowTitle('Просмотр выдач:')

        window_name_label = QLabel(self)
        window_name_label.setText("Просмотр выдач")
        window_name_label.move(430, 20)

        full_name_label = QLabel(self)
        full_name_label.setText("ФИО Ученика: ")
        full_name_label.move(370, 40)
        self.full_name_input = QLineEdit(self)
        self.full_name_input.move(450, 39)
        completer = QCompleter(self.get_students(), self.full_name_input)
        self.full_name_input.setCompleter(completer)

        execute_button = QPushButton('Запрос', self)
        execute_button.resize(execute_button.sizeHint())
        execute_button.move(440, 70)
        execute_button.clicked.connect(self.load_table)

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setRowCount(10)
        self.table.move(20, 100)
        self.table.setFixedSize(900, 325)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(["ФИО ученика", "Автор книги", "Название книги", "Штрихкод книги",
                                              "Дата выдачи"])

        def load_table(self):
            self.table.setRowCount(len(self.order))
            print(here)
            for row in range(len(self.order)):
                self.table.setItem(row, 0, QTableWidgetItem(str(self.order[row])))

    def load_table(self):
        information = self.get_information()
        self.table.setRowCount(len(information))
        for row in range(len(information)):
            for col in range(5):
                a = information[row][col]
                self.table.setItem(row, col, QTableWidgetItem(str(a)))
        self.table.resizeColumnsToContents()

    def get_students(self):
        students = list()
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        result = db_cur.execute("""SELECT name, surname, patronymic, id FROM Students""").fetchall()
        for elem in result:
            students.append(f'{elem[1]} {elem[0]} {elem[2]} ({elem[3]})')
        db.close()
        return students

    def get_information(self):
        issues_info = list()
        student_id = self.get_student_id(self.full_name_input.text())
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        execute_one = db_cur.execute(f"""SELECT bookID, issueDate, issueStatusId FROM Issue
                                   WHERE studentID = {student_id} and issueStatusId = 1""").fetchall()
        for res in execute_one:
            execute_two = db_cur.execute(f"""SELECT name, surname, patronymic FROM Students
                                         where id = {student_id}""").fetchone()
            student = f'{execute_two[1]} {execute_two[0]} {execute_two[2]}'
            execute_three = db_cur.execute(f"""SELECT name, barcode, authorId FROM Books
                                         where id = {res[0]}""").fetchone()
            barcode, book_name, author_id = execute_three[1], execute_three[0], execute_three[2]
            author_name = db_cur.execute(f"""SELECT name FROM Authors
                                         where id = {author_id}""").fetchone()[0]
            issue_date = res[1]

            issues_info.append(list([student, author_name, book_name, barcode, issue_date]))
        return issues_info

    def get_student_id(self, student_label):
        student_id_start = student_label.find('(')
        student_id_final = student_label.find(')')
        student_id = student_label[student_id_start + 1:student_id_final]
        return student_id

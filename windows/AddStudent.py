import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMainWindow, \
    QCompleter, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sqlite3
import datetime


class AddStudentToBaseForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(700, 300, 310, 210)
        self.setWindowTitle('Добавление ученика в базу')

        name_label = QLabel(self)
        name_label.setText("Имя: ")
        name_label.move(40, 20)
        self.name_input = QLineEdit(self)
        self.name_input.move(132, 19)

        surname_label = QLabel(self)
        surname_label.setText("Фамилия: ")
        surname_label.move(40, 50)
        self.surname_input = QLineEdit(self)
        self.surname_input.move(132, 49)

        patronymic_label = QLabel(self)
        patronymic_label.setText("Отчество: ")
        patronymic_label.move(40, 80)
        self.patronymic_input = QLineEdit(self)
        self.patronymic_input.move(132, 79)

        student_card_id_label = QLabel(self)
        student_card_id_label.setText("Номер уч.билета: ")
        student_card_id_label.move(40, 110)
        self.student_card_id_input = QLineEdit(self)
        self.student_card_id_input.move(132, 109)

        birthday_date_label = QLabel(self)
        birthday_date_label.setText("Дата рождения: ")
        birthday_date_label.move(40, 140)
        self.birthday_date_input = QLineEdit(self)
        self.birthday_date_input.move(132, 139)

        add_button = QPushButton('Добавить', self)
        add_button.resize(add_button.sizeHint())
        add_button.move(120, 173)
        add_button.clicked.connect(self.add_student_to_base)

    def add_student_to_base(self):
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        student_name = self.name_input.text()
        student_surname = self.surname_input.text()
        student_patronymic = self.patronymic_input.text()
        student_card_id = self.student_card_id_input.text()
        student_birthday_date = self.birthday_date_input.text()

        db_cur.execute(f"""INSERT INTO Students (name, surname, patronymic, studentCardId, birthdayDate)
                           VALUES ('{student_name}', '{student_surname}', '{student_patronymic}', '{student_card_id}', '{student_birthday_date}');""")
        db.commit()
        db.close()
        self.open_success_form()

    def open_success_form(self):
        self.form = SuccessForm(self)
        self.form.show()

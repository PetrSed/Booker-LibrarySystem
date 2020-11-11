import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMainWindow, \
    QCompleter, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sqlite3
import datetime


class AddBookToBaseForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(700, 300, 320, 220)
        self.setWindowTitle('Добавление книги в базу')
        self.now_book_type = 'Художественная'

        barcode_label = QLabel(self)
        barcode_label.setText("Штрихкод: ")
        barcode_label.move(60, 20)
        self.barcode_input = QLineEdit(self)
        self.barcode_input.move(122, 19)

        name_label = QLabel(self)
        name_label.setText("Название: ")
        name_label.move(60, 50)
        self.name_input = QLineEdit(self)
        self.name_input.move(122, 49)

        author_label = QLabel(self)
        author_label.setText("Автор: ")
        author_label.move(60, 80)
        self.author_input = QLineEdit(self)
        self.author_input.move(122, 79)
        completer = QCompleter(self.get_authors(), self.author_input)
        self.author_input.setCompleter(completer)

        type_label = QLabel(self)
        type_label.setText("Тип: ")
        type_label.move(60, 110)
        self.type_input = QComboBox(self)
        self.type_input.addItems(self.get_book_type())
        self.type_input.move(122, 109)
        self.type_input.activated[str].connect(self.change_now_book_type)

        class_label = QLabel(self)
        class_label.setText("Класс: ")
        class_label.move(60, 140)
        self.class_input = QLineEdit(self)
        self.class_input.move(122, 139)

        add_button = QPushButton('Добавить', self)
        add_button.resize(add_button.sizeHint())
        add_button.move(120, 180)
        add_button.clicked.connect(self.add_book_to_base)

    def change_now_book_type(self, text):
        self.now_book_type = text

    def get_book_type(self):
        types = list()
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        result = db_cur.execute("""SELECT name FROM BookType""").fetchall()
        for elem in result:
            types.append(elem[0])
        db.close()
        return types

    def get_authors(self):
        authors = list()
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        result = db_cur.execute("""SELECT name FROM Authors""").fetchall()
        for elem in result:
            authors.append(elem[0])
        db.close()
        return authors

    def add_book_to_base(self):
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        book_barcode = self.barcode_input.text()
        book_name = self.name_input.text()
        book_author_id = self.get_author_id(self.author_input.text())
        book_type_id = self.get_book_type_id(self.now_book_type)
        book_class = self.class_input.text()
        db_cur.execute(f"""INSERT INTO Books (barcode, name, authorId, typeId, class)
                           VALUES ('{book_barcode}', '{book_name}', '{book_author_id}', '{book_type_id}', \
        '{book_class}');""")
        db.commit()
        db.close()
        self.open_SuccessForm()

    def open_SuccessForm(self):
        self.form = SuccessForm(self)
        self.form.show()

    def get_author_id(self, book_author_name):

        db = sqlite3.connect(base_name)
        db_cur = db.cursor()

        result = db_cur.execute(f"""SELECT id FROM Authors
                                    WHERE name = '{book_author_name}'""")
        for elem in result:
            return elem[0]

    def get_book_type_id(self, book_id_name):
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()

        result = db_cur.execute(f"""SELECT id FROM BookType
                                    WHERE name = '{book_id_name}'""")
        for elem in result:
            return elem[0]

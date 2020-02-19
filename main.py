import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMainWindow, \
    QCompleter, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sqlite3
import datetime

base_name = 'testBase.db'
program_name = 'Библиотека 2.0'


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 300, 155)
        self.setWindowTitle(program_name)
        self.setWindowIcon(QIcon('icon.png'))
        main_menu = self.menuBar()
        add_to_base_btn = main_menu.addMenu('Добавить в базу')

        add_book_to_base_btn = QAction('Добавить книгу в базу', self)
        add_book_to_base_btn.triggered.connect(self.open_add_book_to_base_form)
        add_to_base_btn.addAction(add_book_to_base_btn)

        add_author_to_base_btn = QAction('Добавить автора в базу', self)
        add_author_to_base_btn.triggered.connect(self.open_add_author_to_base_form)
        add_to_base_btn.addAction(add_author_to_base_btn)

        add_student_to_base_btn = QAction('Добавить ученика в базу', self)
        add_student_to_base_btn.triggered.connect(self.open_add_student_to_base_form)
        add_to_base_btn.addAction(add_student_to_base_btn)

        add_book_type_to_base_btn = QAction('Добавить тип книги в базу', self)
        add_book_type_to_base_btn.triggered.connect(self.open_add_book_type_to_base_form)
        add_to_base_btn.addAction(add_book_type_to_base_btn)

        greeting = QLabel(self)
        greeting.setText(program_name)
        greeting.move(109, 20)

        give_book_btn = QPushButton('Выдать книгу', self)
        give_book_btn.resize(220, 25)
        give_book_btn.move(40, 50)
        give_book_btn.clicked.connect(self.open_give_book_form)

        view_issues_btn = QPushButton('Вернуть книгу', self)
        view_issues_btn.resize(220, 25)
        view_issues_btn.move(40, 85)
        view_issues_btn.clicked.connect(self.return_book_form)

        return_book_btn = QPushButton('Просмотр выдач', self)
        return_book_btn.resize(220, 25)
        return_book_btn.move(40, 120)
        return_book_btn.clicked.connect(self.open_view_issues_form)

    def open_add_book_to_base_form(self):
        self.form = AddBookToBaseForm(self)
        self.form.show()

    def open_add_author_to_base_form(self):
        self.form = AddAuthorToBaseForm(self)
        self.form.show()

    def open_add_student_to_base_form(self):
        self.form = AddStudentToBaseForm(self)
        self.form.show()

    def open_add_book_type_to_base_form(self):
        self.form = AddBookTypeToBaseForm(self)
        self.form.show()

    def open_give_book_form(self):
        self.form = GiveBookForm(self)
        self.form.show()

    def open_view_issues_form(self):
        self.form = ViewIssuesForm(self)
        self.form.show()

    def return_book_form(self):
        self.form = ReturnBookForm(self)
        self.form.show()


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


class AddBookTypeToBaseForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(700, 300, 320, 85)
        self.setWindowTitle('Добавление типа книги в базу')

        name_label = QLabel(self)
        name_label.setText("Название типа: ")
        name_label.move(40, 20)
        self.name_input = QLineEdit(self)
        self.name_input.move(130, 19)

        add_button = QPushButton('Добавить', self)
        add_button.resize(add_button.sizeHint())
        add_button.move(125, 50)
        add_button.clicked.connect(self.add_book_type_to_base)

    def add_book_type_to_base(self):
        db = sqlite3.connect(base_name)
        db_cur = db.cursor()
        book_type_name = self.name_input.text()
        db_cur.execute(f"""INSERT INTO BookType (name)
                           VALUES ('{book_type_name}');""")
        db.commit()
        db.close()
        self.open_success_form()

    def open_success_form(self):
        self.form = SuccessForm(self)
        self.form.show()


class SuccessForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 100, 100)
        self.setWindowTitle('Статус:')
        lbl = QLabel(self)
        lbl.setText('Успех!')
        lbl.move(30, 30)
        lbl.adjustSize()


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
        self.form = SuccessForm(self)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())

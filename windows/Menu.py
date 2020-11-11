class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 300, 155)
        self.setWindowTitle(program_name)
        self.setWindowIcon(QIcon('pics/icon.png'))
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
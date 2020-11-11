import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMainWindow, \
    QCompleter, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sqlite3
import datetime


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

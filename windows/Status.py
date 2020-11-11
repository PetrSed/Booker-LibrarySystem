import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMainWindow, \
    QCompleter, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication, Qt
import sqlite3
import datetime


class Status(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 220, 140)
        self.setWindowTitle(self.tr('Status:'))

        status_label = QLabel(self.tr(args[1]), self)
        status_label.resize(220, 50)
        status_label.move(0, 40)
        status_label.setFont(QFont("Arial", 20))
        status_label.setAlignment(Qt.AlignCenter)

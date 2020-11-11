import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMainWindow, \
    QCompleter, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sqlite3
import datetime
from helpers.settings import check_settings, get_settings
from windows.Menu import Main
from windows.Settings import Settings


def main():
    app = QApplication(sys.argv)
    if check_settings():
        settings = get_settings()
        window = Main(settings)
        window.show()
    else:
        window = Settings()
        window.show()
    sys.exit(app.exec())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec())

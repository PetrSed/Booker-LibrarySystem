import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QComboBox, QAction, QMainWindow, \
    QCompleter, QTableWidget, QTableWidgetItem, QTableWidgetSelectionRange, QGridLayout
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QFont
import sqlite3
import datetime
from PyQt5.QtCore import QCoreApplication, Qt
from windows import *
from helpers.settings import is_first_start, get_settings
import configparser
from windows.Status import Status


class Settings(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 300, 185)
        self.setWindowTitle(self.tr("Settings"))
        self.setWindowIcon(QIcon('pics/icon.png'))

        settings_label = QLabel(self.tr("Settings"), self)
        settings_label.resize(300, 50)
        settings_label.move(0, 10)
        settings_label.setFont(QFont("Arial", 20))
        settings_label.setAlignment(Qt.AlignCenter)

        api_label = QLabel(self.tr("Booker API Server:"), self)
        api_label.resize(300, 50)
        api_label.setFont(QFont("Arial", 10))
        api_label.move(15, 70)
        api_label.setAlignment(Qt.AlignLeft)

        self.api_input = QLineEdit(self)
        self.api_input.resize(150, 20)
        self.api_input.move(130, 69)

        connection_type_label = QLabel(self.tr("Connecting to db:"), self)
        connection_type_label.resize(300, 50)
        connection_type_label.setFont(QFont("Arial", 10))
        connection_type_label.move(15, 100)
        connection_type_label.setAlignment(Qt.AlignLeft)

        self.connection_type_box = QComboBox(self)
        self.connection_type_box.resize(150, 20)
        self.connection_type_box.move(130, 99)
        self.connection_type_box.addItem(self.tr("Remote (Booker API)"))
        self.connection_type_box.addItem(self.tr("Local (sqlite)"))
        self.connection_type_box.setCurrentIndex(1)

        if not is_first_start():
            settings = get_settings()
            self.api_input.setText(settings[1])
            self.connection_type_box.setCurrentIndex(int(settings[0]))

        save_btn = QPushButton(self)
        if is_first_start():
            save_btn.setText(self.tr("Start"))
        else:
            save_btn.setText(self.tr("Save"))
        save_btn.resize(save_btn.sizeHint())
        save_btn.move(110, 140)
        save_btn.clicked.connect(self.save)

    def open_status_window(self, status):
        self.status_window = Status(self, status)
        self.status_window.show()

    def save(self):
        config = configparser.ConfigParser()
        config.add_section("Settings")
        config.set("Settings", "api_server", self.api_input.text())
        config.set("Settings", "connection_type", str(self.connection_type_box.currentIndex()))
        with open("config.conf", "w") as config_file:
            config.write(config_file)
        self.open_status_window(self.tr("Success!"))



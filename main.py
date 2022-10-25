import sys
import pandas as pd
import data_analysis as dan

import re
import pyarrow
import tkinter as tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget, QStackedLayout, QHBoxLayout,
)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TTF Data analysis")

        page_layout = QVBoxLayout()
        #button_layout = QHBoxLayout()
        #self.stacklayout = QStackedLayout()

        #page_layout.addLayout(button_layout)
        #page_layout.addLayout(self.stacklayout)

        #TASKS
        self.task_widg = QComboBox()
        self.task_widg.addItems(datas['task'])
        # Sends the current index (position) of the selected item.
        self.task_widg.currentIndexChanged.connect( self.task_index_changed )
        # There is an alternate signal to send the text.
        self.task_widg.editTextChanged.connect( self.task_text_changed )
        page_layout.addWidget(self.task_widg)

        #WORKERS
        self.worker_widg = QComboBox()
        self.worker_widg.addItems(datas['name'])
        self.worker_widg.currentIndexChanged.connect( self.worker_index_changed )
        self.worker_widg.editTextChanged.connect( self.worker_text_changed )
        page_layout.addWidget(self.worker_widg)

        #PRODUCTS
        self.prod_widg = QComboBox()
        self.prod_widg.addItems(datas['product'])
        self.prod_widg.currentIndexChanged.connect(self.prod_index_changed)
        self.prod_widg.editTextChanged.connect(self.prod_text_changed)
        page_layout.addWidget(self.prod_widg)

        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.the_button_was_clicked)
        page_layout.addWidget(self.go_button)


        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

        # button = QPushButton("Press Me!")
        # button.setCheckable(True)
        # button.clicked.connect(self.the_button_was_toggled)
        #
        # # Set the central widget of the Window.
        # self.setCentralWidget(button)


    # total_units_by_month_for_product(df, prod)
    # rate_for_task_for_worker_by_month(df, name, task)
    # avg_efficiency_per_month(df, name, rate)

    def task_index_changed(self, i): # i is an int
        print(i)

    def task_text_changed(self, s): # s is a str
        print(s)

    def worker_index_changed(self, i): # i is an int
        print(i)

    def worker_text_changed(self, s): # s is a str
        print(s)

    def prod_index_changed(self, i): # i is an int
        print(i)

    def prod_text_changed(self, s): # s is a str
        print(s)

    def the_button_was_clicked(self):
        print('x')
        task_text = self.task_widg.currentText()
        worker_text = self.worker_widg.currentText()
        prod_text = self.prod_widg.currentText()

        dan.rate_for_task_for_worker_by_month(df, worker_text, task_text)
        print(prod_text)




#Start the show
###
app = QApplication(sys.argv)
df, datas = dan.main()

window = MainWindow()
window.show()

app.exec()

def main():
    print('x')

if __name__ == '__main__':
    main()





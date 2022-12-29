import sys
import pandas as pd
import data_analysis as dan

import re
import pyarrow
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtCore import QDate
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
    QWidget, QStackedLayout, QHBoxLayout, QGridLayout, QButtonGroup,
)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.monthly = False
        self.selected_month = 6
        self.selected_year = 2022

        self.setWindowTitle("TTF Data analysis")

        #LAYOUT
        page_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.button_group1 = QButtonGroup()
        button_layout2 = QGridLayout()
        self.button_group2 = QButtonGroup()
        #self.stacklayout = QStackedLayout()


        #page_layout.addLayout(self.stacklayout)

        self.title_label = QLabel("Select type of report to generate.\n\n"
                                  "Time Frame Options:\n"
                                  "- Total stats to date\n"
                                  "- Stats for specific month/year\n\n"
                                  "Subject Options:\n"
                                  "- General Report\n"
                                  "- Report on specific worker\n"
                                  "- Report on specific batch ID\n"
                                  "- Report on specific product type\n"
                                  "- Report on specific task\n")
        page_layout.addWidget(self.title_label)



        #CHECKBOX FOR STATS TO DATE
        self.montlhy_or_todate_label = QLabel("Time Frame: ")
        self.todate_button = QRadioButton("To Date")
        self.todate_button.setChecked(True)
        self.monthly_button = QRadioButton("Monthly")

        self.todate_button.toggled.connect(lambda: self.todateMontlhy_buttonState(self.todate_button))
        self.monthly_button.toggled.connect(lambda: self.todateMontlhy_buttonState(self.monthly_button))

        self.button_group1.addButton(self.todate_button)
        self.button_group1.addButton(self.monthly_button)

        page_layout.addWidget(self.montlhy_or_todate_label)
        button_layout.addWidget(self.todate_button)
        button_layout.addWidget(self.monthly_button)


        page_layout.addLayout(button_layout)

        #BUTTONS FOR STATS SUBJECT

        self.subject_label = QLabel("Report Subject:")

        self.general_report_button = QRadioButton("General")
        self.worker_report_button = QRadioButton("Worker")
        self.bid_report_button = QRadioButton("Batch ID")
        self.product_report_button = QRadioButton("Product")
        self.task_report_button = QRadioButton("Task")

        page_layout.addWidget(self.subject_label)
        button_layout2.addWidget(self.general_report_button, 0, 0)
        button_layout2.addWidget(self.worker_report_button, 1, 0)
        button_layout2.addWidget(self.bid_report_button, 1, 1)
        button_layout2.addWidget(self.product_report_button, 2, 0)
        button_layout2.addWidget(self.task_report_button, 2, 1)

        self.button_group2.addButton(self.general_report_button)
        self.button_group2.addButton(self.worker_report_button)
        self.button_group2.addButton(self.bid_report_button)
        self.button_group2.addButton(self.product_report_button)
        self.button_group2.addButton(self.task_report_button)

        page_layout.addLayout(button_layout2)


        #GIVEN DATE
        self.month_input_label = QLabel("Select Month:")
        self.month_input = QDateEdit(self)
        self.month_input.setDate(QDate.currentDate())
        self.month_input.\
            setDateRange(QDate(2022, 5, 31),
                         QDate(QDate.currentDate().year(), QDate.currentDate().month(), QDate.currentDate().daysInMonth()))
        self.month_input.setDisplayFormat('MMM yy')

        month = self.month_input.date().month()
        year = self.month_input.date().year()

        print(df)

        self.month_things_dict = dan.get_things_dict_for_month(month, year, df)

        self.month_input.dateChanged.connect(self.selected_month_year)


        page_layout.addWidget(self.month_input_label)
        page_layout.addWidget(self.month_input)

        self.month_input.setVisible(False)
        self.month_input_label.setVisible(False)

        #TASKS
        self.task_widg = QComboBox()
        self.task_widg.addItems(datas['tasks'])
        # Sends the current index (position) of the selected item.
        self.task_widg.currentIndexChanged.connect( self.task_index_changed )
        # There is an alternate signal to send the text.
        self.task_widg.editTextChanged.connect( self.task_text_changed )
        page_layout.addWidget(self.task_widg)

        #WORKERS
        self.worker_widg = QComboBox()
        self.worker_widg.addItems(datas['names'])
        self.worker_widg.currentIndexChanged.connect( self.worker_index_changed )
        self.worker_widg.editTextChanged.connect( self.worker_text_changed )
        page_layout.addWidget(self.worker_widg)

        #PRODUCTS
        self.prod_widg = QComboBox()
        self.prod_widg.addItems(datas['products'])

        self.prod_widg.currentIndexChanged.connect(self.prod_index_changed)
        self.prod_widg.editTextChanged.connect(self.prod_text_changed)
        page_layout.addWidget(self.prod_widg)



        # self.task_label1 = QLabel(f" Total units done for {self.prod_widg.currentText()} by month ")
        # page_layout.addWidget(self.task_label1)
        # self.go_button1 = QPushButton("Go")
        # self.go_button1.clicked.connect(self.go_button1_click)
        # page_layout.addWidget(self.go_button1)
        #
        # self.task_label2 = QLabel(f" Avg Rate (units/min) for {self.task_widg.currentText()} done by {self.worker_widg.currentText()} per month ")
        # page_layout.addWidget(self.task_label2)
        # self.go_button2 = QPushButton("Go")
        # self.go_button2.clicked.connect(self.go_button2_click)
        # page_layout.addWidget(self.go_button2)
        #
        # self.task_label3 = QLabel(f" Avg Efficiency for {self.worker_widg.currentText()} across all tasks per month ")
        # page_layout.addWidget(self.task_label3)
        # self.go_button3 = QPushButton("Go")
        # self.go_button3.clicked.connect(self.go_button3_click)
        # page_layout.addWidget(self.go_button3)

        self.task_label4 = QLabel("TEST FUNCTION")
        page_layout.addWidget(self.task_label4)
        self.test_button = QPushButton("Go")
        self.test_button.clicked.connect(self.test_button_click)
        page_layout.addWidget(self.test_button)

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


    def todateMontlhy_buttonState(self, b):

        if b.text() == "To Date":
            if b.isChecked():
                print(b.text())
                self.monthly = False
                self.month_input.setVisible(False)
                self.month_input_label.setVisible(False)

                self.task_widg.clear()
                self.worker_widg.clear()
                self.prod_widg.clear()
                self.task_widg.addItems(datas['tasks'])
                self.worker_widg.addItems(datas['names'])
                self.prod_widg.addItems(datas['products'])

        if b.text() == "Monthly":
            if b.isChecked():
                print(b.text())
                self.monthly = True
                self.month_input.setVisible(True)
                self.month_input_label.setVisible(True)

                self.task_widg.clear()
                self.worker_widg.clear()
                self.prod_widg.clear()
                self.task_widg.addItems(self.month_things_dict['tasks'])
                self.worker_widg.addItems(self.month_things_dict['names'])
                self.prod_widg.addItems(self.month_things_dict['products'])

    def selected_month_year(self, m):

        month = self.month_input.date().month()
        year = self.month_input.date().year()

        self.selected_month = month
        self.selected_year = year

        month_things_dict = dan.get_things_dict_for_month(month, year, df)

        self.task_widg.clear()
        self.worker_widg.clear()
        self.prod_widg.clear()
        self.task_widg.addItems(month_things_dict['tasks'])
        self.worker_widg.addItems(month_things_dict['names'])
        self.prod_widg.addItems(month_things_dict['products'])

        print(str(month) + ':' + str(year))

    def task_index_changed(self, i): # i is an int
        # self.task_label1.setText(f" Total units done for {self.prod_widg.currentText()} by month ")
        # self.task_label2.setText(
        #     f" Avg Rate (units/min) for {self.task_widg.currentText()} done by {self.worker_widg.currentText()} per month ")
        # self.task_label3.setText(f" Avg Efficiency for {self.worker_widg.currentText()} across all tasks per month ")
        self.task_label4.setText("TEST FUNCTION")

    def task_text_changed(self, s): # s is a str
        # self.task_label1.setText(f" Total units done for {self.prod_widg.currentText()} by month ")
        # self.task_label2.setText(
        #     f" Avg Rate (units/min) for {self.task_widg.currentText()} done by {self.worker_widg.currentText()} per month ")
        # self.task_label3.setText(f" Avg Efficiency for {self.worker_widg.currentText()} across all tasks per month ")
        self.task_label4.setText("TEST FUNCTION")

    def worker_index_changed(self, i): # i is an int
        # self.task_label1.setText(f" Total units done for {self.prod_widg.currentText()} by month ")
        # self.task_label2.setText(
        #     f" Avg Rate (units/min) for {self.task_widg.currentText()} done by {self.worker_widg.currentText()} per month ")
        # self.task_label3.setText(f" Avg Efficiency for {self.worker_widg.currentText()} across all tasks per month ")
        self.task_label4.setText("TEST FUNCTION")

    def worker_text_changed(self, s): # s is a str
        # self.task_label1.setText(f" Total units done for {self.prod_widg.currentText()} by month ")
        # self.task_label2.setText(
        #     f" Avg Rate (units/min) for {self.task_widg.currentText()} done by {self.worker_widg.currentText()} per month ")
        # self.task_label3.setText(f" Avg Efficiency for {self.worker_widg.currentText()} across all tasks per month ")
        self.task_label4.setText("TEST FUNCTION")

    def prod_index_changed(self, i): # i is an int
        # self.task_label1.setText(f" Total units done for {self.prod_widg.currentText()} by month ")
        # self.task_label2.setText(
        #     f" Avg Rate (units/min) for {self.task_widg.currentText()} done by {self.worker_widg.currentText()} per month ")
        # self.task_label3.setText(f" Avg Efficiency for {self.worker_widg.currentText()} across all tasks per month ")
        self.task_label4.setText("TEST FUNCTION")

    def prod_text_changed(self, s): # s is a str
        # self.task_label1.setText(f" Total units done for {self.prod_widg.currentText()} by month ")
        # self.task_label2.setText(f" Avg Rate (units/min) for {self.task_widg.currentText()} done by {self.worker_widg.currentText()} per month ")
        # self.task_label3.setText(f" Avg Efficiency for {self.worker_widg.currentText()} across all tasks per month ")
        self.task_label4.setText("TEST FUNCTION")


    # def go_button1_click(self):
    #
    #     prod_text = self.prod_widg.currentText()
    #
    #     rates_data = dan.total_units_by_month_for_product(df, prod_text)
    #     print(rates_data)
    #
    # def go_button2_click(self):
    #     print('x')
    #     task_text = self.task_widg.currentText()
    #     worker_text = self.worker_widg.currentText()
    #
    #     rates_data = dan.rate_for_task_for_worker_by_month(df, worker_text, task_text)
    #     print(rates_data)
    #
    # def go_button3_click(self):
    #     print('x')
    #     worker_text = self.worker_widg.currentText()
    #
    #     rates_data = dan.avg_efficiency_per_month(df, worker_text)
    #     print(rates_data)

    def test_button_click(self):
        worker_text = self.worker_widg.currentText()
        task_text = self.task_widg.currentText()
        prod_text = self.prod_widg.currentText()

        # Functionality to be tested...
        # 
        # print(dan.total_hours_worked_by_task_for_worker(df, worker_text))
        # print("By Month")
        # print(dan.total_hours_worked_by_task_for_worker_per_month(df, worker_text))

        # print(dan.rate_for_task_for_worker_by_month(df, worker_text, task_text))

        # # TODO: add field for inputting batch ID
        # print(dan.total_hours_by_product_for_bid(df, "220622PRMG"))
        # print(dan.average_hours_by_product_per_month_for_bid(df, "220622PRMG"))

        # print(dan.hours_for_workers_having_worked_on_bid_by_product(df, "220622PRMG"))
        # print(dan.hours_for_workers_having_worked_on_bid_by_product_per_month(df, "220622PRMG"))

        # print(dan.avg_rate_for_bid_by_product(df, "220622PRMG"))
        # print(dan.avg_rate_per_month_for_bid_by_product(df, "220622PRMG"))

        # print(dan.total_hours_worked_by_task(df))
        # print(dan.total_hours_worked_by_task_per_month(df))

        # print(dan.rate_for_task_for_all_workers_by_month(df, task_text))
        # print(dan.avg_rate_per_month(df))

        # print(dan.avg_rate_for_bid_by_task_per_month(df, "220622PRMG"))

        # print(dan.distribution_of_bid_among_products(df, "220622PRMG"))

        # print(dan.total_units_processed_for_bid(df, "220622PRMG"))
        # print(dan.total_units_processed_for_bid_by_month(df, "220622PRMG"))
        # print(dan.total_amount_by_product_for_bid_by_month(df, "220622PRMG"))

        # print(dan.total_hours_and_units_per_bid_for_worker(df, worker_text))
        # print(dan.ea_bid_worked_on_by_worker(df, worker_text))
        # print(dan.ea_bid_worked_on_by_worker_ea_month(df, worker_text))

        # print(dan.workers_ranked_by_total_efficiency_in_given_month(df, 2022, 10))
        # print(dan.workers_ranked_by_task_efficiency_in_given_month(df, task_text, 2022, 10))

        # print(dan.avg_rate_per_month_by_task(df))

        # print(dan.total_labor_hours_by_month(df))

        # print(dan.(df, worker_text))


#Start the show
###
app = QApplication(sys.argv)

# IN data_analysis.py
#
#   df = pd.read_parquet('record_data/total_data.parquet')
#   datas = {
#         'product': products_series,
#         'name': workers_list,
#         'task': task_list
#     }

df, datas = dan.main()


window = MainWindow()
window.show()

app.exec()

def main():
    print('x')

if __name__ == '__main__':
    main()





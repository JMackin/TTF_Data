import os
import pandas as pd
import data_analysis as dan
import datetime

now_dt = f"{datetime.datetime.now(tz=None).strftime('%S%H%M%j%Y')}"
report_timeframe = "Total_to_Date"
report_subject = "General"

def main(df, monthly, subject, subject_dict, selected_month):

    if not os.path.isdir("./Generated_Reports/"):
        os.mkdir("./Generated_Reports/")

    print(subject)
    print(subject_dict[subject])
    print(selected_month)
    print(monthly)

    if monthly:
        df = df.groupby([pd.Grouper(key='Date', freq='M')]).get_group(selected_month)
        report_timeframe = f"for_{selected_month[:-3]}"

    if subject == 1:
        report_subject = "General"
        make_general_report(df, monthly)
    elif subject == 2:
        make_worker_report(df, monthly)
        report_subject = "Worker"
    elif subject == 3:
        make_batch_report(df, monthly)
        report_subject = "Batch"
    elif subject == 4:
        make_product_report(df, monthly)
    elif subject == 5:
        report_subject = "Product"
        make_task_report(df, monthly)
    else:
        print(f"Received subject no. {subject}. Invalid")
        return


def make_general_report(df, monthly):


   print(df)

   write_table_to_html(df)


def make_product_report(df, monthly):

   print('x')


def make_task_report(df, monthly):

   print('x')


def make_batch_report(df, monthly):

   print('x')


def make_worker_report(df, monthly):

   print('x')

def write_table_to_html(df):
    report_title = f"{report_timeframe}_{report_subject}_Stats_Report_{now_dt}"
    df.to_html(f"./Generated_Reports/{report_title}.html")

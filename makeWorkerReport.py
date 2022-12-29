import os
import pandas as pd
import pdfkit

import data_analysis as dan
import datetime

now_dt = f"{datetime.datetime.now(tz=None).strftime('%S%H%M%j%Y')}"
report_timeframe = "Total_to_Date"
report_subject = "General"
report_title = f"{report_timeframe}_{report_subject}_Stats_Report_{now_dt}"


def main(df, monthly, subject, subject_dict, selected_month):

    # Parent Folder path
    if not os.path.isdir("./Generated_Reports/"):
        os.mkdir("./Generated_Reports/")

    # Report directory containing html files w/ data tables and final report
    if not os.path.isdir(f"./Generated_Reports/{report_title}/"):
        os.mkdir(f"./Generated_Reports/{report_title}/")


    print(subject)
    print(subject_dict[subject])
    print(selected_month)
    print(monthly)

    if monthly:
        df = df.groupby([pd.Grouper(key='Date', freq='M')]).get_group(selected_month)
        report_timeframe = f"for_{selected_month[:-3]}"

    if subject == 1:
        report_subject = "General"
        make_general_report(df, monthly, subject_dict[subject], subject_dict, selected_month)
    elif subject == 2:
        make_worker_report(df, monthly, subject_dict[subject], subject_dict, selected_month)
        report_subject = "Worker"
    elif subject == 3:
        make_batch_report(df, monthly, subject_dict[subject], subject_dict, selected_month)
        report_subject = "Batch"
    elif subject == 4:
        make_product_report(df, monthly, subject_dict[subject], subject_dict, selected_month)
    elif subject == 5:
        report_subject = "Product"
        make_task_report(df, monthly, subject_dict[subject], subject_dict, selected_month)
    else:
        print(f"Received subject no. {subject}. Invalid")
        return



def make_general_report(df, monthly, subject, subject_dict, selected_month):

    first_page = generate_html_template(monthly, subject, subject_dict, selected_month)

    table_list = []
    table_list.append(write_table_to_html(df))

    with open(f"./Generated_Reports/{report_title}/{report_title}.html", "a+") as out_file:
        out_file.write(first_page)
        out_file.write(table_list[0])



def make_product_report(df, monthly, subject, subject_dict, selected_month):

   print('x')


def make_task_report(df, monthly, subject, subject_dict, selected_month):

   print('x')


def make_batch_report(df, monthly, subject, subject_dict, selected_month):

   print('x')


def make_worker_report(df, monthly, subject, subject_dict, selected_month):

   print('x')


def generate_html_template(monthly, subject, subject_dict, selected_month):

    if monthly:
        timeframe = f"For {selected_month}"
    else:
        timeframe = f"Total Statistics to Date\n(starting on 06-22)"


    html_template = f"<h1>{report_subject} Stats Report</h1>\n"\
                    f"<h1>{timeframe}</h1>\n"\
                    f"<h3> Generated: " \
                    f"{datetime.datetime.now(tz=None).strftime('%m/%d/%Y, %H:%M:%S')}"

    return html_template


def write_table_to_html(df):

    df_html = df.to_html()
    return df_html


def create_pdf_from_html(out_html_path_list, out_pdf_path):

    pdfkit.from_file(out_html_path_list, out_pdf_path)


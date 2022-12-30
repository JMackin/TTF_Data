import os
import pandas as pd
import pdfkit

import data_analysis as dan
import datetime


def main(df, monthly, subject, subject_dict, selected_month):

    print(subject)
    print(subject_dict[subject])
    print(selected_month)
    print(monthly)

    if subject == 1:
        report_subject = "General"

        now_dt, report_timeframe, report_title, report_topic \
            = get_report_parameters(df, monthly, subject, subject_dict, selected_month, report_subject)

        make_report_dirs(report_title)

        make_general_report(df, monthly, report_topic, subject_dict, selected_month, report_title, report_subject)

    elif subject == 2:

        report_subject = "Worker"

        now_dt, report_timeframe, report_title, report_topic \
            = get_report_parameters(df, monthly, subject, subject_dict, selected_month, report_subject)

        make_report_dirs(report_title)

        make_worker_report(df, monthly, report_topic, subject_dict, selected_month, report_title, report_subject)

    elif subject == 3:
        report_subject = "Batch"

        now_dt, report_timeframe, report_title, report_topic \
            = get_report_parameters(df, monthly, subject, subject_dict, selected_month, report_subject)

        make_report_dirs(report_title)

        make_batch_report(df, monthly, report_topic, subject_dict, selected_month, report_title, report_subject)

    elif subject == 4:
        report_subject = "Product"

        now_dt, report_timeframe, report_title, report_topic \
            = get_report_parameters(df, monthly, subject, subject_dict, selected_month, report_subject)

        make_report_dirs(report_title)

        make_product_report(df, monthly, report_topic, subject_dict, selected_month, report_title, report_subject)

    elif subject == 5:
        report_subject = "Task"

        now_dt, report_timeframe, report_title, report_topic \
            = get_report_parameters(df, monthly, subject, subject_dict, selected_month, report_subject)

        make_report_dirs(report_title)

        make_task_report(df, monthly, report_topic, subject_dict, selected_month, report_title, report_subject)


    else:
        print(f"Received subject no. {subject}. Invalid")
        return


def get_report_parameters(df, monthly, subject, subject_dict, selected_month, report_subject):

    now_dt = f"{datetime.datetime.now(tz=None).strftime('%S%H%M%j%Y')}"


    if monthly:
        # df = df.groupby([pd.Grouper(key='Date', freq='M')]).get_group(selected_month)
        report_timeframe = f"For_{str(selected_month).split('-')[0]}-{str(selected_month).split('-')[1]}"
    else:
        report_timeframe = "Total_to_Date"

    report_topic = subject_dict[subject]

    report_title = f"{report_timeframe}_{report_subject}_Stats_Report_{now_dt}"

    return now_dt, report_timeframe, report_title, report_topic


def make_product_report(df, monthly, report_topic, subject_dict, selected_month, report_subject, report_title):

    first_page = generate_html_template(monthly, report_topic, subject_dict, selected_month, report_subject)

    table_list = []

    table_list.append(write_table_to_html(df))

    with open(f"./Generated_Reports/{report_title}/{report_title}.html", "a+") as out_file:
        out_file.write(first_page)
        out_file.write(table_list[0])



def make_general_report(df, monthly, report_topic, subject_dict, selected_month, report_title, report_subject):

    first_page = generate_html_template(monthly, report_topic, subject_dict, selected_month, report_subject)

    table_list = []

    if monthly:
        df_list = \
            [
                dan.total_labor_hours_in_given_month(df, selected_month),
                dan.total_hours_worked_by_task_in_given_month(df, selected_month),
                dan.total_labor_hours_per_worker_in_given_month(df, selected_month),
                dan.total_units_for_all_products_in_given_month(df, selected_month),
                dan.total_hours_and_units_per_bid_in_given_month(df, selected_month),
                dan.avg_rate_per_task_in_given_month(df, selected_month),
                dan.workers_ranked_by_total_efficiency_in_given_month(df, selected_month)
            ]
    else:
        df_list = \
            [   # LABOR
                dan.total_labor_hours_by_month(df),
                dan.total_hours_worked_by_task_per_month(df),
                dan.total_labor_hours_per_worker_by_month(df),
                dan.total_units_by_month_for_all_products(df),
                dan.total_hours_and_units_per_bid_per_month(df),
                # EFFICIENCY
                dan.avg_rate_per_task_by_month(df),
                dan.workers_ranked_by_total_efficiency(df),
             ]

    table_list.append(write_table_to_html(df))

    with open(f"./Generated_Reports/{report_title}/{report_title}.html", "a+") as out_file:
        out_file.write(first_page)
        out_file.write(table_list[0])


def make_task_report(df, monthly, report_topic, subject_dict, selected_month, report_title, report_subject):

    first_page = generate_html_template(monthly, report_topic, subject_dict, selected_month, report_subject)

    table_list = []
    table_list.append(write_table_to_html(df))

    with open(f"./Generated_Reports/{report_title}/{report_title}.html", "a+") as out_file:
        out_file.write(first_page)
        out_file.write(table_list[0])


def make_batch_report(df, monthly, report_topic, subject_dict, selected_month, report_title, report_subject):

    first_page = generate_html_template(monthly, report_topic, subject_dict, selected_month, report_subject)

    table_list = []
    table_list.append(write_table_to_html(df))

    with open(f"./Generated_Reports/{report_title}/{report_title}.html", "a+") as out_file:
        out_file.write(first_page)
        out_file.write(table_list[0])


def make_worker_report(df, monthly, report_topic, subject_dict, selected_month, report_title, report_subject):

    first_page = generate_html_template(monthly, report_topic, subject_dict, selected_month, report_subject)

    table_list = []
    table_list.append(write_table_to_html(df))

    with open(f"./Generated_Reports/{report_title}/{report_title}.html", "a+") as out_file:
        out_file.write(first_page)
        out_file.write(table_list[0])


def generate_html_template(monthly, report_topic, subject_dict, selected_month, report_subject):

    if monthly:
        timeframe = f"For {selected_month[-5:-3]}-{selected_month[:4]}"
    else:
        timeframe = f"Total Statistics to Date\n(starting on 06-22)"

    if report_topic == "General":
        html_template = f"<h1>{report_subject} Stats Report</h1>\n"\
                        f"<h2>{timeframe}</h2>\n"\
                        f"<h3> Generated: " \
                        f"{datetime.datetime.now(tz=None).strftime('%m/%d/%Y, %H:%M:%S')}"
    else:
        html_template = f"<h1>{report_subject} Stats Report</h1>\n" \
                        f"<h1>Subject: {report_topic}</h1>"\
                        f"<h2>{timeframe}</h2>\n"\
                        f"<h3> Generated: " \
                        f"{datetime.datetime.now(tz=None).strftime('%m/%d/%Y, %H:%M:%S')}"\
                        f"<br><br>"

    return html_template


def write_table_to_html(df):

    df_html = df.to_html()
    return df_html


def create_pdf_from_html(out_html_path_list, out_pdf_path):

    pdfkit.from_file(out_html_path_list, out_pdf_path)


def make_report_dirs(report_title):
    # Parent Folder path
    if not os.path.isdir("./Generated_Reports/"):
        os.mkdir("./Generated_Reports/")

    # Report directory containing html files w/ data tables and final report
    if not os.path.isdir(f"./Generated_Reports/{report_title}/"):
        os.mkdir(f"./Generated_Reports/{report_title}/")
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
                # "<h4></h4>",
                "<h4>Total Labor hours among all workers and tasks</h4>",
                dan.total_labor_hours_in_given_month(df, selected_month),
                "<h4>Total Labor hours for each task among all workers</h4>",
                dan.total_hours_worked_by_task_in_given_month(df, selected_month),
                "<h4>Total labor hours for each worker</h4>",
                dan.total_labor_hours_per_worker_in_given_month(df, selected_month),
                "<h4>Total units completed for each product type</h4>",
                dan.total_units_for_all_products_in_given_month(df, selected_month),
                "<h4>Total labor hours and units completed for each batch ID</h4>",
                dan.total_hours_and_units_per_bid_in_given_month(df, selected_month),
                "<h4>Total units completed for each batch ID divided by each product type</h4>",
                dan.distribution_of_ea_bid_among_products_for_given_month(df, selected_month),
                "<h4>Average work rate (units per min) for each task</h4>",
                dan.avg_rate_per_task_in_given_month(df, selected_month),
                "<h4>Workers ranked by average work rate (units per min) for all tasks</h4>",
                dan.workers_ranked_by_total_efficiency_in_given_month(df, selected_month)
            ]
    else:
        df_list = \
            [   # LABOR
                "<h4>Total Labor hours among all workers and tasks</h4>",
                dan.total_labor_hours_by_month(df),
                "<h4>Total Labor hours for each task among all workers</h4>",
                dan.total_hours_worked_by_task_per_month(df),
                "<h4>Total labor hours for each worker</h4>",
                dan.total_labor_hours_per_worker_by_month(df),
                "<h4>Total units completed for each product type</h4>",
                dan.total_units_by_month_for_all_products(df),
                "<h4>Total units completed for each batch ID divided by each product type</h4>",
                dan.distribution_of_ea_bid_among_products_per_month(df),
                "<h4>Each Batch ID divided by product type <b>as a percentage</b> of the total batch</h4>",
                dan.percentage_distribution_of_ea_bid_among_products_per_month(df),
                "<h4>Total labor hours and units completed for each batch ID</h4>",
                dan.total_hours_and_units_per_bid_per_month(df),
                # EFFICIENCY
                "<h4>Average work rate (units per min) for each task</h4>",
                dan.avg_rate_per_task_by_month(df),
                "<h4>Workers ranked by average work rate (units per min) for all tasks</h4>",
                dan.workers_ranked_by_total_efficiency(df),
             ]

    table_list = [write_table_to_html(func_df) for func_df in df_list]

    with open(f"./Generated_Reports/{report_title}/{report_title}.html", "a+") as out_file:
        out_file.write(first_page)

        for stat_table in table_list:
            out_file.write(stat_table)

    create_pdf_from_html(f"./Generated_Reports/{report_title}/{report_title}.html",
                         f"./Generated_Reports/{report_title}/{report_title}.pdf")

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
                        f"{datetime.datetime.now(tz=None).strftime('%m/%d/%Y, %H:%M:%S')}" \
                        f"<p><small> Stats are computed  using given totals taken from selected timeframe." \
                        f"<br>e.g. worker related stats under 'to date' will consist of all workers employed during the " \
                        f"given year.<br>Whereas stats for a given month will contain only the workers who were employed " \
                        f"during that month." \
                        f"<br><i> Note: Months are denoted by their last day. </i></small></p>" \
                        f"<br><br>"
    else:
        html_template = f"<h1>{report_subject} Stats Report</h1>\n" \
                        f"<h1>Subject: {report_topic}</h1>"\
                        f"<h2>{timeframe}</h2>\n"\
                        f"<h3> Generated: " \
                        f"{datetime.datetime.now(tz=None).strftime('%m/%d/%Y, %H:%M:%S')}" \
                        f"<h3><i> Note: Months denoted by final day. </i></h3>" \
                        f"<p><small> Stats are computed  using given totals taken from selected timeframe." \
                        f"<br>e.g. worker related stats under 'to date' will consist of all workers employed during the " \
                        f"given year.<br>Whereas stats for a given month will contain only the workers who were employed " \
                        f"during that month." \
                        f"<br><i> Note: Months are denoted by their last day. </i></small></p>" \
                        f"<br><br>"

    return html_template



def write_table_to_html(df):


    print(type(df))
    #
    # month_dict = {'2022-06-30': 'Jun 22',
    #               '2022-07-31': 'July 22',
    #               '2022-08-31': 'Aug 22',
    #               '2022-09-30': 'Sep 22',
    #               '2022-10-31': 'Oct 22',
    #               '2022-11-30': 'Nov 22',
    #               '2022-12-31': 'Dec 22'}

    if isinstance(df, pd.Series):
        df = df.to_frame()
    elif isinstance(df, str):
        return df

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
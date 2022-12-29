import sys
import pandas as pd
import data_analysis as dan


def main(df, monthly, subject, subject_dict, selected_month):

    print(subject)
    print(subject_dict[subject])
    print(selected_month)
    print(monthly)

def make_general_report(df, monthly, month_group):

    if monthly:
        df = df.groupby([pd.Grouper(key='Date', freq='M')]).get_group(month_group)



import pandas as pd

import re
import pyarrow
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import calendar
import datetime

def clean_df():

    df = pd.read_csv('record_data/total_data.csv')
    df = df.convert_dtypes()

    df['Time'] = df['Time'].mask(df['Time'] == 'X:Y', '0:00')

    df['Time'] = df['Time'].map(lambda x: pd.to_timedelta(x+':00') if 'GMT' not in x else pd.to_timedelta('0:00:00'))

    # df['Date'] = df['Date'].map(lambda x: x[:-2]+'2022' if x[-4:] != '2022' else x)

    df['Date'] = df['Date'].map(lambda x: pd.to_datetime(x[1:], format='%m/%d/%y') if len(x) == 9 else pd.to_datetime(x[1:], format='%m/%d/%Y'))
    # df['Time'] = df['Time'].map(lambda x: int((x.split(':')[0]))*60+int(x.split(':')[1]))

    df['Task'] = df['Task'].map(lambda x: 'T/S/B' if (re.search('T/S/B', x) and not re.search('T/S/B\(2-Pack\)', x)) else x)
    df['Task'] = df['Task'].map(lambda x: x.replace('Didtask:', ''))

    #GET EFFICIENCY RATE
    worker_rate = df['Time'].map(lambda x: x.total_seconds())
    df['Rate'] = df['Units'].div((worker_rate) / 60)

    df.to_parquet('record_data/total_data.parquet')


def main():

    clean_df()
    df = pd.read_parquet('record_data/total_data.parquet')

    products_series = df['Product'].unique()
    workers_list = df['Name'].unique()
    task_list = df['Task'].unique()

    things_dict = {
        'products': products_series,
        'names': workers_list,
        'tasks': task_list
    }

    # total_units_by_month_for_product(df, products_series[2])
    # rate_for_task_for_worker_by_month(df, "Ashley", "Twisted")
    # avg_efficiency_per_month(df, "Ashley")

    return df, things_dict

    # do_analysis(df, products_series, workers_list, task_list)


def get_things_dict_for_month(month, year, df):

    given_month = calendar.monthrange(year, month)

    if month < 10:
        given_month = str(year) + '-0' + str(month) + '-' + str(given_month[1])
    else:
        given_month = str(year) + '-' + str(month) + '-' + str(given_month[1])

    df = df.groupby([pd.Grouper(key='Date', freq='M')]).get_group(given_month)

    products_series = df['Product'].unique()
    workers_list = df['Name'].unique()
    task_list = df['Task'].unique()
    bid_list = df['BatchID'].unique()

    things_dict = {
        'products': products_series,
        'names': workers_list,
        'tasks': task_list,
        'bids': bid_list
    }

    return things_dict, given_month


def distribution_of_bid_among_products(df, bid):

    df = df[df["BatchID"] == bid]
    total_units_per_product_for_bid_df = total_amount_by_product_for_bid(df, bid)
    total_units_df = total_units_processed_for_bid(df, bid)
    total_units = total_units_df.iloc[0]

    distribution_among_products = total_units_per_product_for_bid_df.div(total_units)
    distribution_among_products = distribution_among_products * 100

    return distribution_among_products


def distribution_of_ea_bid_among_products_per_month(df, bid):

    df = df[df["BatchID"] == bid]
    total_units_per_product_for_bid_df = total_amount_by_product_for_bid(df, bid)
    total_units_df = total_units_processed_for_bid(df, bid)
    total_units = total_units_df.iloc[0]

    distribution_among_products = total_units_per_product_for_bid_df.div(total_units)
    distribution_among_products = distribution_among_products * 100

    return distribution_among_products


def avg_rate_per_month_for_bid_by_product(df, bid):
    df = df[df["BatchID"] == bid]

    avg_rate_by_product_per_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID', 'Product'])['Rate'].agg('mean')

    return avg_rate_by_product_per_month


def avg_rate_for_bid_by_product(df, bid):
    df = df[df["BatchID"] == bid]

    avg_rate_by_product = df.groupby(['BatchID', 'Product'])['Rate'].agg('mean')

    return avg_rate_by_product


def avg_rate_for_bid_by_task(df, bid):

    df = df[df["BatchID"] == bid]

    avg_rate_by_task = df.groupby(['BatchID', 'Task'])['Rate'].agg('mean')

    return avg_rate_by_task


def avg_rate_for_bid_by_task_per_month(df, bid):

    df = df[df["BatchID"] == bid]

    avg_rate_by_task = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID', 'Task'])['Rate'].agg('mean')

    return avg_rate_by_task


def hours_for_workers_having_worked_on_bid_by_product_per_month(df, bid):

    df = df[df["BatchID"] == bid]

    total_units_per_product_for_bid = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID', 'Product', 'Name'])['Time'].agg('sum')

    return total_units_per_product_for_bid


def hours_for_workers_having_worked_on_bid_by_product(df, bid):

    df = df[df["BatchID"] == bid]

    total_units_per_product_for_bid = df.groupby(['BatchID', 'Product', 'Name'])['Time'].agg('sum')

    return total_units_per_product_for_bid


def average_hours_by_product_per_month_for_bid(df, bid):
    df = df[df["BatchID"] == bid]

    total_units_per_product_for_bid_by_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID', 'Product'])['Time'].agg('mean')

    return total_units_per_product_for_bid_by_month


def total_hours_by_product_per_month_for_bid(df, bid):
    df = df[df["BatchID"] == bid]

    print("Total time per product")
    total_units_per_product_for_bid_by_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID', 'Product'])['Time'].agg('sum')

    return total_units_per_product_for_bid_by_month


def average_hours_by_product_for_bid(df, bid):

    df = df[df["BatchID"] == bid]

    print("Total time per product")
    avg_units_per_product_for_bid = df.groupby(['BatchID', 'Product'])['Time'].agg('mean')

    return avg_units_per_product_for_bid


def total_hours_by_product_for_bid(df, bid):

    df = df[df["BatchID"] == bid]

    print("Total time per product")
    total_units_per_product_for_bid = df.groupby(['BatchID', 'Product'])['Time'].agg('sum')

    return total_units_per_product_for_bid


def total_hours_per_month_for_bid(df, bid):
    df = df[df["BatchID"] == bid]

    total_units_per_product_for_bid_by_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID'])['Time'].agg('sum')

    return total_units_per_product_for_bid_by_month


def total_hours_for_bid(df, bid):

    df = df[df["BatchID"] == bid]

    total_units_per_product_for_bid = df.groupby(['BatchID'])['Time'].agg('sum')

    return total_units_per_product_for_bid


def total_amount_by_product_for_bid_by_month(df, bid):

    df = df[df["BatchID"] == bid]

    total_units_per_product_for_bid = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID', 'Product'])['Units'].agg('sum')

    return total_units_per_product_for_bid


def total_amount_by_product_for_bid(df, bid):

    df = df[df["BatchID"] == bid]

    total_units_per_product_for_bid = df.groupby(['BatchID', 'Product'])['Units'].agg('sum')

    return total_units_per_product_for_bid


def total_units_processed_for_bid(df, bid):

    df = df[df["BatchID"] == bid]

    total_units_for_bid = df.groupby(['BatchID'])['Units'].agg('sum')

    return total_units_for_bid


def total_units_processed_for_bid_by_month(df, bid):

    df = df[df["BatchID"] == bid]

    total_units_for_bid_by_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID'])['Units'].agg('sum')

    return total_units_for_bid_by_month


def total_hours_worked_by_task_for_worker(df, name):

    df = df[df["Name"] == name]

    total_hours_by_task = df.groupby(['Task'])['Time'].agg('sum')

    return total_hours_by_task


def total_hours_worked_by_task(df):

    total_hours_by_task = df.groupby(['Task'])['Time'].agg('sum')

    return total_hours_by_task

def total_hours_worked_by_task_in_given_month(df, given_month):

    total_hours_by_task_in_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'Task'])['Time'].agg('sum')
    total_hours_by_task_in_month = total_hours_by_task_in_month.groupby(['Date']).get_group(given_month)

    return total_hours_by_task_in_month

def total_hours_worked_by_task_per_month(df):

    total_hours_by_task_per_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'Task'])['Time'].agg('sum')

    return total_hours_by_task_per_month


def total_hours_worked_by_task_for_worker_per_month(df, name):
    df = df[df["Name"] == name]

    total_hours_by_task = df.groupby([pd.Grouper(key='Date', freq='M'), 'Task'])['Time'].agg('sum')

    return total_hours_by_task


def total_units_all_time_by_product_for_worker(df, name):

    df = df[df['Name'] == name]

    total_units_per_product = df.groupby(['Product'])['Units'].agg('sum')

    return total_units_per_product


def total_units_per_month_by_product_for_worker(df, name):

    df = df[df['Name'] == name]

    total_units_per_product_by_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'Product'])['Units'].agg('sum')

    return total_units_per_product_by_month


def total_units_per_month_by_product_for_worker(df, name):

    df = df[df['Name'] == name]

    total_units_per_product = df.groupby(['Product'])['Units'].agg('sum')
    total_units_per_product_by_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'Product'])['Units'].agg('sum')

    return total_units_per_product


def total_units_done_by_task_for_worker_per_month(df, name):

    df = df[df['Name'] == name]

    total_units_per_task_per_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'Task'])['Units'].agg('sum')

    return total_units_per_task_per_month


def total_units_done_by_task_for_worker(df, name):

    df = df[df['Name'] == name]

    total_units_per_task = df.groupby(['Task'])['Units'].agg('sum')

    return total_units_per_task


def total_units_by_month_for_product(df, prod):

    df = df[df['Product'] == prod]

    total_units_per_product_per_month = df.groupby(pd.Grouper(key='Date', freq='M'))['Units'].agg('sum')

    # total_units_per_product_per_month.plot.bar()

    return total_units_per_product_per_month
    # df['Time'] = df['Time'].map(lambda x: pd.to_timedelta(x+':00'))


def total_units_by_month_for_all_products(df):

    total_units_per_product_per_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'Product'])['Units'].agg('sum')

    # total_units_per_product_per_month.plot.bar()

    return total_units_per_product_per_month

def total_units_for_all_products_in_given_month(df, given_month):

    total_units_per_product_in_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'Product'])['Units'].agg('sum')
    total_units_per_product_in_month = total_units_per_product_in_month.groupby(['Date']).get_group(given_month)
    # total_units_per_product_per_month.plot.bar()

    return total_units_per_product_in_month

def rate_for_task_for_one_worker_by_month(df, name, task):

    df = df[df['Task'] == task]
    df = df[df['Name'] == name]

    worker_rank_task_speed = df.groupby(pd.Grouper(key='Date', freq='M'))['Rate'].agg('mean').sort_values(ascending=False)

    return worker_rank_task_speed

    # worker_rank_task_speed.plot(x="Date", y="Rate")


def rate_for_task_for_all_workers_by_month(df, task):

    df = df[df['Task'] == task]

    avg_rate_per_task_per_worker_per_month = df.groupby(['Name', pd.Grouper(key='Date', freq='M')])['Rate'].agg('mean')

    return avg_rate_per_task_per_worker_per_month

    # worker_rank_task_speed.plot(x="Date", y="Rate")


def total_hours_and_units_per_bid_for_worker(df, name):

    df = df[df['Name'] == name]

    total_units_per_bid = df.groupby(['BatchID'])['Units'].agg('sum')
    total_hours_per_bid = df.groupby(['BatchID'])['Time'].agg('sum')

    total_hours_and_units_per_bid = pd.concat([total_units_per_bid, total_hours_per_bid], axis=1)
    return total_hours_and_units_per_bid

def total_hours_and_units_per_bid_per_month(df):

    total_units_per_bid = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID'])['Units'].agg('sum')
    total_hours_per_bid = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID'])['Time'].agg('sum')

    total_hours_and_units_per_bid = pd.concat([total_units_per_bid, total_hours_per_bid], axis=1)
    return total_hours_and_units_per_bid

def total_hours_and_units_per_bid_in_given_month(df, given_month):

    total_units_per_bid = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID'])['Units'].agg('sum')
    total_hours_per_bid = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID'])['Time'].agg('sum')

    total_hours_and_units_per_bid = pd.concat([total_units_per_bid, total_hours_per_bid], axis=1)

    total_hours_and_units_per_bid = total_hours_and_units_per_bid.groupby(['Date']).get_group(given_month)

    return total_hours_and_units_per_bid


def total_hours_worked_for_worker(df, name):

    df = df[df['Name'] == name]

    total_hours_for_worker = df['Time'].agg('sum')

    return total_hours_for_worker


def total_hours_worked_for_worker_per_month(df, name):

    df = df[df['Name'] == name]

    total_hours_for_worker = df.groupby(['Time', pd.Grouper(key='Date', freq='M')]).agg('sum')

    return total_hours_for_worker


def ea_bid_worked_on_by_worker(df, name):   #Returns Array

    df = df[df['Name'] == name]

    ea_bid_worked_on = df["BatchID"].unique()

    return ea_bid_worked_on


def ea_bid_worked_on_by_worker_ea_month(df, name):

    df = df[df['Name'] == name]

    ea_bid_worked_on_monthly_date = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID'], group_keys=True)['Date']\
        .apply(lambda x: x)
    ea_bid_worked_on_monthly_units = df.groupby([pd.Grouper(key='Date', freq='M'), 'BatchID'], group_keys=True)['Units']\
        .apply(lambda x: x)

    ea_bid_worked_on_monthly = pd.concat([ea_bid_worked_on_monthly_date, ea_bid_worked_on_monthly_units], axis=1)

    ea_bid_worked_on_monthly = ea_bid_worked_on_monthly.set_axis(['Day', 'Units'], axis='columns').rename_axis("BIDs_per_month", axis="columns")

    return ea_bid_worked_on_monthly


def avg_rate_per_month_by_task(df):

    avg_rate_per_task_per_month = df.groupby(['Task', pd.Grouper(key='Date', freq='M')])['Rate'].agg('mean')

    return avg_rate_per_task_per_month


def avg_rate_per_task_by_month(df):

    avg_rate_per_task_per_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'Task'])['Rate'].agg('mean')

    return avg_rate_per_task_per_month

def avg_rate_per_task_in_given_month(df, given_month):

    avg_rate_per_task_in_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'Task'])['Rate'].agg('mean')

    avg_rate_per_task_in_month = avg_rate_per_task_in_month.groupby(['Date']).get_group(given_month)

    return avg_rate_per_task_in_month


def avg_efficiency_per_month_for_one_worker(df, name):

    df = df[df['Name'] == name]

    avg_efficiency_per_month_by_worker = df.groupby(pd.Grouper(key='Date', freq='M'))['Rate'].agg('mean').sort_values(ascending=False)

    return avg_efficiency_per_month_by_worker

    # avg_efficiency_per_month_by_worker.plot(x="Date", y="Rate")


def workers_ranked_by_total_efficiency_per_month(df):

    workers_rates = df.groupby([pd.Grouper(key='Date', freq='M'), 'Name'])['Rate'].agg('mean').sort_values(ascending=False)
    workers_rates_rank = df.groupby([pd.Grouper(key='Date', freq='M'), 'Name'])['Rate'].agg('mean').rank(method='dense', ascending=False)

    workers_ranked = pd.merge(workers_rates, workers_rates_rank, on='Date')

    return workers_ranked

def workers_ranked_by_total_efficiency(df):

    workers_rates = df.groupby(['Name'])['Rate'].agg('mean').sort_values(ascending=False)
    workers_rates_rank = df.groupby(['Name'])['Rate'].agg('mean').rank(method='dense', ascending=False)

    workers_ranked = pd.merge(workers_rates, workers_rates_rank, on='Name')

    return workers_ranked

def workers_ranked_by_total_efficiency_in_given_month(df, given_month):

    # given_month = calendar.monthrange(year, month)
    #
    # if month < 10:
    #     given_month = str(year) + '-0' + str(month) + '-' + str(given_month[1])
    # else:
    #     given_month = str(year) + '-' + str(month) + '-' + str(given_month[1])

    workers_rates = df.groupby([pd.Grouper(key='Date', freq='M'), 'Name'])['Rate'].agg(Rate='mean')

    workers_rates['Rank'] = workers_rates.groupby(['Date']).rank(method='min', ascending=False)

    worker_rate_rank_for_given_month = workers_rates.groupby(['Date']).get_group(given_month).sort_values(by='Rank')

    return worker_rate_rank_for_given_month


def workers_ranked_by_task_efficiency_in_given_month(df, task, year, month):

    given_month = calendar.monthrange(year, month)

    if month < 10:
        given_month = str(year) + '-0' + str(month) + '-' + str(given_month[1])
    else:
        given_month = str(year) + '-' + str(month) + '-' + str(given_month[1])

    df = df[df['Task'] == task]

    workers_rates = df.groupby([pd.Grouper(key='Date', freq='M'), 'Name'])['Rate'].agg(Rate='mean')

    workers_rates['Rank'] = workers_rates.groupby(['Date']).rank(method='min', ascending=False)

    worker_rate_rank_for_given_month = workers_rates.groupby(['Date']).get_group(given_month).sort_values(by='Rank')


    return worker_rate_rank_for_given_month


def total_labor_hours_in_given_month(df, given_month):

    # hours = df.groupby([pd.Grouper(key='Date', freq='M')])['Time'].sum()
    hours = df.groupby([pd.Grouper(key='Date', freq='M')])['Time'].sum()

    hours = hours.groupby(['Date']).get_group(given_month)


    return hours

def total_labor_hours_by_month(df):

    hours = df.groupby([pd.Grouper(key='Date', freq='M')])['Time'].sum()

    return hours

def total_labor_hours_per_worker_in_given_month(df, given_month):

    hours = df.groupby([pd.Grouper(key='Date', freq='M'), 'Name'])['Time'].sum()

    hours = hours.groupby(['Date']).get_group(given_month)

    return hours

def total_labor_hours_per_worker_by_month(df):

    hours = df.groupby([pd.Grouper(key='Date', freq='M'), 'Name'])['Time'].sum()

    return hours

def total_labor_hours_to_date(df):

    hours = 0

    return hours

def do_analysis(df, products_series, workers_list, task_list):

    total_units_per_product_per_month = df.groupby(['Product', pd.Grouper(key='Date', freq='M')])['Units'].agg('sum')

    avg_rate_per_task_per_month = df.groupby(['Task', pd.Grouper(key='Date', freq='M')])['Rate'].agg('mean')
    avg_rate_per_task_per_worker_per_month = df.groupby(['Task', 'Name', pd.Grouper(key='Date', freq='M')])['Rate'].agg('mean')

    # print(avg_rate_per_task_per_month)
    print(total_units_per_product_per_month)
    # print(avg_rate_per_task_per_worker_per_month)

    df_pivoted = total_units_per_product_per_month.unstack(level=0)
    df_pivoted.plot.bar(subplots=True)
    df_pivoted.to_csv('Total_units_to_date.csv')

    print(df_pivoted)
    plt.show()


def twisting_stats(df, products_series):
    #  Rank workers based on avg twisting speed (pre-rolls per minute)
    pre_roll_list = [x for x in products_series if re.search("PR", x)]
    worker_df = df[df['Product'].isin(pre_roll_list)]
    worker_df = worker_df[worker_df['Task'] == 'Twisted']

    worker_rate = worker_df['Time'].map
    hours = df['Time'].sum()(lambda x: x.total_seconds())
    worker_df['Rate'] = worker_df['Units'].div((worker_rate) / 60)

    print(worker_df)

    worker_rate_twisting_sum_total = worker_df.groupby('Name', sort=True)['Units'].agg('sum').sort_values(ascending=False)

    worker_rank_twisting_speed = worker_df.groupby('Name', sort=True)['Rate'].agg('mean').sort_values(ascending=False)

    worker_rank_twisting_speed.to_csv('record_data/worker_rank_twisting_speed.csv')

    worker_rank_twisting_speed_by_month = worker_df.groupby(['Name', pd.Grouper(key='Date', freq='M')])['Rate'].agg(
        'mean')
    print(worker_rank_twisting_speed_by_month)

    worker_rank_twisting_speed_by_month.to_csv('record_data/worker_rank_twisting_speed_by_month.csv')

    worker_rank_twisting_speed_by_5Day = worker_df.groupby(['Name', pd.Grouper(key='Date', freq='5D')])['Rate'].agg(
        'mean')
    print(worker_rank_twisting_speed_by_5Day)

    worker_rank_twisting_speed_by_5Day.to_csv('record_data/worker_rank_twisting_speed_by_5Day.csv')

    worker_rank_twisting_speed_by_2day = worker_df.groupby(['Name', pd.Grouper(key='Date', freq='2D')])['Rate'].agg('mean')

    # worker_rank_twisting_speed_by_5Day['Ashley'].plot(x="Date", y="Rate")

    worker_rank_twisting_speed_by_2day['Ashley'].plot(x="Date", y="Rate")

    # plt.bar(worker_rank_twisting_speed.index, worker_rank_twisting_speed.values)
    # plt.bar(worker_rate_twisting_sum_total.index, worker_rate_twisting_sum_total.values)

    # worker_rank_twisting_speed_by_day.plot()

    plt.show()

if __name__ == '__main__':
    main()



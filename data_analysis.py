import pandas as pd

import re
import pyarrow
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

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
        'product': products_series,
        'name': workers_list,
        'task': task_list
    }

    # total_units_by_month_for_product(df, products_series[2])
    # rate_for_task_for_worker_by_month(df, "Ashley", "Twisted")
    # avg_efficiency_per_month(df, "Ashley")


    return df, things_dict

    # do_analysis(df, products_series, workers_list, task_list)

def total_units_all_time_by_product_for_worker(df, name):

    df = df[df['Name'] == name]

    total_units_per_product = df.groupby(['Product'])['Units'].agg('sum')

    return total_units_per_product

def total_units_per_month_by_product_for_worker(df, name):

    df = df[df['Name'] == name]

    total_units_per_product_by_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'Product'])['Units'].agg('sum')

    return total_units_per_product_by_month

def total_units_all_time_by_product_for_worker(df, name):

    df = df[df['Name'] == name]

    total_units_per_product = df.groupby(['Product'])['Units'].agg('sum')
    total_units_per_product_by_month = df.groupby([pd.Grouper(key='Date', freq='M'), 'Product'])['Units'].agg('sum')

    return total_units_per_product

def total_units_by_month_for_product(df, prod):

    df = df[df['Product'] == prod]

    total_units_per_product_per_month = df.groupby(pd.Grouper(key='Date', freq='M'))['Units'].agg('sum')

    # total_units_per_product_per_month.plot.bar()

    return total_units_per_product_per_month
    df['Time'] = df['Time'].map(lambda x: pd.to_timedelta(x+':00'))

def rate_for_task_for_worker_by_month(df, name, task):

    df = df[df['Task'] == task]
    df = df[df['Name'] == name]

    worker_rank_task_speed = df.groupby(pd.Grouper(key='Date', freq='M'))['Rate'].agg('mean').sort_values(ascending=False)

    return worker_rank_task_speed

    # worker_rank_task_speed.plot(x="Date", y="Rate")


def avg_efficiency_per_month(df, name):

    df = df[df['Name'] == name]

    avg_efficiency_per_month_by_worker = df.groupby(pd.Grouper(key='Date', freq='M'))['Rate'].agg('mean').sort_values(ascending=False)

    return avg_efficiency_per_month_by_worker

    # avg_efficiency_per_month_by_worker.plot(x="Date", y="Rate")



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

    worker_rate = worker_df['Time'].map(lambda x: x.total_seconds())
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



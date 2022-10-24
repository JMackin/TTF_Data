import pandas as pd

import re
import pyarrow


def clean_df():

    df = pd.read_csv('record_data/total_data.csv')
    df = df.convert_dtypes()

    [print(i) for i in df['Time']]

    df['Time'] = df['Time'].mask(df['Time'] == 'X:Y', '0:00')

    df['Time'] = df['Time'].map(lambda x: pd.to_timedelta(x+':00'))

    # df['Date'] = df['Date'].map(lambda x: x[:-2]+'2022' if x[-4:] != '2022' else x)

    df['Date'] = df['Date'].map(lambda x: pd.to_datetime(x[1:], format='%m/%d/%y') if len(x) == 9 else pd.to_datetime(x[1:], format='%m/%d/%Y'))
    # df['Time'] = df['Time'].map(lambda x: int((x.split(':')[0]))*60+int(x.split(':')[1]))

    # df.to_parquet('record_data/total_data.parquet')

    return df


def do_analysis(df):

    print('x')

def main():

    df = pd.read_parquet('record_data/total_data.parquet')

    products_series = df['Product'].unique()
    pre_roll_list = [x for x in products_series if re.search("PR", x)]
    worker_df = df[df['Product'].isin(pre_roll_list)]
    worker_df = worker_df[worker_df['Task'] == 'Twisted']


    worker_rate = worker_df['Time'].map(lambda x: x.total_seconds())

    worker_df['Rate'] = worker_df['Units'].rdiv(worker_rate)


    print(worker_df['Rate'])





    worker_df = worker_df.groupby('Name', sort=True)

    # print(w_pr_stats.sort_values(ascending=False))



    # print(pre_roll_list)
    # print(products_series)
    # print(df)
    # print(df['Name'][16])
    # print(df['Time'][0].total_seconds())




if __name__ == '__main__':
    main()




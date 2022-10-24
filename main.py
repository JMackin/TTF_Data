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

    worker_df = df.groupby('Name')

    products_series = df['Product'].unique()


    print(products_series)
    print(df)
    print(df['Name'][16])

    # print(df['Time'][0].total_seconds())




if __name__ == '__main__':
    main()




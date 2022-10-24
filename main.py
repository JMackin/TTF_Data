import pandas as pd

import re

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.

    df = pd.read_csv('record_data/total_data.csv')
    df = df.convert_dtypes()

    [print(i) for i in df['Time']]

    df['Time'] = df['Time'].mask(df['Time'] == 'X:Y', '0:00')

    df['Time'] = df['Time'].map(lambda x: pd.to_timedelta(x+':00'))

    # df['Date'] = df['Date'].map(lambda x: x[:-2]+'2022' if x[-4:] != '2022' else x)

    df['Date'] = df['Date'].map(lambda x: pd.to_datetime(x[1:], format='%m/%d/%y') if len(x) == 9 else pd.to_datetime(x[1:], format='%m/%d/%Y'))
    # df['Time'] = df['Time'].map(lambda x: int((x.split(':')[0]))*60+int(x.split(':')[1]))




    [print(i) for i in df['Time']]

    [print(x) for x in df['Date']]

    print(df)
    print(df.dtypes)






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

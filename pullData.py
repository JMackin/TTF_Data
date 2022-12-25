from __future__ import print_function

import io
import os
import re
import calendar as cal
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']


def main():

    count = 2
    years = {21: {}, 22: {}}
    mnth = None
    total_df_list = []

    month_to_short = {'January': 'Jan', 'February': 'Feb', 'March': 'Mar',
                      'April': 'Apr', 'May': 'May', 'June': 'Jun', 'July': 'Jul',
                      'August': 'Aug', 'September': 'Sep', 'October': 'Oct',
                      'November': 'Nov', 'December': 'Dec'}
    short_to_month = {'Jan': 'January', 'Feb': 'February', 'Mar': 'March',
                      'Apr': 'April', 'May': 'May', 'Jun': 'June', 'Jul': 'July',
                      'Aug': 'August', 'Sep': 'September', 'Oct': 'October',
                      'Nov': 'November', 'Dec': 'December'}
    month_list = list(cal.month_name)

    with open('folder_ids_month.txt', 'r') as f:

        for line in f.readlines():

            if re.search('202[0-9]', line):
                count = 3
                date = line[2:4]

            if count % 2 == 0 and count != 3:
                mnth = line
                print(f'{mnth}triggered\n')

            elif count % 2 != 0 and count > 2:
                if mnth:
                    years[int(date)].update({mnth: line})
            else:
                print(f'This line -> {line} <-\n')

            count = count + 1

    for x in years.keys():
        print(x)
        count = 1
        for y in years.get(x).keys():
            # print((years.get(x)).get(y))
            # print(f'>> {y[:-1]} and {((years.get(x)).get(y))[:-1]}')
            folder_id = (years.get(x)).get(y)[:-1]

            if y != '\n':
                month = short_to_month[y[:-1]]
                year = str(x)

            if x == 22 and count > 5:
                out_df = read_extract(folder_id, month, year)
                total_df_list.append(out_df)
            count = count + 1

    total_df = pd.concat(total_df_list, ignore_index=True)
    total_df.to_csv('./record_data/total_data.csv')

def read_extract(folder_id, month, year):
    creds = make_creds()
    big_df_list = []



    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        #

        results = service.files().list(
            q=f"'{folder_id}' in parents",
            fields="nextPageToken, files(id, name)")\
            .execute()

        items = results.get('files', [])

        print('yes')

        if not items:
            print('No files found.')
            return

        failed_items = []

        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            try:
                body = get_body(service, item['id'])
                data = extract_data(body)
                out_df = make_df(data[0], data[1], month, year)
                big_df_list.append(out_df)
                print('...')
            except:
                item_name = {item['name']}
                failed_items.append(item_name)
                print(f'{item_name} didnt work')
                continue

        # create_month_folders(service)
        # org_files_by_month(service)

        print("These files failed: ")
        [print(i) for i in failed_items]

        with open('failed_files.txt', 'a+') as ff:
            failedfiles = ff.read().splitlines()

            for file in failed_items:
                if file not in failedfiles:
                    ff.write(str(file)+'\n')

        print('yeah')

        big_df = pd.concat(big_df_list, ignore_index=True)
        big_df.to_csv(f'./record_data/{year}/{month}/total_{month+year}data.csv')
        return big_df


    except HttpError as error:
        print(f'An error occurred: {error}')

def make_df(data, today_date, month, year):

    df_list = []

    out_dir_name = today_date.replace('/', '_')
    print(out_dir_name)
    out_path = './record_data/' + year + '/' + month + '/' + out_dir_name.strip('\ufeff')

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    print(out_dir_name)

    for k, v in data.items():
        #print(data[k])
        filename = k
        for vv in data[k]:
            for key in vv.keys():
                # [print(key) for x in range(0, len(vv[key][0]))]
                reformed_data = {
                    'BatchID': [k for x in range(0, len(vv[key][0]))],
                    'Strain': [key.split(',', 1)[0] for x in range(0, len(vv[key][0]))],
                    'Product': [key.split(',', 1)[1] for x in range(0, len(vv[key][0]))],
                    'Name': vv[key][0],
                    'Task': vv[key][1],
                    'Units': vv[key][2],
                    'Time': vv[key][3],
                    'Date': [today_date for x in range(0, len(vv[key][0]))]

                }

                df_list.append(pd.DataFrame.from_dict(reformed_data))

    if len(df_list) > 0:
        combined_df = pd.concat(df_list)
        df_list = []

    print(pd.DataFrame.from_dict(combined_df))
    out_df = pd.DataFrame.from_dict(combined_df)
    out_df.to_csv(f'{out_path}/{filename}.csv')

    return out_df

def extract_data(body):

#   Info array:
#       0           1       2       3       4
#   | Prod_type | Worker | Task | # units | Time |
#
#   key:Batch Id
#   value: info
#   [ {BID: [4]}, {BID: [4]} ]

    name_list = []
    task_list = []
    unit_list = []
    time_list = []
    task_str = ''
    time_str = ''
    entries = []
    sub_entries = []
    prod_list = []
    at_trimming = False
    line_count = True
    prod_tasks = {}
    task_entries_list = []
    task_entries = {}
    split_strings = []

    str_arr = body.split(b'\n\r')


    for i in str_arr:
        if len(i) > 1:
            entries.append(i)

    for i in entries:
        sub_entries.append(i.split(b'\n'))

    for i in sub_entries:

        if line_count == True:
            today_date = i[0].decode()[-11:-1]
            line_count = False
            continue
        else:
            split_strings = [x.split(b' ') for x in i[2:]]
            prod_tasks[i[1].decode()] = split_strings

            if re.search('________________', i[1].decode()):
                at_trimming = True

                break

    name_flag = False
    task_flag = False
    time_flag = False
    el_cnt = 0

    # [print(i) for i in prod_tasks.values()]
    prod_tasks.popitem()
    print('----')

    for w, i in prod_tasks.items():
        prod_list = []
        for j in i:
            if j[2] != b'-':
                product = b''.join(j)
                product = product.decode().strip('\r')
                name_list = []
                task_list = []
                unit_list = []
                time_list = []
                task_str = ''
                time_str = ''
            else:
                for k in j:

                    if k == b'-':
                        name_flag = True
                        continue

                    if name_flag == True:
                        name_list.append(k.decode())
                        task_flag = True
                        name_flag = False
                        continue

                    elif task_flag == True:
                        if re.search('\d', k.decode()) and not re.search('-', k.decode()):
                            task_list.append(task_str)
                            unit_list.append(k.decode())
                            task_flag = False
                            el_cnt = 1
                            time_flag = True
                            task_str = ''
                            continue
                        else:
                            task_str += k.decode()

                    elif time_flag == True:
                        if el_cnt == 3:
                            time_str = k.decode()
                        elif el_cnt == 6:
                            time_str = time_str + ':' + k.decode()
                            time_list.append(time_str)
                            time_flag = False
                            break
                        el_cnt += 1

                if {product: [name_list, task_list, unit_list, time_list]} not in prod_list:
                    prod_list.append({product: [name_list, task_list, unit_list, time_list]})

        task_entries[w.strip('\r')] = prod_list

        # end for j in i

    #[print(i) for i in prod_list]



    # [print(i) for i in task_entries.items()]

    print(today_date)

    return [task_entries, today_date]


def get_body(service, file_id):

    req = service.files().export_media(fileId=file_id,
                                     mimeType='text/plain')
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, req)
    done = False

    while done is False:
        status, done = downloader.next_chunk()
        print(F'Download {int(status.progress() *100)}.')

    return file.getvalue()


def make_creds():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'ttfcreds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


if __name__ == '__main__':
    main()
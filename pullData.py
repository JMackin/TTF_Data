from __future__ import print_function

import io
import os
import re

import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']

def main():

    creds = make_creds()

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        #

        folder_id = input("Enter file ID: ")

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
                make_df(data[0], data[1])
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

        print('yeah')

    except HttpError as error:
        print(f'An error occurred: {error}')


def make_df(data, today_date):

    df_list = []

    out_dir_name = today_date.replace('/', '_')
    print(out_dir_name)
    out_path = f'./record_data/{out_dir_name}'

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



        print('-------')


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
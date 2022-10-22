from __future__ import print_function

import io
import os.path

import pandas as pd

import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.

SCOPES = ['https://www.googleapis.com/auth/drive']

def main():

    creds = make_creds()

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        # TODO: List summaries in drive with dd/mm/yyyy daily summary format to "TTF West End Daily Summaries" dir
        #
        # results = service.files().list(
        #     q="'1yp5blq-DU3X7MHFafyKiRYd_nAdqSIEJ' in parents",
        #     pageSize=10,
        #     fields="nextPageToken, files(id, name)")\
        #     .execute()
        #
        # items = results.get('files', [])

        ## Experimenting with labels

        print('yes')

        body = get_body(service, '1Mo1syVsDzkQIn1NEE45r_mRL9VtN_Xnic5Kxo4Ta6XE')

        make_df(body)

        # create_month_folders(service)
        # org_files_by_month(service)

        print('yeah')

    #     first_file_id = items[0]['id']
    #     print('Gonna move this file')
    #     print(str(first_file_id))
    #
    #     # Moves the file back to the base drive
    #     service.files().update(fileId=first_file_id, removeParents='1yp5blq-DU3X7MHFafyKiRYd_nAdqSIEJ').execute()
    #
    #     if not items:
    #         print('No files found.')
    #         return
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))

    except HttpError as error:
        print(f'An error occurred: {error}')


def make_df(body):

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
            today_date = i[0].decode()[-2:-11]
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

    [print(i) for i in prod_tasks.values()]

    for i in prod_tasks.values():
        for j in i:
            if j[0] != b'':
                product = ''.join(j[0].decode())
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
                        if re.search('\d', k.decode()) and (k != b'(2-Packs)'):
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
                            time_str = time_str.join(f':{k.decode()}')
                            time_list.append(time_str)
                            time_flag = False
                            break
                        el_cnt += 1

        prod_list.append({product: [name_list, task_list, unit_list, time_list]})

        # end for j in i

    [print(i) for i in prod_list]



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

def org_files_by_month(service):

    import calendar as cal

    ## PART 1: Make Dictionary of dictionaries mapping months to file IDs

    count = 2
    years = {21: {}, 22: {}}
    mnth = None

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

    print('Success Part 1\n')
    for x in years.keys():
        print(x)
        for y in years.get(x).keys():
         print(f'>> {y[:-1]} and {((years.get(x)).get(y))[:-1]}')


    ## PART 2 Move files to respective folders

    # short_to_month = {'Jan': 'January', 'Feb': 'February', 'Mar': 'March',
    #                   'Apr': 'April', 'May': 'May', 'Jun': 'June', 'Jul': 'July',
    #                   'Aug': 'August', 'Sep': 'September', 'Oct': 'October',
    #                   'Nov': 'November', 'Dec': 'December'}

    month_to_short = {'January': 'Jan', 'February': 'Feb', 'March': 'Mar',
                      'April': 'Apr', 'May': 'May', 'June': 'Jun', 'July': 'Jul',
                      'August': 'Aug', 'September': 'Sep', 'October': 'Oct',
                      'November': 'Nov', 'December': 'Dec'}

    month_list = list(cal.month_name)

    dir_id = input("Enter Folder Id to move files from > ")

    files_2b_moved = service.files().list(
        q=f"'{dir_id}' in parents",
        fields="nextPageToken, files(id, name)")\
        .execute()

    items = files_2b_moved.get('files', [])

    print('Got files...\n')

    for item in items:
        if re.search('((1[0-2])|(0[1-9]))/[0-3][0-9]/202[0-9] daily summary', item['name']):

            file_month_num = int(item['name'][:2])
            file_year = int(item['name'][8:10])
            file_month = f'{month_to_short[month_list[file_month_num]]}\n'

            month_dir = str(years.get(file_year).get(file_month))[:-1]

            # [print(i[:-1]) for i in years.get(file_year).keys()]

            print(f'{file_month}, {file_year}')
            print(f'>>>>>{month_dir}')

            service.files().update(
                fileId=item['id'], removeParents=f'{dir_id}'
            ).execute()

            service.files().update(
                fileId=item['id'], addParents=f'{month_dir}'
            ).execute()

            print(f'{item["name"]}')

        elif re.search('Daily Summary ((1[0-2])|([1-9]))/(([1-3][0-9])|([1-9]))/2[0-2]', item['name']):

            file_date = (((item['name'])[14:]).split('/'))
            file_month_num = int(file_date[0])
            file_year = int(file_date[2])
            file_month = f'{month_to_short[month_list[file_month_num]]}\n'

            month_dir = str(years.get(file_year).get(file_month))[:-1]

            print(f'{file_month}, {file_year}')



            service.files().update(
                fileId=item['id'], removeParents=f'{dir_id}'
            ).execute()

            service.files().update(
                fileId=item['id'], addParents=f'{month_dir}'
            ).execute()

            print(f'{item["name"]}')

        else:
            print('Not..')
            continue




def list_labels(items_list, service):

    first_file_id = items_list[0]['id']

    labels = service.files().listLabels(fileId=first_file_id).execute()

    label_fields = labels.get('items', [])

    for field in label_fields:
        print(f"{field}")


def create_month_folders(service):

    import calendar as cal

    folder_id_top = '1yp5blq-DU3X7MHFafyKiRYd_nAdqSIEJ'
    folder_id_2021 = '1kqNHQCaJhhCPGepdmKTw1-B8WwRYqBi0'
    folder_id_2022 = '1cpzBmIPArHixCQLNuIYe7nNTIhoLkC7K'

    month_dir_ids = []
    month_dir_ids_2021 = []
    month_dir_ids_2022 = []


    # List of month names
    month_list = list(cal.month_name)

    # Make month-named folders for 2022
    for i in range(1, 13):
        try:
            file_metadata = {
                'name': f'{month_list[i]}',
                'mimeType': 'application/vnd.google-apps.folder'
            }

            fold = service.files().create(body=file_metadata, fields='id').execute()

            service.files().update(
                fileId=fold.get('id'), addParents=f'{folder_id_2022}'
            ).execute()

            month_dir_ids_2022.append(fold.get('id'))

            print(fold.get('id'))

        except HttpError as error:
            print(F'An error occurred: {error}')
            fold = None


    # Make month-named folders for 2021
    for i in range(6, 13):
        try:
            file_metadata = {
                'name': f'{month_list[i]}',
                'mimeType': 'application/vnd.google-apps.folder'
            }

            fold = service.files().create(body=file_metadata, fields='id').execute()

            service.files().update(
                fileId=fold.get('id'), addParents=f'{folder_id_2021}'
            ).execute()

            month_dir_ids_2021.append(fold.get('id'))

            print(fold.get('id'))

        except HttpError as error:
            print(F'An error occurred: {error}')
            fold = None




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
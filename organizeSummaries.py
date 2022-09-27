from __future__ import print_function

import os.path

import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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

        create_month_folders(service)

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
                'TTFprodwe_creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

if __name__ == '__main__':
    main()
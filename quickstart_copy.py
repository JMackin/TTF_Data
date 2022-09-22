from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.

SCOPES = ['https://www.googleapis.com/auth/drive']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        # Gets files within a specific folder. Folders are referred to as 'parents'
        results = service.files().list(
            q="'1yp5blq-DU3X7MHFafyKiRYd_nAdqSIEJ' in parents",
            pageSize=10,
            fields="nextPageToken, files(id, name)")\
            .execute()

        items = results.get('files', [])

        first_file_id = items[0]['id']
        print('Gonna move this file')
        print(str(first_file_id))

        # Moves the file back to the base drive
        service.files().update(fileId=first_file_id, removeParents='1yp5blq-DU3X7MHFafyKiRYd_nAdqSIEJ').execute()

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Move a file to a designated directory (change parent)
        print(f'An error occurred: {error}')



if __name__ == '__main__':
    main()
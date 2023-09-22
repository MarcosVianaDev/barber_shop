from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


__all__ = ['Gsheets_db', 'SPREADSHEET_ID']

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1DClw0F_WGxr_w2rp8f_GojIzYJdl7G5gihYyTKsFE-U'
RANGE_NAME = 'A1:B'


class Gsheets_db:

    def __init__(self) -> None:
        self.sheet = self.__creds = None
        if os.path.exists('token.json'):
            self.__creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.__creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.__creds.to_json())
        try:
            service = build('sheets', 'v4', credentials=self.__creds)
            # Call the Sheets API
            self.sheet = service.spreadsheets()
        except HttpError as err:
            print(err)



    def getValues(self, range:str = 'A1:Z'):
        result:dict = self.sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=range).execute()
        values = result.get('values', [])
        
        if not values:
            print('No data found.')
            return ''

        return values


    def setValues(self, range:str = 'A1', new_values: str | list = ''):
        global sheet
        if('str' in str(type(new_values))):
            new_values = [
            [
                new_values
            ],
        ]
        elif('list' in str(type(new_values))):
            ...
        else:
            raise TypeError(f'Type Error: new_values must be string or list type. You passed {type(new_values)}')
        body = {
            'values': new_values
        }
        result = self.sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                    range=range,
                                    valueInputOption= 'USER_ENTERED',
                                    body=body).execute()
        return result


    def insertValues(self, range:str='A1', new_values: str | list = ''):
        if('str' in str(type(new_values))):
            new_values = [
            [
                new_values
            ],
        ]
        elif('list' in str(type(new_values))):
            ...
        else:
            raise TypeError(f'Type Error: new_values must be string or list type. You passed {type(new_values)}')
        body = {
            'values': new_values
        }
        result = self.sheet.values().append(spreadsheetId=SPREADSHEET_ID,
                                    range=range,
                                    valueInputOption='USER_ENTERED',
                                    body=body).execute()
        return result


if __name__ == '__main__':
    print(Gsheets_db().getValues())
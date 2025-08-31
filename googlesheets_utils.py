from pprint import pprint
from googleapiclient import discovery, errors
from google.oauth2 import service_account


class GooglesheetUtils:
    def __init__(self, spreadsheet_id) -> None:
        self.spreadsheet_id = spreadsheet_id
        self.credentials = service_account.Credentials.from_service_account_file(
            './secrets/wordsagent-f6f858f2293d.json',
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = discovery.build('sheets', 'v4', credentials=self.credentials)

    def get_columns(self, range_name):
        try:
            service = discovery.build("sheets", "v4", credentials=self.credentials)

            result = (
                service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=self.spreadsheet_id, 
                    range=range_name,
                    majorDimension='COLUMNS'
                )
            )

            response = result.execute()
            rows = response.get("values", [])
            print(f"{len(rows)} columns retrieved")
            return rows
        except errors.HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def update_data(self, range_name, values) -> None:
        request = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            valueInputOption='USER_ENTERED',
            includeValuesInResponse=True,
            range=range_name,
            body={
                'majorDimension': 'ROWS',
                'values': values
            }
        )

        response = request.execute()
        pprint(response)

    def append_data(self, range_name, values):
        try:
            service = discovery.build("sheets", "v4", credentials=self.credentials)

            request = (
                service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=self.spreadsheet_id,
                    range=range_name,
                    valueInputOption='USER_ENTERED',
                    body={
                        'majorDimension': 'ROWS',
                        'values': values
                    },
                )
            )

            response = request.execute()

            print(f"{(response.get('updates').get('updatedCells'))} cells appended.")
            return response

        except errors.HttpError as error:
            print(f"An error occurred: {error}")
            return error

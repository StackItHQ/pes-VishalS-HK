import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of your spreadsheet.
SAMPLE_SPREADSHEET_ID = ""
SAMPLE_RANGE_NAME = "Sheet1!A:E"

def main():
    """Shows basic usage of the Sheets API.
    Reads values from a sample spreadsheet, then writes new data.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API to read data
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get("values", [])

        if not values:
            print("No data found.")
        else:
            print("Existing data:")
            for row in values:
                print(row)

        # Prepare new data to write
        new_values = [
            ['Vijay', '7', 'pes2ug21cs605', 'CSE'],
            ['Nihal', '7', 'pes2ug21cs069', 'CSE'],
        ]

        # Append the new data to the sheet
        request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                        range=SAMPLE_RANGE_NAME, 
                                        valueInputOption="USER_ENTERED", 
                                        body={"values": new_values})
        response = request.execute()

        print(f"\nAppended {response.get('updates').get('updatedRows')} rows.")

        # Read the updated data
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                    range=SAMPLE_RANGE_NAME).execute()
        updated_values = result.get("values", [])

        print("\nUpdated data:")
        for row in updated_values:
            print(row)

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()

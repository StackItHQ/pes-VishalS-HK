import os, time
import mysql.connector
from mysql.connector import Error
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1S5qrZ1y47Nn4b04EzHE9DPHMyV2rqU7J5qGx1l-WyI8"
RANGE_NAME = "Sheet1!A:E"

DB_CONFIG = {
    'host': 'localhost',
    'database': 'superJoinAi',
    'user': 'root',
    'password': 'Olivegreen@123'
}

def get_google_sheets_service():
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
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("sheets", "v4", credentials=creds)

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to the DB: {e}")
    return None

def get_sheet_data(service):
    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        return result.get("values: ", [])
    except HttpError as error:
        print(f"An error occured in getting the sheet data: {error}")
    return []

def update_db_data(db_connection, formatted_data):
    try:
        cursor = db_connection.cursor()
        sql = """insert into spreadsheet (srn, name, semester, dept)
        values (%s, %s, %s, %s)
        on duplicate key update
        name = values(name), semester = values(semester), dept = values(dept)
        """
        cursor.executemany(sql, formatted_data)
        db_connection.commit()
    except Error as e:
        print(f"Error while updating database: {e}")

def update_sheet_data(sheet_service, data_to_update):
    try:
        body = {"values": data_to_update}
        sheet_service.spreadsheets().values().update (
            spreadsheet_id = SPREADSHEET_ID, range = RANGE_NAME,
            valueInputOption="USER_ENTERED", body = body).execute()
    except Error as err:
        print(f"An error occurred: {err}")


def sync_sheet_to_database(sheet_data, db_connection):
    if sheet_data and sheet_data[0][0] == 'SRN':
        sheet_data = sheet_data[1:]
    
    formatted_data = [(row[0], row[1], row[2], row[3]) for row in sheet_data]
    update_db_data(db_connection, formatted_data)

def get_db_data(db_connection):
    
    try:
        cursor = db_connection.cursor()
        cursor.execute("select * from spreadsheet")
        return cursor.fetchall()
    except Error as e:
        print(f"Error while fetching data from database: {e}")
        return []

def sync_database_to_sheet(db_data, sheets_service):
    data_to_update = [['SRN', 'Name','Semester','Department']] + db_data
    update_sheet_data = (sheets_service, data_to_update)


def main():
    sheets_service = get_google_sheets_service()
    db_connection = get_db_connection()

    if not db_connection:
        print("Failed to connect to the database!!!")
        return

    try:
        while True:
            ## Syncing Google sheets to database
            sheet_data = get_sheet_data(sheets_service)
            sync_sheet_to_database(sheet_data, db_connection)

            ## Syncing database to Google Sheets
            db_data = get_db_data(db_connection)
            sync_database_to_sheet(db_data, sheets_service)

            print("Sync complete!")
            time.sleep(30) # A wait time of 30 seconds before every sunc

    except KeyboardInterrupt as key_err:
        print(f"{key_err}")
    finally:
        if db_connection.is_connected():
            db_connection.close()



if __name__ == "__main__":
    main()

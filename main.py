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
    pass

def main():
    sheets_service = get_google_sheets_service()
    db_connection = get_db_connection()


if __name__ == "__main__":
    main()

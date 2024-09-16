# import os, time
# import mysql.connector
# from mysql.connector import Error
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# SPREADSHEET_ID = "1S5qrZ1y47Nn4b04EzHE9DPHMyV2rqU7J5qGx1l-WyI8"
# RANGE_NAME = "Sheet1!A:E"

# DB_CONFIG = {
#     'host': 'localhost',
#     'database': 'superJoinAi',
#     'user': 'root',
#     'password': 'Olivegreen@123'
# }

# def get_google_sheets_service():
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())
#     return build("sheets", "v4", credentials=creds)

# def get_db_connection():
#     try:
#         connection = mysql.connector.connect(**DB_CONFIG)
#         if connection.is_connected():
#             return connection
#     except Error as e:
#         print(f"Error while connecting to the DB: {e}")
#     return None

# def get_sheet_data(service):
#     try:
#         sheet = service.spreadsheets()
#         result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
#         return result.get("values: ", [])
#     except HttpError as error:
#         print(f"An error occured in getting the sheet data: {error}")
#     return []

# def update_db_data(db_connection, formatted_data):
#     try:
#         cursor = db_connection.cursor()
#         sql = """insert into spreadsheet (srn, name, semester, dept)
#         values (%s, %s, %s, %s)
#         on duplicate key update
#         name = values(name), semester = values(semester), dept = values(dept)
#         """
#         cursor.executemany(sql, formatted_data)
#         db_connection.commit()
#     except Error as e:
#         print(f"Error while updating database: {e}")

# def update_sheet_data(sheet_service, data_to_update):
#     try:
#         body = {"values": data_to_update}
#         sheet_service.spreadsheets().values().update (
#             spreadsheet_id = SPREADSHEET_ID, range = RANGE_NAME,
#             valueInputOption="USER_ENTERED", body = body).execute()
#     except Error as err:
#         print(f"An error occurred: {err}")


# def sync_sheet_to_database(sheet_data, db_connection):
#     if sheet_data and sheet_data[0][0] == 'SRN':
#         sheet_data = sheet_data[1:]
    
#     formatted_data = [(row[0], row[1], row[2], row[3]) for row in sheet_data]
#     update_db_data(db_connection, formatted_data)

# def get_db_data(db_connection):
    
#     try:
#         cursor = db_connection.cursor()
#         cursor.execute("select * from spreadsheet")
#         return cursor.fetchall()
#     except Error as e:
#         print(f"Error while fetching data from database: {e}")
#         return []

# def sync_database_to_sheet(db_data, sheets_service):
#     data_to_update = [['SRN', 'Name','Semester','Department']] + db_data
#     update_sheet_data = (sheets_service, data_to_update)


# def main():
#     sheets_service = get_google_sheets_service()
#     db_connection = get_db_connection()

#     if not db_connection:
#         print("Failed to connect to the database!!!")
#         return

#     try:
#         while True:
#             sheet_data = get_sheet_data(sheets_service)
#             sync_sheet_to_database(sheet_data, db_connection)

#             db_data = get_db_data(db_connection)
#             sync_database_to_sheet(db_data, sheets_service)

#             print("Sync complete!")
#             time.sleep(30) # A wait time of 30 seconds before every sunc

#     except KeyboardInterrupt as key_err:
#         print(f"{key_err}")
#     finally:
#         if db_connection.is_connected():
#             db_connection.close()



# if __name__ == "__main__":
#     main()





import os
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import mysql.connector
from mysql.connector import Error

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

def get_sheet_data(service):
    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        return result.get("values", [])
    except HttpError as err:
        print(f"An error occurred: {err}")
        return []

def update_sheet_data(service, values):
    try:
        body = {"values": values}
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
            valueInputOption="USER_ENTERED", body=body).execute()
    except HttpError as err:
        print(f"An error occurred: {err}")

def delete_sheet_row(service, row_index):
    try:
        request = {
            "requests": [
                {
                    "deleteDimension": {
                        "range": {
                            "sheetId": 0,
                            "dimension": "ROWS",
                            "startIndex": row_index,
                            "endIndex": row_index + 1
                        }
                    }
                }
            ]
        }
        service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=request).execute()
    except HttpError as err:
        print(f"An error occurred: {err}")

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    return None

def get_db_data(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM spreadsheet")
        return cursor.fetchall()
    except Error as e:
        print(f"Error while fetching data from MySQL: {e}")
        return []

def update_db_data(connection, data):
    try:
        cursor = connection.cursor()
        sql = """INSERT INTO spreadsheet (srn, name, semester, dept) 
         VALUES (%s, %s, %s, %s) 
         ON DUPLICATE KEY UPDATE 
         name = VALUES(name), semester = VALUES(semester), dept = VALUES(dept)"""
        cursor.executemany(sql, data)
        connection.commit()
    except Error as e:
        print(f"Error while updating MySQL: {e}")

def delete_db_row(connection, srn):
    try:
        cursor = connection.cursor()
        sql = "DELETE FROM spreadsheet WHERE srn = %s"
        cursor.execute(sql, (srn,))
        connection.commit()
    except Error as e:
        print(f"Error while deleting from MySQL: {e}")

def sync_sheet_to_db(sheet_data, db_connection):
    if sheet_data and sheet_data[0][0] == 'SRN':
        sheet_data = sheet_data[1:]

    db_data = get_db_data(db_connection)
    db_srns = set(row[0] for row in db_data)

    rows_to_update = []
    srns_in_sheet = set()

    for row in sheet_data:
        srn = row[0]
        srns_in_sheet.add(srn)
        rows_to_update.append((srn, row[1], row[2], row[3]))

    update_db_data(db_connection, rows_to_update)

    for db_srn in db_srns:
        if db_srn not in srns_in_sheet:
            delete_db_row(db_connection, db_srn)

def sync_db_to_sheet(db_data, sheets_service):
    rows_to_update = [['SRN', 'Name', 'Semester', 'Department']]  # Header row
    for row in db_data:
        rows_to_update.append(list(row))

    try:
        clear_request = sheets_service.spreadsheets().values().clear(
            spreadsheetId=SPREADSHEET_ID, 
            range=RANGE_NAME, 
            body={}
        )
        clear_request.execute()

        update_request = sheets_service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption="USER_ENTERED",
            body={"values": rows_to_update}
        )
        update_request.execute()

        print(f"Sheet updated successfully with {len(rows_to_update) - 1} rows of data.")
    except HttpError as err:
        print(f"An error occurred while updating the sheet: {err}")

def main():
    sheets_service = get_google_sheets_service()
    db_connection = get_db_connection()

    if not db_connection:
        print("Failed to connect to the database. Exiting.")
        return

    try:
        while True:
            db_data = get_db_data(db_connection)
            sync_db_to_sheet(db_data, sheets_service)

            sheet_data = get_sheet_data(sheets_service)
            sync_sheet_to_db(sheet_data, db_connection)

            print("Synchronization completed.")
            time.sleep(30)  # A wait time of 30 seconds before every sunc

    except KeyboardInterrupt:
        print("Synchronization stopped by user.")
    finally:
        if db_connection.is_connected():
            db_connection.close()

if __name__ == "__main__":
    main()
import os, time
import mysql.connector
from mysql.connector import Error
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = ""
RANGE_NAME = "Sheet1!A:E"

DB_CONFIG = {
    'host': 'localhost',
    'database': 'superJoinAi',
    'user': 'root',
    'password': ''
}


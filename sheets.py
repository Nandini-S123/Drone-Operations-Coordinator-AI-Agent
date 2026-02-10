import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_client():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json",
            SCOPES
        )

        # This automatically sets redirect_uri to localhost
        creds = flow.run_local_server(
            host="localhost",
            port=0,  # auto-pick free port
            authorization_prompt_message="",
            success_message="The authentication flow has completed. You may close this window."
        )


        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return gspread.authorize(creds)

def read_sheet(sheet_name):
    client = get_client()
    sheet = client.open(sheet_name).sheet1
    records = sheet.get_all_records()
    return records, sheet


def update_pilot_status(sheet, pilot_id, new_status):
    records = sheet.get_all_records()

    for idx, row in enumerate(records):
        if row["pilot_id"] == pilot_id:
            # Column 6 = status
            sheet.update_cell(idx + 2, 6, new_status)
            return True

    return False
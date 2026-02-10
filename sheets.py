import gspread
import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
import json

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

TOKEN_FILE = "token.json"

@st.cache_resource
def get_client():
    creds = None

    # Load token if it exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Refresh token if possible
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    # If still no valid creds → manual OAuth
    if not creds or not creds.valid:
        flow = Flow.from_client_config(
            {
                "web": st.secrets["google_oauth"]
            },
            scopes=SCOPES,
            redirect_uri=st.secrets["google_oauth"]["redirect_uri"]
        )

        auth_url, _ = flow.authorization_url(
            access_type="offline",
            prompt="consent"
        )

        st.warning("🔐 Google authorization required")
        st.markdown(f"[Click here to authorize]({auth_url})")

        auth_code = st.text_input("Paste the authorization code here")

        if not auth_code:
            st.stop()

        flow.fetch_token(code=auth_code)
        creds = flow.credentials

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return gspread.authorize(creds)


def read_sheet(sheet_name):
    client = get_client()
    sheet = client.open(sheet_name).sheet1
    return sheet.get_all_records(), sheet


def update_pilot_status(sheet, pilot_id, new_status):
    records = sheet.get_all_records()
    for idx, row in enumerate(records):
        if row.get("pilot_id") == pilot_id:
            sheet.update_cell(idx + 2, 6, new_status)
            return True
    return False

import gspread
import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_client():
    if "credentials" not in st.session_state:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": st.secrets["google_oauth"]["client_id"],
                    "client_secret": st.secrets["google_oauth"]["client_secret"],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [st.secrets["google_oauth"]["redirect_uri"]],
                }
            },
            scopes=SCOPES,
            redirect_uri=st.secrets["google_oauth"]["redirect_uri"],
        )

        # If Google has not redirected back yet
        if "code" not in st.query_params:
            auth_url, _ = flow.authorization_url(
                access_type="offline",
                prompt="consent"
            )
            st.markdown("### 🔐 Google authorization required")
            st.markdown(f"[Click here to authorize access]({auth_url})")
            st.stop()

        # Exchange auth code for token
        flow.fetch_token(code=st.query_params["code"])
        st.session_state.credentials = flow.credentials

    creds = Credentials(
        token=st.session_state.credentials.token,
        refresh_token=st.session_state.credentials.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=st.secrets["google_oauth"]["client_id"],
        client_secret=st.secrets["google_oauth"]["client_secret"],
        scopes=SCOPES,
    )

    return gspread.authorize(creds)

def read_sheet(sheet_name):
    client = get_client()
    sheet = client.open(sheet_name).sheet1
    return sheet.get_all_records(), sheet

def update_pilot_status(sheet, pilot_id, new_status):
    records = sheet.get_all_records()
    for idx, row in enumerate(records):
        if row["pilot_id"] == pilot_id:
            sheet.update_cell(idx + 2, 6, new_status)
            return True
    return False

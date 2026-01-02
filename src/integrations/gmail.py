# src/gmail.py

import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying scopes, delete token.json
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_service():
    """Authenticate and return Gmail API service."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def list_unread_emails():
    """Fetch unread emails."""
    service = get_service()
    results = service.users().messages().list(userId="me", labelIds=["UNREAD"]).execute()
    messages = results.get("messages", [])
    emails = []
    for msg in messages:
        m = service.users().messages().get(userId="me", id=msg["id"]).execute()
        snippet = m.get("snippet", "")
        emails.append({"id": msg["id"], "snippet": snippet})
    return emails

def send_reply(to: str, subject: str, body: str):
    """Send an email reply."""
    service = get_service()
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()

def get_message_details(message_id: str):
    """Fetch full message details (headers + snippet)."""
    service = get_service()
    msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()
    headers = msg["payload"]["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "")
    snippet = msg.get("snippet", "")
    return {"id": message_id, "subject": subject, "sender": sender, "snippet": snippet}


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return creds

def create_event(summary, start_time, end_time, attendees_emails, doctor):
    creds = get_credentials()
    if not creds or not creds.valid:
        return "Authorization required. Please authorize the application."
    
    try:
        service = build('calendar', 'v3', credentials=creds)

        attendees = [{'email': email} for email in attendees_emails]

        event = {
            'summary': summary,
            'description': f'Appointment with {doctor}',
            'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
            'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
            'attendees': attendees
        }

        event_result = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {event_result.get('htmlLink')}"
    except HttpError as error:
        return f"An error occurred: {error}"
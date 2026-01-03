import os.path
import uuid

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    creds = None

    # Load existing tokens
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Refresh or create new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Keep credentials.json in the same folder as this script for portability
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Unique requestId is required to create conference (Meet) details reliably
        meet_request_id = str(uuid.uuid4())

        event_body = {
            "summary": "Interview Session - AVIN",
            "location": "Online",
            "description": "Interview discussion and next steps.",
            "colorId": "6",
            "start": {
                "dateTime": "2026-01-10T19:00:00",
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": "2026-01-10T20:00:00",
                "timeZone": "Asia/Kolkata"
            },
            "recurrence": [
                "RRULE:FREQ=DAILY;COUNT=3"
            ],
            "attendees": [
                {"email": "samiha@gmail.com"},
                {"email": "samiha01@gmail.com"}
            ],
            "conferenceData": {
                "createRequest": {
                    "requestId": meet_request_id,
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    }
                }
            }
        }

        created = service.events().insert(
            calendarId="primary",
            body=event_body,
            conferenceDataVersion=1,
            sendUpdates="all"
        ).execute()

        print("Event created:", created.get("htmlLink"))

        # Extract Meet link if present
        meet_link = None
        conference_data = created.get("conferenceData", {})
        entry_points = conference_data.get("entryPoints", [])
        for ep in entry_points:
            if ep.get("entryPointType") == "video":
                meet_link = ep.get("uri")
                break

        if meet_link:
            print("Google Meet link:", meet_link)
        else:
            print("Meet link not found in response. Check if Meet is allowed for this account/domain.")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()

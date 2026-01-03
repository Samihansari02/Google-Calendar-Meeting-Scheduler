# Google Calendar API, Meeting Scheduler (Python)

Creates Google Calendar events with:
- attendees (email invites)
- recurrence rules
- optional Google Meet link generation

## Prerequisites
- Python 3.9+
- A Google Cloud project with Google Calendar API enabled

## Google Cloud Setup
1. Create/select a Google Cloud project.
2. Enable the Google Calendar API.
3. Configure OAuth consent screen (Testing is fine for personal use).
4. Create OAuth Client ID credentials: "Desktop app".
5. Download the OAuth client file and save it as `credentials.json` in the repo root.

Google quickstart reference:
https://developers.google.com/workspace/calendar/api/quickstart/python

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

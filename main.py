# Minimum required code to work with the Google Calendar API
# Derived from quickstart.py

from __future__ import print_function
from datetime import time,datetime, timedelta
import pytz
import os.path
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    dayOffset = -1
    calSelect = 5
    
    def getTime():
        # Get the time at the start and end of the day
        today = datetime.utcnow().date()+timedelta(days=dayOffset)
        startOfDay = datetime.combine(today, time()).isoformat() + 'Z'
        endOfDay = datetime.combine(today, time(23, 59, 59, 999999)).isoformat() + 'Z'
        return startOfDay, endOfDay

    startOfDay, endOfDay = getTime()

    # Gets the calendars from the user's account
    calList = service.calendarList().list(minAccessRole='writer').execute()
    # Create a list to save all the calendar IDs to
    ids = list()
    # iterate through the list of calendars and get each ID, append to the list
    for item in calList["items"]:
        ids.append(item["id"])
    #print(ids)

    calEvents = service.events().list(calendarId=ids[calSelect],singleEvents=True,timeMin=startOfDay,timeMax=endOfDay).execute()
    events = list()
    for item in calEvents["items"]:
        events.append(item["summary"])
    pprint(calEvents["summary"])
    pprint(events)

if __name__ == '__main__':
    main()
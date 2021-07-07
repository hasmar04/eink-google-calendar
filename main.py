'''
    eInk Google Calendar
    A beautiful calendar that shows your events from Google Calendar on an eInk display
    By Harrison Asmar
'''

#Dependencies
from __future__ import print_function
from datetime import time,datetime, timedelta
import pytz
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pprint import pprint

#Default day and Calendar (testing only)
dayOffset = 0
calSelect = 5
#Timezone configuration. Use timezones from docs/timezones.txt
timezone = pytz.timezone("Australia/Brisbane")

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
            creds = flow.run_console(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    gcal = build('calendar', 'v3', credentials=creds)
    
    def getTime():
        """
        Get the time at the start and end of the day
        
        Returns: 
        str:startOfDay
        str:endOfDay
        """
        day = datetime.utcnow().date()+timedelta(days=dayOffset)
        startOfDay = datetime.combine(day, time(second=0), tzinfo=timezone).isoformat()
        endOfDay = datetime.combine(day, time(23, 59, 59), tzinfo=timezone).isoformat()
        return startOfDay, endOfDay

    startOfDay, endOfDay = getTime()
    print(startOfDay)
    print(endOfDay)

    # Gets the calendars from the user's account
    calList = gcal.calendarList().list(minAccessRole='writer').execute()
    # Create a list to save all the calendar IDs to a list
    ids = list()
    # iterate through the list of calendars and get each ID, append to the list
    for item in calList["items"]:
        ids.append(item["id"])
    #print(ids)

    calEvents = gcal.events().list(calendarId=ids[calSelect],singleEvents=True,timeMin=startOfDay,timeMax=endOfDay).execute()
    events = list()
    for item in calEvents["items"]:
        events.append(item["start"])
        #if item["start"] == "*date': *":
            #print('true')
        print(str(item["summary"])+', '+str(item["start"])+', '+str(item["end"]))
    #pprint(calEvents["summary"])
    #pprint(events)

    #for item in events:
        #pprint(gcal.events().get(calendarId=ids[calSelect],eventId=item).execute()["summary"])

if __name__ == '__main__':
    main()
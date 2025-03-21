from googleapiclient.discovery import build
from app.services.google_auth_service import GoogleAuthService

class GoogleCalendarService:
  
    def __init__(self):
         self.google_auth_service = GoogleAuthService()
      
    def show_meeting(self, start_time:str,end_time:str, user_id: str= 13 ):
        credentials =  self.google_auth_service.get_user_credentials(user_id);
        service = build("calendar", "v3", credentials=credentials)
        events_result = service.events().list(
            calendarId="primary", timeMin=start_time, timeMax=end_time, singleEvents=True, orderBy="startTime", timeZone="Asia/Kolkata"
        ).execute()
        return events_result.get("items", [])
    
    def create_meeting(self, data:dict, user_id: str=13):
        
        event = {
            "summary": data["summary"],
            "description": data["description"],
            "start": {"dateTime": data["start_time"], "timeZone": data['time_zone']},
            "end": {"dateTime": data["end_time"], "timeZone": data['time_zone']},
            "attendees": [{"email": email} for email in data["attendees"]],
            "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": 30},  
                        {"method": "popup", "minutes": 10},  
                    ],
            },
        }
        
        if data["video_conference"] == True:
            event["conferenceData"] = {
                "createRequest": {
                    "requestId": "meeting-" + data["summary"],
                    "conferenceSolutionKey": {"type": "hangoutsMeet"}
                }
            }
       
        credentials =  self.google_auth_service.get_user_credentials(user_id)
        service = build("calendar", "v3", credentials=credentials)
        event = service.events().insert(
                calendarId="primary",
                body=event,
                sendUpdates="all", 
                conferenceDataVersion=1  
            ).execute()

        return {
                "event_id": event["id"],
                "meet_link": event["conferenceData"]["entryPoints"][0]["uri"] if data["video_conference"] else None,
                "status": "created",
                "attendees": data["attendees"]
                }
    
    def delete_meeting(self, event_id: str, user_id:int = 13):       
        credentials = self.google_auth_service.get_user_credentials(user_id) 
        service = build("calendar", "v3", credentials=credentials)
        service.events().delete(calendarId="primary", eventId=event_id).execute()
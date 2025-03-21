import cherrypy
from marshmallow import ValidationError
from app.services.google_auth_service import GoogleAuthService
from app.services.google_calendar_service import GoogleCalendarService
from googleapiclient.discovery import build
from app.schemas.create_meeting_schema import CreateMeetingSchema
from google.auth.exceptions import GoogleAuthError
from app.tools.auth import use_auth

use_auth()

class GoogleCalendarController:
    
    def __init__(self):
        self.google_auth_service = GoogleAuthService()
        self.google_calendar_service = GoogleCalendarService()
    
    @cherrypy.expose("meetings")
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.auth()
    def fetch_meetings(self, **param):
        start_time = param['start_date']
        end_time = param['end_date']
        user = cherrypy.request.user
        return self.google_calendar_service.show_meeting(start_time, end_time, user['id'])
        
    
    @cherrypy.expose("create_meeting")
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def create_meeting(self):
        
        if cherrypy.request.method == "OPTIONS": # to handle cors request
            cherrypy.response.status = 200
            cherrypy.response.body = b"ok"
            return 
    
        user = cherrypy.request.user
        data = cherrypy.request.json
        schema = CreateMeetingSchema()
        
        try:
            data = schema.load(data)
        except ValidationError as err:
            cherrypy.response.status = 400
            return {"error": err.messages}

        try:
           self.google_calendar_service.create_meeting(data, user['id']) 
        except GoogleAuthError as auth_error:
             return {"error": "Authentication failed", "details": str(auth_error)}
        except Exception as e:
            return {"error": "Failed to delete meeting", "details": str(e)}
        
    @cherrypy.expose("delete_meeting")
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def delete_meeting(self):
        
        if cherrypy.request.method == "OPTIONS": # to handle cors request
            cherrypy.response.status = 200
            cherrypy.response.body = b"ok"
            return 

        user = cherrypy.request.user
       
        try:
            data = cherrypy.request.json
            event_id = data.get("event_id")
            
            self.google_calendar_service.delete_meeting(event_id, user["id"])

            return {"status": "success", "message": "Meeting deleted successfully"}

        except GoogleAuthError as auth_error:
            return {"error": "Authentication failed", "details": str(auth_error)}

        except Exception as e:
            return {"error": "Failed to delete meeting", "details": str(e)}
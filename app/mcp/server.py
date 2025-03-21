from datetime import datetime
import sys
import os

import pytz

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))

from mcp.server.fastmcp import FastMCP
from app.services.google_calendar_service import GoogleCalendarService

mcp = FastMCP("google_calendar_api")
service = GoogleCalendarService()

@mcp.tool()
def current_date_time() -> str:
    """tool to get current date time """
    india_tz = pytz.timezone('Asia/Kolkata')
    current_datetime = datetime.now(india_tz).strftime('%Y-%m-%d %H:%M:%S')
    return current_datetime

@mcp.tool()
def create_meeting(meetingJsonData) -> int:
    
    """Create or Schedule Google Meetings 
    example meetingJsonData = {
        "summery" : "Daily Sprint Meeting",
        "description" : "Status about the current task and progress",
        "start_time" : "2025-01-01T01:00:00",
        "end_time" : "2025-01-01T02:00:00",
        "time_zone" : "Asia/Kolkata",
        "attendees" : ["sujanmoi787@gamil.com],
        "video_conference" : true
    } note- video-conference always default true and time_zone by default "Asia/Kolkata"""

    try:
        return service.create_meeting(meetingJsonData)
    except  Exception as e:
         return {"error": "Failed to create meeting", "details": str(e)}

@mcp.tool()
def show_meetings(start_date_time: str, end_date_time: str) -> int:
    """show the list of meetings base on start_date_time and end_date_time
    example start_date_time=2025-01-01T01:00:00Z example end_date_time=2025-01-01T02:00:00Z"""
    try:
        return service.show_meeting(start_date_time, end_date_time)
    except  Exception as e:
        return {"error": "Failed to fetch meeting", "details": str(e)}

@mcp.tool()
def delete_meetings(event_ids: list ) -> bool:
    """delete meetings example event_ids = ["GOCSPX-dYtZVbU7pk7Ac3sgb", "tZVbU7pk7Ac3sgb"]"""
    try:
        for event_id in event_ids:
            service.delete_meeting(event_id)
        
        return {"message" : "events has been deleted success fully"}    
    except  Exception as e:
        return {"error": "Failed to fetch meeting", "details": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")

    
    
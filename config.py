import os
from dotenv import load_dotenv

load_dotenv()

APP_SECRET = os.getenv("APP_SECRET")

# database

DATABASE_URL=os.getenv('DATABASE_URL')

# google credentials

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')
GOOGLE_CALENDAR_SCOPE = "https://www.googleapis.com/auth/calendar.events"
GOOGLE_PROFILE_SCOPE = "email profile"
import cherrypy
from app.tools.cors import cors_tool
from app.controllers.google_auth_controller import GoogleAuthController
from app.controllers.google_calendar_controller import GoogleCalendarController
from app.controllers.ai_agent_chat_controller import AiAgentChatController

cherrypy.tools.cors = cherrypy.Tool("before_handler", cors_tool)
 
cherrypy.config.update({
   "server.socket_host": "0.0.0.0",
    "server.socket_port": 8080,
    "tools.sessions.on": True,
    "tools.sessions.storage_type": "ram",  
    "tools.sessions.storage_class": cherrypy.lib.sessions.RamSession,  
    "tools.sessions.timeout": 60,
    "tools.cors.on": True,
    "tools.response_headers.on": True
})

config={"/": {  "tools.cors.on": True,  "tools.response_headers.on": True }}

cherrypy.tree.mount(GoogleAuthController(), "/api/auth/google", config=config)
cherrypy.tree.mount(GoogleCalendarController(), "/api/google-calendar", config=config)
cherrypy.tree.mount(AiAgentChatController(), "/api/ai-agent-chat", config=config)

cherrypy.engine.start()
cherrypy.engine.block()

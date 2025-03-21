from asyncio import sleep
import cherrypy
from app.utils.mcp_client import agent_invoke

class AiAgentChatController:
    
    def __init__(self):
        pass
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.allow(methods=["GET"])
    @cherrypy.tools.auth()
    def chat_histories(self, **param):
        limit = param['limit']
        user = cherrypy.request.user
        return {}
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    # @cherrypy.tools.auth()
    def create_chat(self):
        
        if cherrypy.request.method == "OPTIONS": # to handle cors request
            cherrypy.response.status = 200
            cherrypy.response.body = b"ok"
            return 
    
        # user = cherrypy.request.user
        data = cherrypy.request.json
        
        try:
            query = data["query"]
            response = agent_invoke(query)
            return {"text" : response, "role" : "AGENT"}
            
        except Exception as err:
            cherrypy.response.status = 400
            return {"error": str(err)}

        
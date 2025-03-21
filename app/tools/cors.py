import cherrypy

def cors_tool():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000" 
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "true" 

    if cherrypy.request.method == "OPTIONS":
        cherrypy.response.status = 200
        cherrypy.response.body = b"OK"
        return 


import webapp2
import sys
import json
import cgi
import ast
import Call_Email_timer
class MainHandler(webapp2.RequestHandler):
    
    def get(self):
        self.response.out.write("Hello, Carlos!")

    def post(self):
        blob = self.request.get('json')
        
        stuff = json.loads(blob)
        
        print stuff

app = webapp2.WSGIApplication([('/app/', MainHandler)],
                              debug=True)
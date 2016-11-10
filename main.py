

import os
import sys
import webapp2
import jinja2
import urlparse
import urllib

from google.appengine.api import urlfetch

from webapp2_extras import json

from webapp2 import Route as r

from logging import info, warn

XIRSYS_API_ENDPOINT = "https://service.xirsys.com"


def get_jinja_enviroment():
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader("./views"),
        extensions=['jinja2.ext.autoescape', 'jinja2.ext.i18n'],
        autoescape=True, trim_blocks=True, cache_size=400)
    

class Handler(webapp2.RequestHandler):
    """this is just a wrapper over webapp2.RequestHandler"""
    
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)

        self.template_values = {}

        self.jinja_enviroment = get_jinja_enviroment()

    def return_json(self, obj={}, status_code=200):

        self.response.content_type = 'application/json'
        self.response.set_status(status_code)

        try:

            self.response.write( json.encode(obj) )
        except Exception, e:
            warn(e)

            self.response.write( json.encode({}) )

def prepare_url(endpoint, username=None):

    data = {
        "ident": os.environ.get("XIRSYS_IDENT"),
        "secret": os.environ.get("XIRSYS_SECRET"),
        "domain": os.environ.get("XIRSYS_DOMAIN"),
        "application": os.environ.get("XIRSYS_APPLICATION"),
        "room": os.environ.get("XIRSYS_ROOM"),,
        "secure": 1
    }

    # if username:
        # data["username"] = username
    
    url = XIRSYS_API_ENDPOINT + endpoint + "?" + urllib.urlencode(data)

    # print the url so we can check it
    info(url)

    return url

class HomePage(Handler):

    def get(self):
        
        template = "index.html"        

        self.template = self.jinja_enviroment.get_template(template)
        
        # use the values from os
        self.template_values = {
            "domain": os.environ.get("XIRSYS_DOMAIN"),
            "application": os.environ.get("XIRSYS_APPLICATION"),
            "room": os.environ.get("XIRSYS_ROOM"),
        }
        page_content = self.template.render(self.template_values)

        self.response.write( page_content )


class SignalApi(Handler):

    def post(self):

        endpoint = "/signal/token"

        username = urlparse.parse_qs( self.request.body ).get('username', [''])[0]

        url = prepare_url(endpoint, username)

        response = urlfetch.fetch(url=url, method="GET")

        response = json.decode(response.content)
        
        info(response)

        if response["s"] != 200:
            warn("Problem getting a token from XirSys")        

        self.return_json(response)


class IceApi(Handler):

    def req(self):

        # endpoint = "/signal/token"
        endpoint = "/ice"

        username = urlparse.parse_qs( self.request.body ).get('username', [''])[0]

        url = prepare_url(endpoint, username)

        response = urlfetch.fetch(url=url, method="GET")

        response = json.decode(response.content)
        
        info(response)

        if response["s"] != 200:
            warn("Problem getting a token from XirSys")        

        self.return_json(response)

    def get(self):
        
        self.req()

    def post(self):

        self.req()


class ListApi(Handler):

    def req(self):
        endpoint = "/signal/list"

        username = urlparse.parse_qs( self.request.body ).get('username', [''])[0]

        url = prepare_url(endpoint, username)

        response = urlfetch.fetch(url=url, method="GET")

        response = json.decode(response.content)
        
        info(response)

        if response["s"] != 200:
            warn("Problem getting a token from XirSys")        

        self.return_json(response)

    def get(self):

        self.req()

    def post(self):

        self.req()




app = webapp2.WSGIApplication([
        r('/',              handler= HomePage,       name="home"),

        r('/signal/token',  handler= SignalApi,    name="api-token"),
        r('/ice',           handler= IceApi,       name="api-ice-servers"),
        r('/signal/list',   handler= ListApi,      name="api-servers-list")
    ],
    debug=True
)

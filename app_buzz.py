#!/usr/bin/env python
#

__author__ = 'Cameron Rodda'
__date__   = 'Sept 2014'

import os
import cherrypy
import jinja2
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates/').replace('\\','/') #to fix windows errors with os.path
STYLES_DIR = os.path.join(BASE_DIR,'styles/').replace('\\','/')
JS_DIR = os.path.join(BASE_DIR,'js/').replace('\\','/')
IMG_DIR = os.path.join(BASE_DIR,'images/').replace('\\','/')

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)

class Buzz(object):

    @cherrypy.expose
    def index(self):
        cherrypy.log.error(BASE_DIR)
        t = jinja_env.get_template('index.html')
        return t.render(name = "Camerons")
        #return "Hello Worlds!"

cherrypy.config.update({
    'server.socket_host': '127.0.0.1',
    'server.socket_port': 7000
})

config = {
    '/':
        {
        'tools.staticdir.debug': True,
        'log.screen': True,		
        },
    '/templates':
        {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': TEMPLATE_DIR
        },
    '/styles':
        {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': STYLES_DIR
        },
    '/js':
        {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': JS_DIR
        },
    '/images':
        {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': IMG_DIR
        }
}

cherrypy.tree.mount(Buzz(),'/',config=config)
cherrypy.engine.start()
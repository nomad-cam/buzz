#!/usr/bin/env python
#

__author__ = 'Cameron Rodda'
__date__   = 'Sept 2014'

import os
import cherrypy
import jinja2
import sqlite3 as lite
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates/').replace('\\','/') #to fix windows errors with os.path
STYLES_DIR = os.path.join(BASE_DIR,'styles/').replace('\\','/')
JS_DIR = os.path.join(BASE_DIR,'js/').replace('\\','/')
IMG_DIR = os.path.join(BASE_DIR,'images/').replace('\\','/')
DB_DIR = os.path.join(BASE_DIR,'db/').replace('\\','/')

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATE_DIR), autoescape=True)

try:
    pass
except lite.Error, e:
    cherrypy.log.error(e)
    raise e


class Buzz(object):

    @cherrypy.expose
    def index(self):
        cherrypy.log.error(BASE_DIR)
        t = jinja_env.get_template('index.html')
        return t.render(name = "Camerons")
    
    @cherrypy.expose
    def config(self):
        t = jinja_env.get_template('config.html')
        return t.render(name = "Camerons")

    @cherrypy.expose
    def hives(self):
        t = jinja_env.get_template('hives.html')
        return t.render(name = "Camerons")

    @cherrypy.expose
    def observe(self):
        db = lite.connect("%sBuzzLight.db" % DB_DIR)
        cur = db.cursor()
        cur.execute("SELECT * FROM beelog")
        data = cur.fetchall()
        db.close()

        #cherrypy.log.error(type(data).string)

        t = jinja_env.get_template('observe.html')
        return t.render(entries=data)

    @cherrypy.expose
    def location(self):
        t = jinja_env.get_template('location.html')
        return t.render(name = "Camerons")

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
cherrypy.engine.autoreload.on = True
cherrypy.engine.autoreload.files.add('app_buzz.py')
cherrypy.engine.start()
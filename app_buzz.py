#!/usr/bin/env python
#

__author__ = 'Cameron Rodda'
__date__   = 'Sept 2014'

import os
import cherrypy
import jinja2
import sqlite3 as lite
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')#to fix windows errors with os.path
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates/')
STYLES_DIR = os.path.join(BASE_DIR,'styles/')
JS_DIR = os.path.join(BASE_DIR,'js/')
IMG_DIR = os.path.join(BASE_DIR,'images/')
DB_DIR = os.path.join(BASE_DIR,'db/')
ICON_FILE = "%s/favicon.ico" % BASE_DIR

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
    def observe(self, **kws):
        db = lite.connect("%sBuzzLight.db" % DB_DIR)
        cur = db.cursor()

        if "add_entry" in kws:
            name = kws['name']
            date = kws['date']
            hive = kws['hive']
            notes = kws['notes']
            weather = kws['weather']

            cur.execute("INSERT INTO beelog (date_log,user,hive,notes,weather) "\
                        "VALUES (?,?,?,?,?)", (date,name,hive,notes,weather) )
            db.commit()


        cur.execute("SELECT * FROM beelog ORDER BY date(date_log) DESC")
        data = cur.fetchall()
        db.close()

        #cherrypy.log.error(type(data).string)
        current_date = datetime.datetime.now().strftime("%Y/%m/%d")

        t = jinja_env.get_template('observe.html')
        return t.render(entries=data, now=current_date)

    @cherrypy.expose
    def location(self, **kws):

        db = lite.connect("%sBuzzLight.db" % DB_DIR)
        cur = db.cursor()

        if "add_location" in kws:
            latti = kws['latt']
            longi = kws['long']
            hive = kws['hive']

            cur.execute("INSERT INTO LOCATION (latt,long,hive) "\
                        "VALUES (?,?,?)", (latti,longi,hive))
            db.commit()

        cur.execute("SELECT * FROM LOCATION")
        data = cur.fetchall()

        db.close()

        t = jinja_env.get_template('location.html')
        return t.render(locations=data)

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
        },
    '/favicon.ico':
        {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': ICON_FILE
        }
}

cherrypy.tree.mount(Buzz(),'/',config=config)
cherrypy.engine.autoreload.on = True
cherrypy.engine.autoreload.files.add('app_buzz.py')
cherrypy.engine.start()
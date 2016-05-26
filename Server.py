#!/usr/bin/python

import cherrypy
import json


class Root(object):
    @cherrypy.expose
    def index(self):
        with open('sensordata.json', 'r') as datafile:
            data = json.load(datafile)
            return rootResponse % (data['t'], data['h'], data['time'])

'''
class ConfigGet(object):
    @cherrypy.expose
    def configGet(self):
        with open('settings.json', 'r') as datafile:
            data = json.load(datafile)
            return rootResponse % (data['t'], data['h'], data['time'])
'''

rootResponse = """
<!DOCTYPE html>
<html>
<title>Sensor readings</title>
<body>
<h1>Temperature</h1>
<strong>%s</strong>
<h1>Humidity</h1>
<strong>%s</strong>
<h3>Time of measurement</h3>
<strong>%s</strong>
</body>
</html>
"""

if __name__ == '__main__':
    # cherrypy.tree.mount(ConfigGet(), '/config')
    cherrypy.server.socket_host = '0.0.0.0'
    # cherrypy.server.socket_port = 80
    cherrypy.quickstart(Root(), '/')

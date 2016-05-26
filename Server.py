#!/usr/bin/python

import cherrypy
import json
from cherrypy.lib.httputil import parse_query_string


class Root(object):
    @cherrypy.expose
    def index(self):
        with open('sensordata.json', 'r') as datafile:
            data = json.load(datafile)
            return rootResponse % (data['t'], data['h'], data['time'])


class ConfigGet(object):
    @cherrypy.expose
    def index(self):
        with open('settings.json', 'r') as datafile:
            data = json.load(datafile)
            motionEnable = 'checked' if data['motion_detection'] else ''
            return configGetResponse % (data['temperature_threshold'], data['humidity_threshold'], motionEnable, ' '.join(data['recipients']))


class ConfigSet(object):
    @cherrypy.expose
    def index(self, **args):
        params = parse_query_string(cherrypy.request.query_string)
        print params
        print args
        recipients = "["
        for rec in params['recipients'].split(' '):
            recipients += '"' + rec + '",'
        recipients = recipients[:-1]
        recipients += ']'
        motionEnable = 'true' if ('motion_detection' in params.keys()) else 'false'
        with open('settings.json', 'w') as datafile:
            datafile.write('{"motion_detection": %s,"temperature_threshold": %.1f,"humidity_threshold": %.1f,"recipients": %s}' % (motionEnable, float(params['temperature_threshold']), float(params['humidity_threshold']), recipients))
        raise cherrypy.HTTPRedirect("/")

rootResponse = """<!DOCTYPE html>
<html>
    <title>Sensor readings</title>
    <body>
        <h1>Temperature</h1>
        <strong>%s</strong>
        <h1>Humidity</h1>
        <strong>%s</strong>
        <h1>Time of measurement</h1>
        <strong>%s</strong>
        <p>To configure alerts, <a href="/config">click here</a>.</p>
    </body>
</html>
"""

configGetResponse = """<!DOCTYPE html>
<html>
<title>Configure Home Surveillance System</title>
<body>
<form action="/configSet">
    <h1>Temperature Alert Threshold</h1>
        <input id="temperature_threshold" name="temperature_threshold" type="text" value="%s">
    <h1>Humidity Alert Threshold</h1>
        <input id="humidity_threshold" name="humidity_threshold" type="text" value="%s">
    <h1>Motion detection</h1>
        <input type="checkbox" id="motion_detection" name="motion_detection" value="True" %s> Motion detection
    <h1>Alert email recipients</h1>
        <input id="recipients" name="recipients" type="text" value="%s" size="50">
        <input type="submit" value="Submit">
</form>
</body>
</html>
"""

if __name__ == '__main__':
    cherrypy.tree.mount(ConfigGet(), '/config')
    cherrypy.tree.mount(ConfigSet(), '/configSet')
    # cherrypy.tree.mount(Root(), '/')
    cherrypy.server.socket_host = '0.0.0.0'
    # cherrypy.server.socket_port = 80
    cherrypy.quickstart(Root(), '/')
    cherrypy.engine.start()
    cherrypy.engine.block()

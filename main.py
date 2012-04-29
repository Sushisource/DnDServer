from DnDSocket import DnDSocket
import os

import cherrypy as cp
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

from mako.template import Template
from mako.lookup import TemplateLookup

rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'www'))
class Root(object):
    def __init__(self, host, port, ssl=False):
        self.host = host
        self.port = port
        self.scheme = 'wss' if ssl else 'ws'

    @cp.expose
    def index(self):
        tlok = TemplateLookup(directories=rootdir,
                                output_encoding='utf-8',
                                input_encoding='utf-8')
        return tlok.get_template('index.mako').render()

    @cp.expose
    def ws(self):
        cp.log("Handler created: %s" % repr(cp.request.ws_handler))

if __name__ == '__main__':
    cp.config.update({'server.socket_host': '0.0.0.0',
                      'server.socket_port': 9000,
                      'tools.staticdir.root': rootdir})

    WebSocketPlugin(cp.engine).subscribe()
    cp.tools.websocket = WebSocketTool()

    cp.quickstart(Root('127.0.0.1', 9000, False), '', config={
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': DnDSocket
        },
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '.'
        }
    }
    )
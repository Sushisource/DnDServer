from DnDSocket import DnDSocket
import os, sys, inspect
import cherrypy as cp
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
import Spark

from mako.lookup import TemplateLookup

rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'www'))
class Root(object):
    def __init__(self, host, port, ssl=False):
        self.host = host
        self.port = port
        self.scheme = 'wss' if ssl else 'ws'
        self.tlok = TemplateLookup(directories=rootdir,
            output_encoding='utf-8',
            input_encoding='utf-8')
        #Dark magicks:
        self.dndfuncs = [x for x in inspect.getmembers(DnDSocket) if inspect.ismethod(x[1])]

    @cp.expose
    def index(self):
        return self.tlok.get_template('index.mako').render()

    @cp.expose
    def ws(self):
        cp.log("Handler created: %s" % repr(cp.request.ws_handler))

    @cp.expose
    def dicehisto(self, list, **args):
        cp.response.headers['Content-Type'] = 'image/png'
        list = [int(x) for x in list.split(',')]
        return Spark.plot_sparkline_discrete(list,args,True)

if __name__ == '__main__':
    cp.config.update({'server.socket_host': '0.0.0.0',
                      'server.socket_port': 9000,
                      'engine.autoreload_on': False,
                      'tools.staticdir.root': rootdir,
                      'log.screen': False})

    WebSocketPlugin(cp.engine).subscribe()
    cp.tools.websocket = WebSocketTool()

    root = Root('127.0.0.1', 9000, False)

    cp.Application.root = root
    cp.quickstart(root, '', config={
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': DnDSocket
        },
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '.'}})

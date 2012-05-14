from functools import partial
from DnDSocket import DnDSocket
import os, sys, inspect
import cherrypy as cp
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from InitlistManager import InitlistManager
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
        #Setup our managers. Foreach take their members and add a method of the same
        #name to it, but where we wrap the return value in a send message. This employs
        #the darkest of python magicks
        self.ilm = InitlistManager()
        self.add_mgr_methods_to_socket(self.ilm)
        self.dndfuncs = [x for x in inspect.getmembers(DnDSocket) if inspect.ismethod(x[1])]

    def add_mgr_methods_to_socket(self, manager):
        for ilf in inspect.getmembers(manager):
            if inspect.ismethod(ilf[1]) and ilf[0] != "__init__":
                def usethis(function):
                    def sendwrapper(self, data):
                        self.send_message(*function(data))
                    return sendwrapper
                retme = usethis(ilf[1])
                retme.__name__ = ilf[0]
                setattr(DnDSocket, ilf[0], retme)

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
    port = 9000
    cp.config.update({'server.socket_host': '0.0.0.0',
                      'server.socket_port': port,
                      'engine.autoreload_on': False,
                      'tools.staticdir.root': rootdir,
                      'log.screen': False})

    WebSocketPlugin(cp.engine).subscribe()
    cp.tools.websocket = WebSocketTool()

    root = Root('127.0.0.1', port, False)

    cp.Application.root = root
    cp.quickstart(root, '', config={
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': DnDSocket
        },
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '.'}})

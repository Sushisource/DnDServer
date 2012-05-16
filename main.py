import os, sys, inspect, Spark, signal
import cPickle as pickle
import cherrypy as cp
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from mako.lookup import TemplateLookup
from DnDSocket import DnDSocket
from InitlistManager import InitlistManager
from StoreableManager import StoreableManager
from UserManager import UserManager

rootdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'www'))
class DnDRoot(object):
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
        self.managers = list()
        self.ilm = InitlistManager()
        self.add_mgr_methods_to_socket(self.ilm)
        self.storem = StoreableManager()
        self.add_mgr_methods_to_socket(self.storem)
        self.usermgr = UserManager()
        self.add_mgr_methods_to_socket(self.usermgr)
        self.dndfuncs = [x for x in inspect.getmembers(DnDSocket)
                         if inspect.ismethod(x[1]) and hasattr(x[1], 'is_callable')]

    def add_mgr_methods_to_socket(self, manager):
        """
        Darkest magicks method. Takes an object, and adds each of its
        functions which are not the constructor to the DnDSocket class,
        wrapping them to call send message on the expansion of each
        tuple in the return list of messages to send

        We dont add methods that start with a _ "ie: private methods"

        Also we add them to our list of managers, so they'll send and save
        state information.
        """
        self.managers.append(manager)

        for ilf in inspect.getmembers(manager):
            if inspect.ismethod(ilf[1]) and not str.startswith(ilf[0],'_'):
                def usethis(function):
                    def sendwrapper(self, data):
                        messages = function(data)
                        for msg in messages:
                            self.send_message(*msg)
                    sendwrapper.is_callable = True
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

    root = DnDRoot('127.0.0.1', port, False)
    cp.Application.root = root

    cp.quickstart(root, '', config={
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': DnDSocket
        },
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '.'}})

from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
from json import dumps
import cherrypy as cp

class DnDSocket(WebSocket):
    chars = {}

    def received_message(self, message):
        print message.data
        if not message.is_binary:
            eval("self."+str(message.data))

    def get_state(self):
        greet ="Sending state\n"
        self.send_message("echo", greet, True)
        self.send_initlist()

    def add_char(self, charname, initiative):
        if charname in self.chars:
            self.chars[charname].initiative = initiative
            self.send_message('updatechar', self.chars[charname].to_dict())
            return
        char = Character(charname)
        char.initiative = initiative
        self.chars[charname] = char
        self.send_message('addchar', char.to_dict())

    def del_char(self, charname):
        del self.chars[charname]
        self.send_message('delchar', charname)

    def send_initlist(self):
        initlist = {}
        for char in self.chars.values():
            initlist[char.name] = char.initiative
        self.send_message('initlist', initlist, True)

    def send_message(self, protocol, data, private=False):
        m = dumps((protocol, data))
        if not private:
            cp.engine.publish('websocket-broadcast', TextMessage(m))
        else:
            self.send(m,False)

    def ekko(self, msg):
        self.send_message('echo', msg)

    def closed(self, code, reason=None):
        print "client disconnect"


class Character:
    def __init__(self, name):
        self.name = name
        self.initiative = 0

    def to_dict(self):
        ret = {'name': self.name, 'init': self.initiative}
        return ret

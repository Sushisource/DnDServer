from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
from json import dumps, loads
import types
import cherrypy as cp
from cherrypy import Application as cpa

def callable(func):
    func.is_callable = True
    return func

class DnDSocket(WebSocket):
    def __init__(self, sock, protocols=None, extensions=None, environ=None):
        super(DnDSocket, self).__init__(sock, protocols, extensions, environ)

    @callable
    def get_state(self, data):
        #Welcome mat
        self.serverchat("Welcome to DnD Server {0}!".format(self.uname))
        #Send state
        msgs = self.produce_state()
        for msg in msgs:
            self.send_message(*msg)

    @callable
    def userchat(self, message):
        self.send_message('titlealert', "-- New chat --")
        input = message['msg']
        if input.startswith('/'):
            cpa.root.cmdh.do_command(input, self)
        else:
            msg = {'name': self.uname, 'msg': input}
            self.send_message('chat', msg)

    @callable
    def reset(self, reason):
        print "Resetting because {0}".format(reason)
        cpa.root.reset()

    def produce_state(self):
        #Send state from every manager
        msgs = list()
        for manager in cpa.root.managers:
            msgs.extend(manager._send_state())
        cpa.root.dndstate = msgs
        return msgs

    def save_state(self):
        for manager in cpa.root.managers:
            manager._save_state()

    def received_message(self, message):
        if not message.is_binary:
            try:
                msg = loads(str(message))
                for func in cpa.root.dndfuncs:
                    if msg['fn'] == func[0]:
                        #Extra dark magicks:
                        boundf = types.MethodType(func[1], self, DnDSocket)
                        boundf(msg['data'])
                        print "%s runs %s" % (self.uname, msg['fn'])
            except Exception as err:
                print "Couldn't run: %s" % message.data
                print err

    def send_message(self, protocol, data, private=False):
        sendme = dumps((protocol, data))
        #Hack to set user particulars
        if protocol == "user_response":
            self.uname = data['name']
            self.m_uid = data['id']
        if not private:
            cp.engine.publish('websocket-broadcast', TextMessage(sendme))
        else:
            self.send(sendme, False)

    def serverchat(self, message):
          self.send_message('chat',
                  {'name': "Chief Ripnugget",
                   'msg': message})

    def closed(self, code, reason=None):
        try:
            self.send_message('deluser', self.m_uid)
            cpa.root.usermgr._del_user(self.m_uid)
            print "client disconnect"
        except Exception as e:
            #Phantom client. Better print message
            print "Orphaned client refresh"
            print e

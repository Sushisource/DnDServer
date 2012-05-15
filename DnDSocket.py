from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
from json import dumps, loads
import types
import cherrypy as cp
from cherrypy import Application as cpa
from Roller import rollDice

class DnDSocket(WebSocket):

    def __init__(self, sock, protocols=None, extensions=None, environ=None):
        super(DnDSocket, self).__init__(sock, protocols, extensions, environ)
        self.m_uid = None
        self.uname = "Redshirt"

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
        if not private:
            cp.engine.publish('websocket-broadcast', TextMessage(sendme))
        else:
            self.send(sendme, False)

    def get_state(self, data):
        greet = "Sending state\n"
        self.send_message("echo", greet, True)
        #Send the userlist
        for uid, uname in cpa.root.usermgr.enum_users():
            if uid is not self.m_uid:
                self.send_message('ouser_response',
                        {'name': uname, 'id': uid}, True)
        #Send initiative list
        self.send_initlist(None)
        #Send the storeables
        self.send_storeables(None)
        #Welcome mat
        self.send_message('chat',
                {'name': "Chief Ripnugget",
                 'msg': "Welcome to DnD Server %s!" % self.uname})

    def add_user(self, data):
        uname = data['name']
        self.m_uid = cpa.root.usermgr.add_user(uname)
        self.uname = uname
        self.send_message('user_response', {'name': uname, 'id': self.m_uid}, True)
        self.send_message('ouser_response', {'name': uname, 'id': self.m_uid})

    def userchat(self, message):
        msg = {'name': self.uname, 'msg': message['msg']}
        self.send_message('chat', msg)

    def dicebox(self, data):
        rollstr = data['rollstr']
        result = rollDice(rollstr)
        tlok = cpa.root.tlok
        result = tlok.get_template('diceresult.mako').render(query=rollstr,
            total=result)
        self.send_message("diceroll",
                {'result': result,
                 'name': self.uname})

    def closed(self, code, reason=None):
        try:
            cpa.root.usermgr.del_user(self.m_uid)
            self.send_message('deluser', self.m_uid)
            print "client disconnect"
        except Exception:
            #Phantom client. Better print message
            print "Orphaned client refresh"

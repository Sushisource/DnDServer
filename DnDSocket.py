from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
from json import dumps, loads
import types
import cherrypy as cp
from cherrypy import Application as cpa
from Roller import rollDice

def callable(func):
    func.is_callable = True
    return func

class DnDSocket(WebSocket):

    def __init__(self, sock, protocols=None, extensions=None, environ=None):
        super(DnDSocket, self).__init__(sock, protocols, extensions, environ)

    @callable
    def get_state(self, data):
        greet = "Sending state\n"
        self.send_message("echo", greet, True)
        #Send the userlist
        msgs = cpa.root.usermgr._send_ulist(self.m_uid)
        #Send initiative list
        msgs.extend(cpa.root.ilm._send_initlist())
        #Send the storeables
        msgs.extend(cpa.root.storem._send_storeables())
        #Welcome mat
        self.serverchat("Welcome to DnD Server %s!" % self.uname)
        #Send all the messages we've built up
        for msg in msgs:
            self.send_message(*msg)

    @callable
    def userchat(self, message):
        msg = {'name': self.uname, 'msg': message['msg']}
        self.send_message('chat', msg)

    @callable
    def dicebox(self, data):
        rollstr = data['rollstr']
        result = rollDice(rollstr)
        tlok = cpa.root.tlok
        result = tlok.get_template('diceresult.mako').render(query=rollstr,
            total=result)
        self.send_message("diceroll",
                {'result': result,
                 'name': self.uname})

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

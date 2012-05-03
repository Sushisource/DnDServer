from ws4py.websocket import WebSocket
from Storable import Storable
from ws4py.messaging import TextMessage
from json import dumps, loads
import cherrypy as cp
from Roller import rollDice

class DnDSocket(WebSocket):
    ilist_chars = {}
    next_i_id = {'next': 0}
    users = {}
    next_uid = {'next': 0}
    storables = {}
    next_storid = {'next': 0}
    m_uid = None

    def received_message(self, message):
        if self.m_uid is not None:
            print "%s runs %s" % (self.users[self.m_uid], str(message.data))
        if not message.is_binary:
            try:
                eval("self."+str(message.data))
            except AttributeError as e:
                print "Couldn't run: %s" % message.data
                print e

    def get_state(self):
        greet ="Sending state\n"
        self.send_message("echo", greet, True)
        self.send_initlist()
        #Send the userlist
        for id, uname in self.users.items():
            if id is not self.m_uid:
                self.send_message('ouser_response', {'name': uname, 'id': id}, True)
        #Send the storeables
        for id in self.storables.keys():
            self.render_storeable(id, True)
        #Welcome mat
        self.send_message('chat',
                {'name': "Chief Ripnugget",
                 'msg': "Welcome to DnD Server %s!" % self.users[self.m_uid]})

    def add_inititem(self, charname, initiative):
        if charname in self.ilist_chars:
            self.ilist_chars[charname].initiative = initiative
            self.send_message('updatechar', self.ilist_chars[charname].to_dict())
            return
        char = InitlistObject(charname, self.next_i_id['next'])
        self.next_i_id['next'] += 1
        char.initiative = initiative
        self.ilist_chars[charname] = char
        self.send_message('addchar', char.to_dict())

    def del_inititem(self, charname):
        self.send_message('delchar', self.ilist_chars[charname].to_dict())
        del self.ilist_chars[charname]

    def send_initlist(self):
        initlist = {}
        for char in self.ilist_chars.values():
            initlist[char.name] = char.to_dict()
        self.send_message('initlist', initlist, True)

    def send_message(self, protocol, data, private=False):
        m = dumps((protocol, data))
        if not private:
            cp.engine.publish('websocket-broadcast', TextMessage(m))
        else:
            self.send(m,False)

    def add_user(self, uname):
        uid = self.next_uid['next']
        self.users[uid] = uname
        self.m_uid = uid
        self.next_uid['next'] += 1
        print "New user %s id: %d" % (uname, uid)
        self.send_message('user_response', {'name': uname, 'id': uid}, True)
        self.send_message('ouser_response', {'name': uname, 'id': uid})

    def dicebox(self, rollstr):
        result = rollDice(rollstr)
        tlok = cp.Application.root.tlok
        result = tlok.get_template('diceresult.mako').render(query=rollstr,
            total=result)
        self.send_message("diceroll",
                {'result': result, 'query': rollstr,
                 'name': self.users[self.m_uid]})

    def update_storeable(self, id, data):
        id = int(id)
        data = loads(data)
        self.storables[id] = dict(self.storables[id].items() + data.items())

    def add_storeable(self, templatename, data):
        id = self.next_storid['next']
        data = loads(data)
        storeme = Storable(templatename,id,data)
        self.next_storid['next'] += 1
        self.storables[id] = storeme
        print "New storeable type:%s data:%s" % (templatename, data)
        self.render_storeable(id, False)

    def render_storeable(self, id, solo):
        id = int(id)
        output = self.storables[id].render()
        callback = self.storables[id].callback
        print output
        self.send_message("showstoreable", output, solo)
        if callback is not None:
            self.send_message(callback, id)

    def ekko(self, msg):
        self.send_message('echo', msg)

    def closed(self, code, reason=None):
        try:
            print "Deleted user: " + self.users[self.m_uid]
            self.send_message('deluser', self.m_uid)
            del self.users[self.m_uid]
            print "client disconnect"
        except Exception:
            #Phantom client. Better print message
            print "Orphaned client refresh"


class InitlistObject:
    def __init__(self, name, id):
        self.name = name
        self.initiative = 0
        self.id = id

    def to_dict(self):
        ret = {'name': self.name, 'init': self.initiative, 'id': self.id}
        print ret
        return ret

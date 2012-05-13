from ws4py.websocket import WebSocket
from Storable import Storable
from ws4py.messaging import TextMessage
from json import dumps, loads
import cherrypy as cp, types
from Roller import rollDice

class DnDSocket(WebSocket):
    ilist_chars = {}
    next_i_id = {'next': 0}
    users = {}
    next_uid = {'next': 0}
    storeables = {}
    next_storid = {'next': 0}
    m_uid = None

    def received_message(self, message):
        if not message.is_binary:
            try:
                msg = loads(str(message))
                for func in cp.Application.root.dndfuncs:
                    if msg['fn'] == func[0]:
                        #Extra dark magicks:
                        boundf = types.MethodType(func[1], self, DnDSocket)
                        boundf(msg['data'])
                        print "%s runs %s" % (self.users[self.m_uid], msg['fn'])
            except Exception as err:
                print "Couldn't run: %s" % message.data
                print err

    def get_state(self, data):
        greet = "Sending state\n"
        self.send_message("echo", greet, True)
        self.send_initlist(None)
        #Send the userlist
        for uid, uname in self.users.items():
            if uid is not self.m_uid:
                self.send_message('ouser_response',
                        {'name': uname, 'id': uid}, True)
        #Send the storeables
        for uid in self.storeables.keys():
            self.render_storeable(uid, True)
        #Welcome mat
        self.send_message('chat',
                {'name': "Chief Ripnugget",
                 'msg': "Welcome to DnD Server %s!" % self.users[self.m_uid]})

    def add_inititem(self, data):
        charname = data['name']
        initiative = data['initiative']
        if charname in self.ilist_chars:
            self.ilist_chars[charname].initiative = initiative
            self.send_message('updatechar',
                self.ilist_chars[charname].to_dict())
            return
        char = InitlistObject(charname, self.next_i_id['next'])
        self.next_i_id['next'] += 1
        char.initiative = initiative
        self.ilist_chars[charname] = char
        self.send_message('addchar', char.to_dict())

    def del_inititem(self, data):
        charname = data['name']
        self.send_message('delchar', self.ilist_chars[charname].to_dict())
        del self.ilist_chars[charname]

    def send_initlist(self, data):
        initlist = {}
        for char in self.ilist_chars.values():
            initlist[char.name] = char.to_dict()
        self.send_message('initlist', initlist, True)

    def send_message(self, protocol, data, private=False):
        sendme = dumps((protocol, data))
        if not private:
            cp.engine.publish('websocket-broadcast', TextMessage(sendme))
        else:
            self.send(sendme, False)

    def add_user(self, data):
        uid = self.next_uid['next']
        uname = data['name']
        self.users[uid] = uname
        self.m_uid = uid
        self.next_uid['next'] += 1
        print "New user %s id: %d" % (uname, uid)
        self.send_message('user_response', {'name': uname, 'id': uid}, True)
        self.send_message('ouser_response', {'name': uname, 'id': uid})

    def userchat(self, message):
        uname = self.users[self.m_uid]
        msg = {'name': uname, 'msg': message['msg']}
        self.send_message('chat', msg)

    def dicebox(self, data):
        rollstr = data['rollstr']
        result = rollDice(rollstr)
        tlok = cp.Application.root.tlok
        result = tlok.get_template('diceresult.mako').render(query=rollstr,
            total=result)
        self.send_message("diceroll",
                {'result': result,
                 'name': self.users[self.m_uid]})

    def update_storeable(self, data):
        store_id = int(data['id'])
        subdict = data['subdict_name']
        if subdict not in self.storeables[store_id].data:
            self.storeables[store_id].data[subdict] = {}
        updated = dict(self.storeables[store_id].data[subdict].items() + data['subdict'].items())
        self.storeables[store_id].data[subdict] = updated
        self.re_render_storeable(store_id)

    def add_storeable(self, data):
        store_id = self.next_storid['next']
        templatename = data['template']
        storeme = Storable(templatename, store_id, data)
        self.next_storid['next'] += 1
        self.storeables[store_id] = storeme
        print "New storeable type:%s data:%s" % (templatename, data)
        self.render_storeable(store_id, False)

    def render_storeable(self, store_id, solo):
        store_id = int(store_id)
        output = self.storeables[store_id].render()
        callback = self.storeables[store_id].callback
        self.send_message("showstoreable",
                {'output': output, 'id': store_id}, solo)
        if callback is not None:
            self.send_message(callback, store_id)

    def re_render_storeable(self, store_id, solo=False):
        store_id = int(store_id)
        output = self.storeables[store_id].render()
        callback = self.storeables[store_id].callback
        self.send_message("updatestoreable",
                {'output': output, 'id': store_id}, solo)
        if callback is not None:
            self.send_message(callback, store_id)

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
    def __init__(self, name, m_id):
        self.name = name
        self.initiative = 0
        self.id = m_id

    def to_dict(self):
        ret = {'name': self.name, 'init': self.initiative, 'id': self.id}
        print ret
        return ret

from Manager import Manager

class InitlistManager(Manager):
    def add_inititem(self, data):
        charname = data['name']
        initiative = data['initiative']
        if charname in self.manageditems:
            self.manageditems[charname].initiative = initiative
            return [('updatechar', self.manageditems[charname].to_dict())]
        char = InitlistObject(charname, self.next_itemid)
        self.next_itemid += 1
        char.initiative = initiative
        self.manageditems[charname] = char
        return [('addchar', char.to_dict())]

    def del_inititem(self, data):
        charname = data['name']
        dict = self.manageditems[charname].to_dict()
        del self.manageditems[charname]
        return [('delchar', dict)]

    def _send_state(self):
        initlist = {}
        for char in self.manageditems.values():
            initlist[char.name] = char.to_dict()
        return [('initlist', initlist, True)]


class InitlistObject:
    def __init__(self, name, m_id):
        self.name = name
        self.initiative = 0
        self.id = m_id

    def to_dict(self):
        ret = {'name': self.name, 'init': self.initiative, 'id': self.id}
        return ret
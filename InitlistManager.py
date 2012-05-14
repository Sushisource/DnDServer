class InitlistManager:

    def __init__(self):
        self.ilist_chars = {}
        self.next_id = 0

    def add_inititem(self, data):
         charname = data['name']
         initiative = data['initiative']
         if charname in self.ilist_chars:
             self.ilist_chars[charname].initiative = initiative
             return ('updatechar', self.ilist_chars[charname].to_dict())
         char = InitlistObject(charname, self.next_id)
         self.next_id += 1
         char.initiative = initiative
         self.ilist_chars[charname] = char
         return ('addchar', char.to_dict())

    def del_inititem(self, data):
         charname = data['name']
         dict = self.ilist_chars[charname].to_dict()
         del self.ilist_chars[charname]
         return ('delchar', dict)

    def send_initlist(self, data):
         initlist = {}
         for char in self.ilist_chars.values():
             initlist[char.name] = char.to_dict()
         return ('initlist', initlist, True)

class InitlistObject:
    def __init__(self, name, m_id):
        self.name = name
        self.initiative = 0
        self.id = m_id

    def to_dict(self):
        ret = {'name': self.name, 'init': self.initiative, 'id': self.id}
        print ret
        return ret
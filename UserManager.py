from Manager import Manager

class UserManager(Manager):
    def add_user(self, data):
        name = data['name']
        self.manageditems[self.next_itemid] = name
        uid = self.next_itemid
        self.next_itemid += 1
        print "New user %s id: %d" % (name, uid)
        ret = [('user_response', {'name': name, 'id': uid}, True)]
        ret.append(('ouser_response', {'name': name, 'id': uid}))
        return ret

    def _del_user(self, uid):
        print "Deleted user: " + self.manageditems[uid]
        del self.manageditems[uid]

    def _send_state(self):
        ret = list()
        for uid, uname in self.manageditems.items():
                ret.append(('ouser_response', {'name': uname, 'id': uid}, True))
        return ret

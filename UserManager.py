class UserManager:

    def __init__(self):
        self.users = {}
        self.next_id = 0

    def add_user(self, data):
        name = data['name']
        self.users[self.next_id] = name
        uid = self.next_id
        self.next_id += 1
        print "New user %s id: %d" % (name, uid)
        ret = [('user_response', {'name': name, 'id': uid}, True)]
        ret.append(('ouser_response', {'name': name, 'id': uid}))
        return ret

    def del_user(self, uid):
        print "Deleted user: " + self.users[uid]
        del self.users[uid]

    def _send_ulist(self, id):
        ret = list()
        for uid, uname in self.users.items():
            if uid is not id:
                ret.append(('ouser_response', {'name': uname, 'id': uid}, True))
        return ret

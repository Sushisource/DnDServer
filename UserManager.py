class UserManager:

    def __init__(self):
        self.users = {}
        self.next_id = 0

    def add_user(self, name):
        self.users[self.next_id] = name
        uid = self.next_id
        self.next_id += 1
        print "New user %s id: %d" % (name, uid)
        return uid

    def get_name(self, uid):
        return self.users[uid]

    def del_user(self, uid):
        print "Deleted user: " + self.users[uid]
        del self.users[uid]

    def enum_users(self):
        return self.users.items()

from Manager import Manager
from Storable import Storable

class StoreableManager(Manager):
    def update_storeable(self, data):
         store_id = int(data['id'])
         subdict = data['subdict_name']
         if subdict not in self.manageditems[store_id].data:
             self.manageditems[store_id].data[subdict] = {}
         updated = dict(self.manageditems[store_id].data[subdict].items() + data['subdict'].items())
         self.manageditems[store_id].data[subdict] = updated
         return self.render_storeable(store_id, rerender=True)

    def add_storeable(self, data):
        store_id = self.next_itemid
        self.next_itemid += 1
        templatename = data['template']
        storeme = Storable(templatename, store_id, data)
        self.manageditems[store_id] = storeme
        print "New storeable type:%s data:%s" % (templatename, data)
        return self.render_storeable(store_id, False)

    def render_storeable(self, store_id, solo=False, rerender=False):
        store_id = int(store_id)
        output = self.manageditems[store_id].render()
        callback = self.manageditems[store_id].callback
        jsfn = "updatestoreable" if rerender else "showstoreable"
        retme = [(jsfn, {'output': output, 'id': store_id}, solo)]
        if callback is not None:
            retme.append((callback, store_id))
        return retme

    def _send_state(self):
        retme = list()
        for stid in self.manageditems.keys():
            retme.extend(self.render_storeable(stid, True))
        return retme

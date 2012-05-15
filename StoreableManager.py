from Storable import Storable

class StoreableManager:

    def __init__(self):
        self.storeables = {}
        self.next_storid = 0

    def update_storeable(self, data):
         store_id = int(data['id'])
         subdict = data['subdict_name']
         if subdict not in self.storeables[store_id].data:
             self.storeables[store_id].data[subdict] = {}
         updated = dict(self.storeables[store_id].data[subdict].items() + data['subdict'].items())
         self.storeables[store_id].data[subdict] = updated
         return self.render_storeable(store_id, rerender=True)

    def add_storeable(self, data):
        store_id = self.next_storid
        self.next_storid += 1
        templatename = data['template']
        storeme = Storable(templatename, store_id, data)
        self.storeables[store_id] = storeme
        print "New storeable type:%s data:%s" % (templatename, data)
        return self.render_storeable(store_id, False)

    def render_storeable(self, store_id, solo=False, rerender=False):
        store_id = int(store_id)
        output = self.storeables[store_id].render()
        callback = self.storeables[store_id].callback
        jsfn = "updatestoreable" if rerender else "showstoreable"
        retme = [(jsfn, {'output': output, 'id': store_id}, solo)]
        if callback is not None:
            retme.append((callback, store_id))
        return retme

    def send_storeables(self, data):
        retme = list()
        for stid in self.storeables.keys():
            retme.extend(self.render_storeable(stid, True))
        return retme

import abc

class Manager:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.manageditems = dict()
        self.next_itemid = 0

    @abc.abstractmethod
    def _send_state(self):
        """This method must return a list of
        messages to be sent during get_state()"""
        return

    def _save_state(self):
        pass


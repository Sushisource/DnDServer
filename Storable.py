import cherrypy as cp

class Storable:

    def __init__(self, templatename, id, data):
        self.m_template_lk = cp.Application.root.tlok
        self.m_template_lk.get_template(templatename)
        self.data = data
        self.id = id

    def render(self):
        self.m_template_lk.render(data=self.data, id=self.id)
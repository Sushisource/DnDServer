import cherrypy as cp

class Storable:

    def __init__(self, templatename, id, data):
        self.m_template_lk = cp.Application.root.tlok
        self.templname = templatename
        self.data = data
        self.id = id
        if 'callback' in self.data:
            self.callback = self.data['callback']

    def render(self):
        template = self.m_template_lk.get_template(self.templname)
        return template.render(data=self.data, id=self.id)
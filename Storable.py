import cherrypy as cp

class Storable:

    def __init__(self, templatename, id, data):
        self.m_template_lk = cp.Application.root.tlok
        self.templname = templatename
        self.data = {}
        self.data['root'] = data
        self.id = id
        if 'callback' in self.data['root']:
            self.callback = self.data['root']['callback']

    def render(self):
        template = self.m_template_lk.get_template(self.templname)
        return template.render(root=self.data['root'], data=self.data, id=self.id)
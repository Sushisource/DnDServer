import cherrypy as cp

class Storable:

    """
    Generic class for storing information and rendering it with a mako template
    """

    def __init__(self, templatename, store_id, data):
        """
        Creates a storeable with a 'root' default subdict using your data.
        If there's a 'callback' key in data, it'll be run every time the
        storeable is rendered.
        """
        self.m_template_lk = cp.Application.root.tlok
        self.templname = templatename
        self.data = dict()
        self.data['root'] = data
        self.id = store_id
        if 'callback' in self.data['root']:
            self.callback = self.data['root']['callback']

    def render(self):
        """
        Renders this storeable using its template and returns the result
        """
        template = self.m_template_lk.get_template(self.templname)
        return template.render(root=self.data['root'],
            data=self.data, id=self.id)
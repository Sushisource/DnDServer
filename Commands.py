from cherrypy import Application as cpa
import inspect
import re
from Roller import rollDice

def callable(func):
    func.is_callable = True
    return func

class CommandHandler:
    def __init__(self):
        self.callables = list()
        for f in inspect.getmembers(self):
            if hasattr(f[1], 'is_callable'):
                self.callables.append(f[1])

    def do_command(self, commandstr, dnd):
       """
       Breaks apart a command and does dispatch to its proper
       function

       @type dnd: DnDSocket
       @param dnd: The calling socket
       """
       m = re.match(r"/(\w+) (.+)", commandstr)
       if not m:
           dnd.serverchat("Invalid command, {0}!\
           </br>Syntax is like <i>/command parameter(s)</i>".format(dnd.uname))
           return
       cmd, param = m.group(1,2)

       ran = False
       for callable in self.callables:
           if cmd == callable.__name__:
               ran = True
               callable(dnd, param)
       if not ran:
           dnd.serverchat("No such command: {0}".format(cmd))

    @callable
    def d(self, dnd, dicestr):
        tlok = cpa.root.tlok
        result = rollDice(dicestr)
        result = tlok.get_template('diceresult.mako').render(query=dicestr,
            total=result)
        dnd.send_message("diceroll",
                {'result': result,
                 'name': dnd.uname})

import re

def do_command(commandstr, dnd):
   """
   Breaks apart a command and does dispatch to its proper
   function

   @type dnd: DnDSocket
   @param dnd: The calling socket
   """
   m = re.match(r"\/(\w+) (.+)", commandstr)
   if not m:
       dnd.serverchat("Invalid command, {0}!".format(dnd.uname))
   cmd, param = m.group(1,2)
   dnd.serverchat('Cmd: {0} prm: {1}'.format(cmd,param))

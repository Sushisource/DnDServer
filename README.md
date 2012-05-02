#DNDServer
A fun little server written in python using WebSockets with ws4py and cherrypy which serves up a shared dashboard that players can
use to keep track of ingame stats

###Security Note:
Do not, under any circumstance, expose this server to the internet. It will not scale, it is not secure. It was designed that way to make the code easy to develop and understand, and because no one is going to play D&D with hundreds of people.

##Running
You'll need [ws4py](https://github.com/Lawouach/WebSocket-for-Python) and [cherrypy](http://cherrypy.org/) as well as [mako](http://www.makotemplates.org/) [numpy](http://numpy.scipy.org/) is needed for the die roller.

Then just run main.py and you should be good to go! If your ip doesn't get properly detected you might need to manually modify client.js.

##Compatability
Python 2.7+
import cherrypy, ConfigParser, sys, logging
from setup import quotes, times, engine, feeds
from jinja2 import Environment, FileSystemLoader

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8080,
                       })

env = Environment(loader=FileSystemLoader('templates'))

config = ConfigParser.RawConfigParser()
config.read(sys.argv[1])

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
fh = logging.FileHandler('redditthread.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
fh.setFormatter(formatter)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

log.addHandler(sh)
log.addHandler(fh)

class quoteSearch(object):
    def index(self, search):
        q = quotes.select().order_by('id').where('body LIKE "%{0}%"'.format(search))
        rs = q.execute()
        rows = rs.fetchall()
        
        template = env.get_template("search.jinja2")
        return template.render(results=rows)
    index.exposed = True


if __name__ == "__main__":  
    cherrypy.quickstart(quoteSearch())
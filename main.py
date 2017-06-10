from init import *

hc = C('http')()
hc.start()

host = hc.conf['host'] if hc.conf['host'] else '127.0.0.1'
print('HTTPServer is running at %s:%s' % (host, hc.conf['port']))
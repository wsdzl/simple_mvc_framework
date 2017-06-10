class Controler(object):
	def __init__(self, method, url, cookie, data, headers):
		self.env = {}
		self.env['method'] = method
		self.env['url'] = url
		self.env['cookie'] = cookie
		self.env['data'] = data
		self.env['headers'] = headers
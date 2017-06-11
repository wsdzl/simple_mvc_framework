# Controler基类

class Controler(object):
	def __init__(self, method, url, cookie, data, headers):
		# 从HTTPServer.handle方法引入HTTP环境变量
		self.env = {}
		self.env['method'] = method
		self.env['url'] = url
		self.env['cookie'] = cookie
		self.env['data'] = data
		self.env['headers'] = headers
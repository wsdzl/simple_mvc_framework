# Controler基类

class Controler(object):
	res_code = 200 # HTTP响应码
	res_cookies = [] # HTTP响应头Set-cookie
	headers = None # HTTP响应头
	def __init__(self, method, url, cookie, data, headers):
		# 从HTTPServer.handle方法引入HTTP环境变量
		self.env = {}
		self.env['method'] = method
		self.env['url'] = url
		self.env['cookie'] = cookie
		self.env['data'] = data
		self.env['headers'] = headers

	# 添加Set-cookie头
	def set_cookie(self, key, value, expires=3600, path='/', domain=''):
		self.res_cookies.append([key, value, expires, path, domain])

	# 添加HTTP响应头
	def header(self, data):
		if self.headers == None:
			self.headers = [data]
		else:
			self.headers.append(data)

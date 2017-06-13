# 简单可扩展多线程HTTP服务器，实现了处理GET、POST请求，COOKIE管理等简单功能

import socket as S
from http.cookies import SimpleCookie as SC
from urllib.request import (quote as UE, unquote as UD)
from init import *

class HTTPServer(object):
	def __init__(self, conf):
		# 通过初始化配置启动socket服务器
		# 默认配置（/controler/httpControler.py）
		# default = {
		# 	'host': '',
		# 	'port': 80,
		# 	'bfsz': 1024,
		# 	'backlog': 10,
		# }
		self.conf = conf
		self.servSock = S.socket(S.AF_INET, S.SOCK_STREAM)
		addr = (conf['host'], conf['port'])
		self.servSock.bind(addr)
		t = threading.Thread(target=self._start)
		t.start()

	def _start(self):
		# 循环监听传入的连接
		self.servSock.listen(self.conf['backlog'])
		while True:
			if not self.isStart:
				continue
			cliSock, addr = self.servSock.accept()
			# 为每一个传入的连接打开一个线程操作
			t = threading.Thread(target=self._request, args=(cliSock,))
			t.start()

	def start(self): # 处理传入的连接
		self.isStart = True

	def stop(self): # 暂停处理传入的连接
		self.isStart = False

	def _request(self, s): # 处理客户端请求
		req = []
		while True:
			bf = s.recv(self.conf['bfsz'])
			if not bf:
				break
			req.append(bf)
			if bf.find(b'\r\n\r\n') != -1: # 截取http请求头
				break
		try:
			# 解析请求头
			req = b''.join(req)
			header, data = req.split(b'\r\n\r\n', 1)
			header = header.decode('utf-8')
			header = header.split('\r\n')
			method, url, version = header[0].strip().split(' ')
			del header[0]
			method = method.upper()
			if not method in ['GET', 'POST', 'HEAD']:
				return
			headers = {}
			for i in header:
				k, v = i.split(':', 1)
				headers[k.upper()] = v
		except:
			return
		# 完整接收POST数据
		if method == 'POST':
			try:
				contLength = int(headers['CONTENT-LENGTH'])
				if contLength > 0:
					while len(data) < contLength:
						bf = s.recv(self.conf['bfsz'])
						data += bf
			except:
				pass
		# 解析客户端cookie
		cookie = {}
		try:
			tmp = headers['COOKIE'].split(';')
			for i in tmp:
				i = i.strip()
				k, v = i.split('=', 1)
				cookie[UD(k)] = UD(v)
		except:
			pass
		# 将请求数据格式化传给handle方法取得响应数据
		s.send(self.handle(method, url, cookie, data, headers))
		s.close() # 关闭连接

	# 数据处理接口方法，子类可重写此方法以扩展功能
	def handle(self, method, url, cookie, data, headers):
		d = b'<html><head><title>\xe6\xb5\x8b\xe8\xaf\x95\xe6\xb5\x8b\xe8\xaf\x95</title></head><body>'
		d += b'<div>Method: %s</div>' % method.encode('utf-8')
		d += b'<div>Url: %s</div>' % url.encode('utf-8')
		d += b'<div>Cookie: %s</div>' % str(cookie).encode('utf-8')
		d += b'<div>Data: %s</div>' % data
		d += b'<div>Headers: %s</div>' % str(headers).encode('utf-8')
		d += b'</body></html>'
		return self.res_404(d)

	# 构造HTTP请求成功响应数据
	# cookies = [
	# 	[key1, value2, expires, path, domain],
	# 	[key2, value2, expires, path, domain],
	# 	...
	# ]
	def res_200(self, data, cookies=[], headers=None, status=b'HTTP/1.1 200 OK\r\n'):
		if headers == None:
			headers = ['Content-Type: text/html;charset=utf-8']
		cookies = self.set_cookie(cookies)
		if cookies:
			headers.append(cookies)
		d = status + '\r\n'.join(headers).encode('utf-8') + b'\r\n\r\n'
		if type(data) != bytes:
			data = data.encode('utf-8')
		d += data
		return d

	# 构造HTTP请求失败响应数据
	def res_404(self, data, cookies=[], headers=None):
		return self.res_200(data, cookies, headers, b'HTTP/1.1 404 Not Found\r\n')

	# 从cookie列表生成Set-cookie响应头数据
	def set_cookie(self, cookies):
		cookie = SC()
		for k, v, expires, path, domain in cookies:
			if not path:
				path = '/'
			k = UE(k)
			v = UE(v)
			cookie[k] = v
			cookie[k]['expires'] = expires
			cookie[k]['path'] = path
			cookie[k]['domain'] = domain
		return cookie.output()



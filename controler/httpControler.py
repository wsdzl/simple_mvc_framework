from init import *
import socket as S

HTTPServer = I('HTTPServer')

class httpControler(HTTPServer):
	default = {
		'host': '',
		'port': 80,
		'bfsz': 1024,
		'backlog': 10,
		'default_controler': 'index',
		'default_controler_method': 'index',
		'param_sep': '/',
		'param_sep_re': ''
	}
	_res_dir = os.path.join(ROOT, 'view')
	_static_res = ['.js', '.html']
	_static_dir = ['static']

	def __init__(self):
		self.conf = I('conf')('http.conf')
		self.default.update(self.conf.data)
		self.conf.data = self.default
		self.conf._save()
		super().__init__(self.conf.data)

	def handle(self, method, url, cookie, data, headers):
		f = self._readfile(url)
		if f != None:
			return self.res_200(f)
		ctlr, _method, args = self._split(url)
		try:
			ctlr = ctlr(method, url, cookie, data, headers)
			return getattr(ctlr, _method)(**args)
		except:
			return self.error_page()
		return self.error_page()

	def error_page(self):
		return self.res_404(I('showMsg')('404'))

	def _split(self, url):
		if self.conf['param_sep_re']:
			re = _im('re')
			params = re.split(self.conf['param_sep_re'], url)
		else:
			params = url.split(self.conf.get('param_sep', '/'))
		params = [i for i in params if i]
		if not params:
			params = [
				self.conf.get('default_controler', 'index'),
				self.conf.get('default_controler_method', 'index')
			]
		try:
			if params[0] == 'http':
				raise ImportError
			ctlr = C(params[0])
			del params[0]
		except:
			ctlr = C(self.conf.get('default_controler', 'index'))
		try:
			method = getattr(ctlr, params[0])
			method = params[0]
			del params[0]
		except:
			method = self.conf.get('default_controler_method', 'index')
		args = {}
		if len(params)%2 == 1:
			params.pop()
		for i in range(len(params)):
			if i%2 == 0:
				args[params[i]] = None
			else:
				args[params[i-1]] = params[i]
		return (ctlr, method, args)

	def _readfile(self, filename):
		filename = os.path.realpath(os.path.join(self._res_dir, '.' + filename))
		_dir = os.path.dirname(filename)
		if not filename.startswith(self._res_dir):
			return
		tmp = filename[len(self._res_dir) + 1:]
		inRange = False
		for i in self._static_dir:
			if tmp.startswith(i + os.path.sep):
				inRange = True
		if not inRange:
			ext = os.path.splitext(filename)[1]
			if not ext in self._static_res:
				return
		try:
			with open(filename, 'rb') as f:
				return f.read()
		except:
			return
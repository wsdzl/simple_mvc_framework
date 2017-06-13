# HTTP控制器，控制URL->Controler->view间路由操作

from init import *
import socket as S
from re import split as re_split

HTTPServer = I('HTTPServer') # 引入HTTPServer类作为基类（/lib/HTTPServer.py）

class httpControler(HTTPServer):
	# HTTPServer默认配置
	default = {
		'host': '', # IP
		'port': 80, # 端口
		'bfsz': 1024, # socket buffer size
		'backlog': 10, # socket backlog
		'default_controler': 'index', # 默认控制器
		'default_controler_method': 'index', # 默认控制器方法
		'param_sep': '/', # URL路由分割符
		'param_sep_re': '' # 正则URL路由分割符，此项若非空则'param_sep'项失效
	}
	_res_dir = os.path.join(ROOT, 'view') # 资源文件夹
	_static_res = ['.js', '.html'] # 允许的静态资源后缀（均按静态资源发送给浏览器）
	_res_mime = {
		'.bmp': 'image/bmp',
		'.git': 'image/gif',
		'.ico': 'image/x-icon',
		'.jpeg': 'image/jpeg',
		'.jpg': 'image/jpeg',
		'.jpe': 'image/jpeg',
		'.txt': 'text/plain',
		'.css': 'text/css',
		'.js': 'text/javascript',
		'.html': 'text/html',
		'.htm': 'text/html'
	}
	_static_dir = ['static'] # 静态资源文件夹（文件夹下所有文件按静态资源发送给浏览器）

	def __init__(self):
		self.conf = I('conf')('http.conf') # 初始化关联配置文件
		self.default.update(self.conf.data) # 合并默认配置
		self.conf.data = self.default # 保存合并配置
		self.conf._save()
		super().__init__(self.conf.data) # 初始化HTTP服务器

	# 重写基类handle方法
	def handle(self, method, url, cookie, data, headers):
		# 尝试在资源文件夹下读文件
		f = self._readfile(url)
		if f != None:
			headers = []
			if f[1] in self._res_mime:
				headers = ['Content-Type: %s' % self._res_mime[f[1]]]
			return self.res_200(f[0], headers=headers)
		# 文件若不存在则从URL映射到控制器方法
		ctlr, _method, args = self._split(url)
		try:
			# 将HTTP环境变量传入控制器
			ctlr = ctlr(method, url, cookie, data, headers)
			result = getattr(ctlr, _method)(**args)
			status = {
				200: b'HTTP/1.1 200 OK\r\n',
				404: b'HTTP/1.1 404 Not Found\r\n'
			}[ctlr.res_code]
			# 执行控制器方法返回结果
			return self.res_200(result, ctlr.res_cookies, ctlr.headers, status)
		except Exception as e: # 浏览器发送参数错误
			if I('conf')('debug.conf').get('open', True): # 调试
				traceback = __import__('traceback') 
				return self.res_404(traceback.format_exc().replace('\n','<br />').encode('utf-8'))
			return self.error_page() # 响应错误页面
		# 请求的控制器方法不存在
		return self.error_page() # 响应错误页面

	# 服务器错误页面，可自定义，返回bytes格式html页面
	def error_page(self):
		return self.res_404(I('showMsg')('404'))

	# 分割URL映射到控制器方法
	# 返回格式：
	# 	tuple(控制器, 方法名, 方法参数{parm1: value1, parm2: value2,...})
	def _split(self, url):
		# 从配置读入URL分割方法
		if self.conf['param_sep_re']:
			params = re_split(self.conf['param_sep_re'], url)
		else:
			params = url.split(self.conf.get('param_sep', '/'))
		params = [i for i in params if i]
		# URL若为空，映射到默认控制器默认方法
		if not params:
			params = [
				self.conf.get('default_controler', 'index'),
				self.conf.get('default_controler_method', 'index')
			]
		# 映射控制器
		try:
			if params[0] == 'http': # 排除httpControler
				raise ImportError
			ctlr = C(params[0])
			del params[0]
		except:
			ctlr = C(self.conf.get('default_controler', 'index'))
		# 映射控制器方法
		try:
			method = getattr(ctlr, params[0])
			method = params[0]
			del params[0]
		except:
			method = self.conf.get('default_controler_method', 'index')
		# 解析传给控制器方法的URL参数
		args = {}
		for i in range(len(params)):
			if i%2 == 0:
				args[params[i]] = None
			else:
				args[params[i-1]] = params[i]
		return (ctlr, method, args)

	# 从资源文件夹读入文件
	def _readfile(self, filename):
		filename = os.path.realpath(os.path.join(self._res_dir, '.' + filename)) # 拼接文件绝对路径
		# 禁止跨目录
		_dir = os.path.dirname(filename)
		if not filename.startswith(self._res_dir):
			return
		# 检查是否位于静态文件夹
		tmp = filename[len(self._res_dir) + 1:]
		inRange = False
		for i in self._static_dir:
			if tmp.startswith(i + os.path.sep):
				inRange = True
		ext = os.path.splitext(filename)[1]
		if not inRange:
			# 检查扩展名是否允许
			if not ext in self._static_res:
				return
		try:
			# 以bytes格式读入文件并返回
			with open(filename, 'rb') as f:
				return (f.read(),ext)
		except:
			return

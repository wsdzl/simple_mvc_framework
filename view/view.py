from init import *
from io import BytesIO
import re

class view(object):
	L_DELIM = b'{{' # 模板表达式左分隔符
	R_DELIM = b'}}' # 模板表达式右分隔符

	# tpl，模板名，格式：'文件夹.[文件夹...].模板名（不带后缀）'
	# ctlr，控制器
	def __init__(self, tpl, ctlr, args={}):
		self.data = BytesIO()
		tpl = tpl.replace('.', os.path.sep) + '.tpl'
		self._file = os.path.join(ROOT, 'view', tpl)
		self.args = args
		self.ctlr = ctlr
		self._re = {
			'var': re.compile(r'^(?:\w+\.)*\w+$'),
			'if': re.compile(r'^\s*if +((?:\w+\.)*\w+):\s*([\S\s]+?)(?:\s+else:\s*([\S\s]+)\s*)?$'),
			'replace_var': re.compile(r'\$\(((?:\w+\.)*\w+)\)')
		}

	# 编译模板
	def compile(self, args=None):
		if args != None:
			self.args = args
		if self.args == None:
			return
		try:
			with open(self._file, 'rb') as f:
				on = 'l'
				lbf = []
				mbf = []
				rbf = []
				l_delim_len = len(self.L_DELIM)
				r_delim_len = len(self.R_DELIM)
				while True:
					b = f.read(1)
					if b == b'':
						break
					if on == 'l':
						self.data.write(b)
						lbf.append(b)
						if len(lbf) > l_delim_len:
							del lbf[0]
						if b''.join(lbf) == self.L_DELIM:
							on = 'm'
							lbf = []
							self.data.seek(self.data.tell()-l_delim_len)
					elif on == 'm':
						mbf.append(b)
						rbf.append(b)
						if len(rbf) > r_delim_len:
							del rbf[0]
						if b''.join(rbf) == self.R_DELIM:
							mbf = mbf[:-2]
							self.data.write(self.exp2bytes(b''.join(mbf).decode('utf-8')))
							rbf = []
							mbf = []
							on = 'l'
		except Exception as e:
			if I('conf')('debug.conf').get('open', True):
				raise e
			return
		return self.data.getvalue()

	__call__ = compile

	# 解析表达式
	def exp2bytes(self, exp):
		if self._re['var'].match(exp):
			return self._parse_var(exp)
		else:
			m = self._re['if'].match(exp)
			if m:
				return self._parse_if(m)
			else:
				return exp.encode('utf-8')

	# 解析变量表达式
	def _parse_var(self, exp):
		exp = exp.split('.')
		exp = [i for i in exp if exp]
		result = None
		if exp[0] == 'ENV': # 解析环境变量
			result = self.ctlr.env
			del exp[0]
		else: # 解析用户数据
			result = self.args
		try:
			if not len(exp):
				return b'NULL'
			while len(exp):
				result = result[exp[0]]
				del exp[0]
		except Exception as e:
			#raise e
			return b'NULL'
		return str(result).encode('utf-8')

	# 解析if语句表达式
	def _parse_if(self, match):
		match = match.groups()
		if self._parse_var(match[0]) != b'NULL':
			result = match[1]
		else:
			result = match[2]
		if result:
			result = self._replace_var(result)
		return result.encode('utf-8')

	# 解析文本中变量
	def _replace_var(self, text):
		varsli = set(self._re['replace_var'].findall(text))
		for i in varsli:
			text = text.replace('$(%s)'%i, self._parse_var(i).decode('utf-8'))
		return text
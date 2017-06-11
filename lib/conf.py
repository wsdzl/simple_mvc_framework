# 配置文件类

from init import *

class conf(object):

	# 调试方法
	__repr__ = lambda self:self.data.__repr__()
	__str__ = __repr__
	
	# 初始化关联配置文件
	def __init__(self, _file='main.conf'):
		self._filename = os.path.join(ROOT, 'conf', _file)
		self._load()

	# 从文件读入数据
	def _load(self):
		with open(self._filename, 'a+') as f:
			f.seek(0)
			text = f.read()
			if text:
				self.data = json.loads(text)
			else:
				self.data = {}
				f.write('{}')

	# 保存数据到文件
	def _save(self):
		with open(self._filename, 'w') as f:
			json.dump(self.data, f)

	# 取配置项，失败返回None
	def __getitem__(self, key):
		try:
			return self.data[key]
		except KeyError:
			return None

	# 取配置项，可指定默认数据
	def get(self, key, default=None):
		v = self[key]
		if v:
			return v
		return default

	# 写配置项
	def __setitem__(self, key, value):
		self.data[key] = value
		self._save()

	# 删除配置项
	def __delitem__(self, key):
		try:
			del self.data[key]
			self._save()
			return True
		except KeyError:
			return False
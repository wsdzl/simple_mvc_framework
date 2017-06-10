from init import *

class conf(object):

	__repr__ = lambda self:self.data.__repr__()
	__str__ = __repr__
	
	def __init__(self, _file='main.conf'):
		self._filename = os.path.join(ROOT, 'conf', _file)
		self._load()

	def _load(self):
		with open(self._filename, 'a+') as f:
			f.seek(0)
			text = f.read()
			if text:
				self.data = json.loads(text)
			else:
				self.data = {}
				f.write('{}')

	def _save(self):
		with open(self._filename, 'w') as f:
			json.dump(self.data, f)

	def __getitem__(self, key):
		try:
			return self.data[key]
		except KeyError:
			return None

	def get(self, key, default=None):
		v = self[key]
		if v:
			return v
		return default

	def __setitem__(self, key, value):
		self.data[key] = value
		self._save()

	def __delitem__(self, key):
		try:
			del self.data[key]
			self._save()
			return True
		except KeyError:
			return False
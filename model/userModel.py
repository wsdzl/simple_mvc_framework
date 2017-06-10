from init import *
from time import time
import hashlib

conf = I('conf')
randstr = I('randstr')
uconf = conf('uconf.conf')

if not uconf['salt']:
	uconf['salt'] = randstr()

if not uconf['session_time']:
	uconf['session_time'] = 3600

class userModel(conf):

	_salt = uconf['salt']
	session_time = uconf['session_time']
	sessions = conf('_sessions.conf')

	def __init__(self):
		super().__init__('userList.conf')
		self.get = super().__getitem__
		self.remove = super().__delitem__

	def add(self, user, pwd):
		pwd = self._hash(pwd)
		self[user] = pwd

	def login(self, user, pwd):
		p = self[user]
		pwd = self._hash(pwd)
		if p == pwd:
			return self.create_session(user)
		return False

	def create_session(self, user):
		k = randstr()
		v = (user, int(time()))
		self.sessions[k] = v
		return k

	def read_session(self, sid):
		session = self.sessions[sid]
		if not session:
			return False
		t = int(time()) - session[1]
		if t > self.session_time:
			del self.sessions[sid]
			return False
		return session

	def _hash(self, pwd):
		pwd += self._salt
		sha1 = hashlib.sha1()
		sha1.update(pwd.encode('utf-8'))
		return sha1.hexdigest()
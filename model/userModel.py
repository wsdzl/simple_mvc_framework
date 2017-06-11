# 简单用户Model，使用json储存，带session控制，适用于少用户量程序（博客、聊天室、……）

from init import *
from time import time
import hashlib

# 读入用户配置
conf = I('conf')
randstr = I('randstr')
uconf = conf('uconf.conf')

if not uconf['salt']:
	uconf['salt'] = randstr()

if not uconf['session_time']:
	uconf['session_time'] = 3600

# 使用配置文件类作为基类（/lib/conf.py）
class userModel(conf):
	_salt = uconf['salt']
	session_time = uconf['session_time']
	sessions = conf('_sessions.conf')

	def __init__(self):
		super().__init__('userList.conf') # 用户列表关联配置文件
		self.get = super().__getitem__ # 读用户密码hash
		self.remove = super().__delitem__ # 删除用户

	def add(self, user, pwd): # 新增用户
		pwd = self._hash(pwd)
		self[user] = pwd

	def login(self, user, pwd): # 用户登陆，成功返回sessionid
		p = self[user]
		pwd = self._hash(pwd)
		if p == pwd:
			return self.create_session(user)
		return False

	def create_session(self, user): # 创建session
		k = randstr()
		v = (user, int(time()))
		self.sessions[k] = v
		return k

	# 读session，成功返回用户数据，tuple(username, logintime)
	def read_session(self, sid):
		session = self.sessions[sid]
		if not session:
			return False
		t = int(time()) - session[1]
		if t > self.session_time:
			del self.sessions[sid]
			return False
		return session

	def _hash(self, pwd): # 密码生成hash，sha1(pwd+salt)
		pwd += self._salt
		sha1 = hashlib.sha1()
		sha1.update(pwd.encode('utf-8'))
		return sha1.hexdigest()
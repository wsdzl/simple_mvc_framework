# 默认控制器
from init import *

msg = I('showMsg')
class indexControler(Controler):
	def index(self, name='guest'):
		li = [('link%d'%i, '链接%d'%i) for i in range(1, 11)]
		v = view('index', self)
		return v({'name': name, 'li': li})

	def test(self):
		return b'Test Method!%s'
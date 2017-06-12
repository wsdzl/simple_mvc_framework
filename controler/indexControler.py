# 默认控制器
from init import *

msg = I('showMsg')
class indexControler(Controler):
	def index(self, name='guest'):
		v = V('view')('index', self)
		return v({'name': name})

	def test(self):
		return b'Test Method!%s'
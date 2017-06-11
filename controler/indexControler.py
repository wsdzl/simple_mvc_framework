# 默认控制器
from init import *

msg = I('showMsg')
class indexControler(Controler):
	def index(self):
		v = V('view')('index', self)
		return v(1)

	def test(self):
		return b'Test Method!%s'
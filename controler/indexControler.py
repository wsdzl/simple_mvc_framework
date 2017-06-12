# 默认控制器
from init import *

msg = I('showMsg')
class indexControler(Controler):
	def index(self):
		v = V('view')('index', self)
		return v({'nihao': 123})

	def test(self):
		return b'Test Method!%s'
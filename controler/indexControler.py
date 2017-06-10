from init import *

msg = I('showMsg')
class indexControler(Controler):
	def index(self):
		return msg(str(self.env))
		return b'It works!'

	def test(self):
		return b'Test Method!'
import os
import sys
import json
import multiprocessing
import threading
from importlib import import_module as _im

ROOT = os.path.abspath('.')

def M(name, _dir='model', _ext='Model'):
	try:
		module = _im('%s.%s%s' % (_dir, name, _ext))
		return getattr(module, name + _ext)
	except ImportError:
		raise NameError("%s%s doesn't exist" % (name, _ext))

V = lambda name:M(name, 'view', '')

C = lambda name:M(name, 'controler', 'Controler')

I = lambda name:M(name, 'lib', '')

Controler = I('Controler')
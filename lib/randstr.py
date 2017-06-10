import random

def randstr(length=20, _range=None):
	if not _range:
		_range = '!#$%&*+-.0123456789?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz'
	rand = []
	while len(rand) < length:
		rand.append(random.choice(_range))
	return ''.join(rand)

if __name__ == '__main__':
	print(randstr())
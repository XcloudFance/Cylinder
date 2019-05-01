from threading import Thread
tmp = 1
def run1():
	global tmp
	tmp+=1
def run2():
	print(tmp)
Thread(target=run2).start()
Thread(target=run1).start()

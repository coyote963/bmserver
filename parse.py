import psycopg2
import bmbuffer
import BMStream
def parse(funclist,socket,**kwargs):
	try:
		bms = kwargs['bms']
		while (True):
			bms.read()
			while not bms.isEmpty():
				bmdict = bms.pop()
				for bmfunc in funclist:
					bmfunc(bmdict,socket,**kwargs)
	except KeyboardInterrupt:
		print "exiting"

		kwargs.get('dbcursor').close()


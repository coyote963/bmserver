import time
import threading

def scoreboardService(socket):
	e = threading.currentThread()
	while getattr(e, "do_run", True):
		time.sleep(10)
		socket.send('/info\n')
		socket.send('/scoreboard\n')
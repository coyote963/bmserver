#!/usr/bin/env python
import sys
import networkhelper
from parse import parse
import psycopg2
import BMStream
from datetime import datetime
from collections import deque
import re
import threading
from matchupdb import matchupdb
from teamsdb import teamsdb, clearTeam, Team,infoIncrement
import config
import scoreboardService
if __name__ == "__main__":
	if len(sys.argv) == 1:
		config.initiate()
	else:
		config.instantinitiate(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
	socket = networkhelper.gameconnect(config.ipaddress, config.port, config.password)
	conn = networkhelper.dbconnect(config.database)
	bmstream = BMStream.BMStream(socket)
	isBalanced= True

	e = threading.Thread(target = scoreboardService.scoreboardService, args = [socket])
	e.start()

	parse([matchupdb,teamsdb, clearTeam,infoIncrement],socket, dbcursor = conn, bms = bmstream, is_balanced = isBalanced, teamlist = Team())

	e.do_run = False
	e.join()
	socket.close()

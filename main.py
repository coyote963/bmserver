#!/usr/bin/env python
import sys
import networkhelper
from parse import parse
import psycopg2
import BMStream
from datetime import datetime
from collections import deque
import re
from request_leaderboard import request_leaderboard
from request_rating import request_rating
from matchupdb import matchupdb, is_running,coyote
from balance import is_balanced, request_balance
from translate import trans
import config

if __name__ == "__main__":
	if len(sys.argv) == 1:
		config.initiate()
	else:
		config.instantinitiate(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
	print config.playertable
	print config.matchuptable
	socket = networkhelper.gameconnect(config.ipaddress, config.port, "5fnu3XVK")
	conn = networkhelper.dbconnect("host='ec2-54-243-52-211.compute-1.amazonaws.com' dbname='d4inae708paere' user='sdsduckhtwkkzl' password='s2YO_0haa9M-0PHuiT3q0D3a7w'")
	bmstream = BMStream.BMStream(socket)
	isBalanced= True
	parse([matchupdb,],socket, dbcursor = conn, bms = bmstream, is_balanced = isBalanced)
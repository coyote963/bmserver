import main
if __name__ == "__run__":
	print "hello"
	socket = networkhelper.gameconnect('104.230.114.72', 7795, "foobar")
	conn = networkhelper.dbconnect("host='ec2-50-17-212-238.compute-1.amazonaws.com' dbname='d4iqpn1cgf40o0' user='kempajfufvpvkk' password='xg8y1RVgUfLdnqeBmzsbi6aPc6'")
	bmstream = BMStream.BMStream(socket)
	isBalanced= True
	parse([request_rating,matchupdb,is_balanced,is_running,request_balance,request_leaderboard],socket, dbcursor = conn, bms = bmstream, is_balanced = isBalanced)
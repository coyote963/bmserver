from networkhelper import gameconnect

socket = gameconnect('104.230.114.72', 7786, "foobar")
socket.send(bytes('hullo!'))

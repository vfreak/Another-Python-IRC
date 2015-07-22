import os, threading, socket as sk

address = 'irc.freenode.net'
port = 6667
nick = 'Nick'
name = 'Bob'
pwd = 'none'
channel = ''

option = 0

sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

def banner():
	os.system('cls')
	print ('#' * 120) * 5
	print '#' * 55 + '  Py IRC  ' + '#' * 55
	print ('#' * 120) * 5
	
	print 'Type any number to change an option.'
	print '(1) NICK: ' + nick
	print '(2) NAME: ' + name
	print '(3) PASS: ' + pwd
	print '(4) ADDRESS: ' + address
	print '(5) PORT: ' + str(port)
	print '(6) CONNECT: '
	print '(7) QUIT: '
	return int(raw_input())
	
def connect():
	sock.connect((address, port))
	sock.send("PASS %s\n\r" % pwd)
	sock.send("USER %(name)s %(name)s %(name)s :%(name)s\n\r" % {'name':name})
	sock.send("NICK %s\n\r" % nick)
	r = threading.Thread(target=recvmsg)
	s = threading.Thread(target=sendmsg)
	r.start()
	s.start()

def disconnect():
	sock.close()

def sendmsg():
	while True:
		msg = raw_input()
		if(msg[:1] != '/'):
			sock.send('PRIVMSG ' + channel + ' :' + msg + '\r\n')
		elif msg[:5] == '/join':
			channel = msg[6:]
			sock.send(msg[1:] + '\r\n')
		else:
			sock.send(msg[1:] + '\r\n')
		
	
def recvmsg():
	while True:
		buff = sock.recv(4096)
		lines = buff.split('\n')
		for line in lines:
			if(line[:4] == 'PING'):
				sock.send('PONG' + line[4:])
				print 'PONG' + line[4:]
			print line
	
def init():
	global option
	global address
	global port
	global nick
	global name
	
	while option != 7 or option != 6:
		option = banner()
		if option == 1:
			nick = raw_input('Enter your desired NICK: ')
		elif option == 2:
			name = raw_input('Enter your desired NAME: ')
		elif option == 3:
			pwd = raw_input('Enter the PASSword you want to connect with: ')
		elif option == 4:
			address = raw_input('Enter the IRC network ADDRESS you wish to connect to: ')
		elif option == 5:
			port = raw_input('Enter enter the PORT you want to connect on: ')
		elif option == 6:
			connect()
			return
		else:
			disconnect()

os.system('mode 120, 50')			
init()

import optparse
import os
import socket
import time
from threading import Thread
from io import StringIO

txt = '''1111
2222
3333
4444
'''

# 服务端程序处理过程
def server(listen_socket):
	while True:
		buf = StringIO(txt)
		sock, addr = listen_socket.accept()
		print('Somebody at %s wants poetry!' %(addr,))
		while True:
			try:
				line = buf.readline().strip()
				if not line:
					sock.close()
					break
				sock.sendall(line.encode('utf8')) # this is a blocking call
				print('send bytes to client: %s' %line)
			except socket.error:
				sock.close()
				break
			time.sleep(0.5) # server每发送一个单词后等待一会
		sock.close()
		print('\n')

# 同时开启三个服务端线程，分别在三个端口监听
# 服务端程序为阻塞方式，只能一次服务于一个客户端
def main():
	ports = [10010, 10011, 10012]
	for port in ports:
		listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		addres = ('127.0.0.1', port)
		listen_socket.bind(addres)
		listen_socket.listen(5)
		print("start listen at: %d" %port)
		worker = Thread(target = server, args = [listen_socket])
		worker.setDaemon(True)
		worker.start()

if __name__ == '__main__':
	main()
	while True:
		time.sleep(0.1) # 如果不sleep的话, CPU会被Python完全占用了


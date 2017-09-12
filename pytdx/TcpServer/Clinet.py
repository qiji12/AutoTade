from socket import *

# 建立三个客户端，分别连接三个不同的服务端程序, 接收服务端传过来的数据并打印
# 这三个客户端是阻塞方式通信的
if __name__ == '__main__':
	ports =  [10010, 10011, 10012]
	for port in ports:
		address = ('127.0.0.1', port)
		sock = socket(AF_INET, SOCK_STREAM)
		sock.connect(address)
		poem = ''
		while True:
			data = sock.recv(4)
			if not data:
				sock.close()
				break
			poem += data.decode('utf8')
		print(poem)
		sock.close()

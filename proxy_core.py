import select
import socket
import threading
import time
from _thread import *
from statistic import Addres_statistics
from filter import Filter

buffer_size = 8192
connection_size = 200
wait_times_requests_on_server = 30 #в секундах
time_out_max = 30


class Server:

	def __init__ (self,host,port):
		self.servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.servSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.servSock.bind((host, port))
		self.servSock.listen(connection_size)
		self.servSock.settimeout(wait_times_requests_on_server)


	def sever_loop (self):
		print("********** Proxy Server Start **********")
		while True:
			try:
				conn, addr = self.servSock.accept()
			except socket.timeout as e :
				None
			except Exception as exception:
				print(exception)
			else:
				start_new_thread(proxy,(conn, addr))




class Client:

	def __init__(self,host,port):
		self.clieSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clieSock.connect((host, port))




def parser(data):
	headers , body = data.split(b"\r\n\r\n") #!!!
	params = headers.decode().split("\r\n")
	output = {}
	output["Body_Len"] = len(body)
	output["Type"],_,_=params[0].split(" ")
	for i in params[1:]:
		key, value =  i.split(": ")
		output[key] = value
	try:
		host , port = output["Host"].split(":")
		output["Host"] = host
		output["Port"] = port
	except ValueError :
		if 'https' in params[0]:
			output["Port"] = 443
		else:
			output["Port"] = 80
	return output


def proxy (serv_conn,clien_addr):
	temp = serv_conn.recv(buffer_size)
	headers = parser(temp)
	Addres_statistics.address_list_temp.append(headers["Host"])
	connect = False
	if Filter.filter(headers["Host"],headers["Port"]):
		if headers["Type"] == 'CONNECT' :
			clien = Client(headers["Host"], int(headers["Port"]))
			clien_conn = clien.clieSock
			serv_conn.send(b'HTTP / 1.1 200 Connection established\nProxy-Agent: THE BB Proxy\n\n')
		else:
			clien = Client(headers["Host"], int(headers["Port"]))
			clien_conn = clien.clieSock
			clien_conn.send(temp)
		connect = True
	else:
		serv_conn.send(b'HTTP/1.1 403 Forbidden')


	time_wait = 0
	while connect:
		recv, _, error = select.select([serv_conn, clien_conn], [], [serv_conn, clien_conn], 3)
		if error:
			print(error)
			break
		if recv:
			for in_ in recv:
				data = in_.recv(buffer_size)
				if in_ is clien_conn:
					out = serv_conn
				else:
					out = clien_conn
				if len(data)>0:
					out.send(data)
					time_wait = 0
				else:
					time.sleep(1)
					time_wait += 1
		else:
			time.sleep(1)
			time_wait +=1
		if time_out_max ==time_wait:
			break
	print("Разрываю соединение ")
	if connect :
		clien_conn.close()
	serv_conn.close()




if __name__ == '__main__':
	server = Server('',9090)
	stat = Addres_statistics
	stat.init()
	threading.Thread(target=stat.addres_statistic_loop, args=(), daemon=True).start()
	Filter.init()
	server.sever_loop()
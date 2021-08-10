import select
import socket
import threading
import time
from _thread import *
import setting
from statistic import Addres_statistics
from filter import Filter

SERVER_PORT = int(setting.get_param("SERVER_PORT"))
BUFFER_SIZE = int(setting.get_param("BUFFER_SIZE"))
CONNECTIONS = int(setting.get_param("CONNECTIONS"))
SERVER_WAIT = int(setting.get_param("SERVER_WAIT"))
TIMEOUT_MAX = int(setting.get_param("TIMEOUT_MAX"))


class Server:

	def __init__ (self,host,port):
		self.servSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.servSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.servSock.bind((host, port))
		self.servSock.listen(CONNECTIONS)
		self.servSock.settimeout(SERVER_WAIT)


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
	try:
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
	except Exception:
		return False

def proxy (serv_conn,clien_addr):
	temp = serv_conn.recv(BUFFER_SIZE)
	headers = parser(temp)
	connect = False
	if headers and Filter.filter(headers["Host"],headers["Port"],clien_addr) :
		Addres_statistics.address_list_temp.append(headers["Host"])
		try:
			if headers["Type"] == 'CONNECT' :
				clien = Client(headers["Host"], int(headers["Port"]))
				clien_conn = clien.clieSock
				serv_conn.send(b'HTTP / 1.1 200 Connection established\nProxy-Agent: THE BB Proxy\n\n')
			else:
				clien = Client(headers["Host"], int(headers["Port"]))
				clien_conn = clien.clieSock
				clien_conn.send(temp)
			connect = True
		except TimeoutError : None
		except Exception as e :
			print("Не предвиденная ошибка ",headers["Host"],headers["Port"],clien_addr,e)
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
				try:
					data = in_.recv(BUFFER_SIZE)
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
						if TIMEOUT_MAX == time_wait:
							break
				except ConnectionAbortedError :
					break
				except ConnectionResetError:
					break
		else:
			time.sleep(1)
			time_wait +=1
		if TIMEOUT_MAX ==time_wait:
			break
	if connect :
		clien_conn.close()
	serv_conn.close()




if __name__ == '__main__':
	server = Server('',SERVER_PORT)
	stat = Addres_statistics
	stat.init()
	threading.Thread(target=stat.addres_statistic_loop, args=(), daemon=True).start()
	Filter.init()
	threading.Thread(target=Filter.update_blacklist_loop, args=(), daemon=True).start()
	server.sever_loop()
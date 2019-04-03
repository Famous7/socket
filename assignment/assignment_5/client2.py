import socket, select
import sys

host = "127.0.0.1"
port = int(sys.argv[1])
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, port))

buf = input(">>>")
socket.sendall(buf.encode())
data = socket.recv(1024)
print("Received Data({A}) : {D}\n".format(A=socket.getpeername(), D=data.decode()))


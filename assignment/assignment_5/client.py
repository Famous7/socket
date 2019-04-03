import socket, select
import sys
import time

host = "127.0.0.1"
port = int(sys.argv[1])

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, port))
socket.setblocking(0)
socs = [socket]

while True:
    insds, outsds, errsds = select.select(socs, socs, [])
    if len(insds) != 0:
        buf = socket.recv(1024)
        if len(buf) != 0:
            print("Receive data : {D}\n".format(D=buf.decode()))
            
    if len(outsds) != 0:
        buf = input(">>>")
        socket.sendall(buf.encode())
    time.sleep(0.1)

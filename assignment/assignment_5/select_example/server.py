import socket, select
import sys

host = ''
port = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
inputs = [server]

while True:
    insds, outsds, errsds = select.select(inputs, inputs, [])   # select를 통해 서버 소켓의 R/W를 감시
    for sds in insds:   # 소켓 목록 중 읽기가 가능한 소켓이 있다면
        if sds is server:   # 서버 소켓이 읽기가 가능한 경우 -> 새로운 클라이언트 접속 요청
            clientsock, clienaddr = sds.accept()
            inputs.append(clientsock)   # 감시할 소켓 목록에 클라이언트 소켓을 추가
        else:   # 클라이언트 소켓이 읽기가 가능한 경우 -> 새로운 데이터가 온 경우
            buf = sds.recv(1024)
            if len(buf) == 0:
                inputs.remove(sds)
            else:
                print("Receive data({A}) : {D}\n".format(A=sds.getpeername(), D=buf.decode()))
                sds.sendall(buf[::-1])  # 받은 문자열을 뒤집어서 전송


import socket 
import sys
import threading 
import argparse
  
def socket_handler(conn):

    # 여기에 클라이언트 소켓에서 데이터를 받고, 보내는 코드 작성 
    # ex) conn.recv(1024)
    data = conn.recv(1024)
    data = data.decode()[::-1]
    conn.sendall(data.encode())
    conn.close()
  
  
if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description="Thread server -p port")
    parser.add_argument('-p', help = "port_number", required = True)

    args = parser.parse_args()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', int(args.p)))
    server.listen(5)

    while True:
        # 여기에 socket.accept 후 리턴받은 클라이언트 소켓으로 스레드를 생성하는 코드 작성
        conn, addr = server.accept()
        print('Connected to :', addr[0], ':', addr[1]) 

        t = threading.Thread(target=socket_handler, args=(conn,))
        t.start()

    server.close()

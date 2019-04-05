import socket
import threading
import argparse

is_alive = {}

def recv_msg(conn):
    peer = conn.getpeername()
    data = ""
    
    while data.upper() != "QUIT" or not is_alive[conn.getpeername()]:
        data = conn.recv(1024).decode()
        if len(data) != 0:
            print("From {0}:{1}, {2}".format(peer[0], peer[1], data))

    is_alive[conn.getpeername()] = False

def socket_handler(conn):
    is_alive[conn.getpeername()] = True
    recv_thread = threading.Thread(target=recv_msg, args=(conn,), daemon=True)
    recv_thread.start()

    msg = ""
    while msg.upper() != "QUIT":
        msg = input()

        if not is_alive[conn.getpeername()]:
            break

        conn.sendall(msg.encode())
    
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Thread server -p port")
    parser.add_argument('-p', help = "port_number", required = True)

    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', int(args.p)))
    server.listen(5)

    while True:
        conn, addr = server.accept()
        print('Connected to :', addr[0], ':', addr[1])

        t = threading.Thread(target=socket_handler, args=(conn,))
        t.start()

    server.close()


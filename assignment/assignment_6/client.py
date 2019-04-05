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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Thread cliet -i host -p port")
    parser.add_argument('-p', help = "port number", required = True)
    parser.add_argument('-i', help = "host address", required = True)

    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((args.i, int(args.p)))

    is_alive[server.getpeername()] = True
    recv_thread = threading.Thread(target=recv_msg, args=(server,), daemon=True)
    recv_thread.start()

    msg = ""
    while msg.upper() != "QUIT":
        msg = input()

        if not is_alive[server.getpeername()]:
            break

        server.sendall(msg.encode())

    server.close()


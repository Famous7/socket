import socket
import threading
import argparse

is_alive = True

def recv_msg(conn):
    peer = conn.getpeername()
    data = ""

    global is_alive
    while data.upper() != "QUIT" and is_alive:
        data = conn.recv(1024).decode()
        if not data:
            print("Conncetion closed")
            break

        print("From {0}:{1}, {2}".format(peer[0], peer[1], data))

    is_alive = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Thread cliet -i host -p port")
    parser.add_argument('-p', help = "port number", required = True)
    parser.add_argument('-i', help = "host address", required = True)

    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((args.i, int(args.p)))

    recv_thread = threading.Thread(target=recv_msg, args=(server,), daemon=True)
    recv_thread.start()

    msg = ""
    while msg.upper() != "QUIT" and is_alive:
        msg = input()

        if not is_alive:
            break

        server.sendall(msg.encode())

    is_alive = False

    server.close()


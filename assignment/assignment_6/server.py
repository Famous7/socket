import socket, errno, time, threading
import argparse

is_alive = None

def recv_msg(conn):
    peer = conn.getpeername()
    data = ""

    global is_alive
    while data.upper() != "QUIT" and is_alive:
        data = conn.recv(1024)

        if not data:
            print("Connection closed")
            break

        print("From {0}:{1}, {2}".format(peer[0], peer[1], data.decode()))

    is_alive = False

def socket_handler(conn):
    recv_thread = threading.Thread(target=recv_msg, args=(conn,), daemon=True)
    recv_thread.start()

    msg = ""

    global is_alive
    while msg.upper() != "QUIT":
        msg = input()

        if not is_alive:
            break

        conn.sendall(msg.encode())

    is_alive = False

    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Thread server -p port")
    parser.add_argument('-p', help = "port_number", required = True)

    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', int(args.p)))
    server.listen(5)

    try:
        conn, addr = server.accept()
        is_alive = True
        print('Connected to :', addr[0], ':', addr[1])

        socket_handler(conn)

    except KeyboardInterrupt:
        print("\nexit..")

    except socket.error as e:
        print(e)

    finally:
        is_alive = False
        server.close()

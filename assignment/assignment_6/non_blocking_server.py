import socket, errno, time, threading
import argparse

def recv_msg(conn):
    peer = conn.getpeername()
    data = ""

    while data.upper() != "QUIT":
        try:
            data = conn.recv(1024)
        
            if not data:
                print("Connection closed(data null)")
                break
        
            print("From {0}:{1}, {2}".format(peer[0], peer[1], data.decode()))
            
        except socket.error as e:
            if e.args[0] == errno.EWOULDBLOCK:
                time.sleep(0.25)
            else:
                print(e)
                break
        

def socket_handler(conn):
    conn.setblocking(0)
    recv_thread = threading.Thread(target=recv_msg, args=(conn,), daemon=True)
    recv_thread.start()

    msg = ""

    while msg.upper() != "QUIT":
        if not msg:
            msg = input()
        try:
            conn.sendall(msg.encode())
            
        except socket.error as e:
            if e.args[0] == errno.EWOULDBLOCK:
                time.sleep(0.25)
            elif e.args[0] == errno.EPIPE:
                print("Connection closed{0}".format(conn.getpeername()))
                break
            else:
                print(e)
                break
        else:
            msg = ""
        
        
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Thread server -p port")
    parser.add_argument('-p', help = "port_number", required = True)

    args = parser.parse_args()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', int(args.p)))
    server.listen(5)

    while True:
        try:
            conn, addr = server.accept()            
            print('Connected to :', addr[0], ':', addr[1])
            socket_handler(conn)

        except KeyboardInterrupt:
            print("exit..")
            break

        except socket.error as e:
            print(e)
            sys.exit(-1)

    server.close()

import socket
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Reverse server -p port")
    parser.add_argument('-p', help="port_number", required=True)
    args = parser.parse_args()

    host = ''   ## 127.0.0.1 Loop back
    port = int(args.p)

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
    
        while True:
            conn, addr = s.accept()
            print("Connect to {I} : {P}".format(I=addr[0], P=addr[1]))
            msg = conn.recv(1024).decode()
            print(msg)
            msg = msg[::-1]
            print(msg)
            conn.sendall(msg.encode())
            conn.close()

import socket
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo Cleint -i host -p port")
    parser.add_argument("-p", help="port_number", required=True)
    parser.add_argument("-i", help="host_address", required=True)

    args = parser.parse_args()

    port = int(args.p)
    host = args.i

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.connect((host, port))

        data = input(">>>")
        s.sendall(data.encode())

        data = s.recv(len(data))
        print(data.decode())

## client.py

import socket
import argparse

def recvall(sock, size):
    data = b''
    while True:
        part = sock.recv(size)
        data += part
        if len(part) < size:
            # either 0 or end of data
            break
    return data

def run(host, port, file_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(file_name.encode())
        file_size = int(s.recv(1024).decode())
        
        print("file name : {FILE}\nsize : {SIZE}".format(FILE=file_name, SIZE=file_size))
        
        if file_size == -1:
            print("No such file : {FILE}".format(FILE=file_name))
            return

        s.sendall("OK".encode())
        
        data = recvall(s, file_size)
        
        with open(file_name, mode="wb") as f:
            f.write(data)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo client -p port -i host -f file name")
    parser.add_argument('-p', help="port_number", required=True)
    parser.add_argument('-i', help="host_name", required=True)
    parser.add_argument('-f', help="file_name", required=True)

    args = parser.parse_args()
    run(host=args.i, port=int(args.p), file_name=args.f)



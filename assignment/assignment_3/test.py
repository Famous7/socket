## server.py

import socket
import argparse
import glob
import os.path


def run_server(port=8888, folder_path=""):
    host = '' ## 127.0.0.1 Loopback
  
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1) ## max 1 client

        conn, addr = s.accept()
        file_name = conn.recv(1024).decode()

        file_path = os.path.join(folder_path, file_name)
        
        if not is_exist(file_path):
            conn.send("No such file : {FILE}\n".format(FILE=file_name).encode())
        
        file_size = os.path.getsize(file_path)
        conn.send(str(file_size).encode())
        data = conn.recv(1024).decode()
        print(data)
        conn.send("dd".encode())
        #conn.sendall((str(file_size) + '2' + '\0').encode())
        
        # with open(os.path.join(folder_path, file_name), mode="rb") as f:
        #     data = f.read()
        #     conn.sendall(data.encode())

        conn.close()

def is_exist(file_path):
    files = glob.glob(file_path)

    if not files:
        return False

    return True
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo server -p port -d directory path")
    parser.add_argument('-p', help="port_number", required=True)
    parser.add_argument('-d', help="directory", required=True)

    args = parser.parse_args()
    run_server(port=int(args.p), folder_path=args.d)



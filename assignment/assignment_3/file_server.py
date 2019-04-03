## server.py

import socket
import argparse
import glob
import os.path


def run_server(port=8888, folder_path=""):
    host = '' ## 127.0.0.1 Loopback
  
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)

        conn, addr = s.accept()
        file_name = conn.recv(1024).decode()

        file_path = os.path.join(folder_path, file_name)
        
        if not is_exist(file_path):
            conn.send(str(-1).encode())
            conn.close()
            return
        
        file_size = os.path.getsize(file_path)
        print("file name : {FILE}\nsize : {SIZE}".format(FILE=file_path, SIZE=file_size))
        conn.send(str(file_size).encode())
        data = conn.recv(2)
	
	if data != "OK":
            conn.close()		
                
        with open(os.path.join(folder_path, file_name), mode="rb") as f:
            data = f.read()
            conn.sendall(data)

        conn.close()

def is_exist(file_path):
    return False if not glob.glob(file_path) else True
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo server -p port -d directory path")
    parser.add_argument('-p', help="port_number", required=True)
    parser.add_argument('-d', help="directory", required=True)

    args = parser.parse_args()
    run_server(port=int(args.p), folder_path=args.d)



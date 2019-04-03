import socket
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo client -p port -i host -s string")
    parser.add_argument('-p', help="port_number", required=True)
    parser.add_argument('-i', help="host_name", type=str, required=True)
    parser.add_argument('-s', help="input_string", type=str, required=True)

    args = parser.parse_args()
    host = args.i
    port = int(args.p)
    msg = args.s

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(msg.encode())
        resp = s.recv(len(msg))
        print(resp.decode())

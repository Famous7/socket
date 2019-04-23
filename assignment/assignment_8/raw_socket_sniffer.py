import os
import socket
import argparse

ETH_P_ALL = 0x0003

def sniffing(nic):
	sniffe_sock = None

	if os.name == 'nt':
		sniffe_sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)
		sniffe_sock.bind((nic,0))
		sniffe_sock.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
		sniffe_sock.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)
	else:
		sniffe_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(ETH_P_ALL))
		sniffe_sock.bind((nic, 0))

	data = sniffe_sock.recv(65535)

	for p in data:
		print("%02x" % p, end=" ")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='This is a simpe packet sniffer')
	parser.add_argument('-i', type=str, required=True, metavar='NIC name', help='NIC name')
	args = parser.parse_args()

	sniffing(args.i)

import os
import socket
import argparse

ETH_P_ALL = 0x0003

def sniffing(nic):
	if os.name == 'nt':
		address_familiy = socket.AF_INET
		protocol_type = socket.IPPROTO_IP
	else:
		address_familiy = socket.AF_PACKET
		protocol_type = socket.ntohs(ETH_P_ALL)

	with socket.socket(address_familiy, socket.SOCK_RAW, protocol_type) as sniffe_sock:
		sniffe_sock.bind((nic, 0))

		if os.name == 'nt':
			sniffe_sock.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
			sniffe_sock.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)
		
		data, _ = sniffe_sock.recvfrom(65535)

		for p in data:
			print("%02x" % p, end=" ")

		if os.name == 'nt':
			sniffe_sock.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='This is a simpe packet sniffer')
	parser.add_argument('-i', type=str, required=True, metavar='NIC name', help='NIC name')
	args = parser.parse_args()

	sniffing(args.i)


import os
import sys
import socket
import argparse
import struct

ETH_P_IP = 0x0800
ETH_P_ALL = 0x0003
ETH_SIZE = 14
MTU = 65535

def dumpcode(buf):
	print("%7s"% "offset ", end='')

	for i in range(0, 16):
		print("%02x " % i, end='')

		if not (i%16-7):
			print("- ", end='')

	print("")

	for i in range(0, len(buf)):
		if not i%16:
			print("0x%04x" % i, end= ' ')

		print("%02x" % buf[i], end= ' ')

		if not (i % 16 - 7):
			print("- ", end='')

		if not (i % 16 - 15):
			print(" ")

	print("")

def make_ethernet_header(raw_data):
	ether = struct.unpack('!6B6BH', raw_data)
	return {'dst':'%02x:%02x:%02x:%02x:%02x:%02x' % ether[:6],
	'src':'%02x:%02x:%02x:%02x:%02x:%02x' % ether[6:12],
	'ether_type':ether[12]}

def make_ip_header(raw_data):
	ip_ver_and_hlen = struct.unpack('!B', raw_data[:1])[0]

	ip_hlen = ip_ver_and_hlen & 0x0F
	raw_data = raw_data[:ip_hlen*4]

	ip = struct.unpack('!BHHHBBH', raw_data[1:12])
	return {'version':ip_ver_and_hlen >> 4,
	'header_length':ip_hlen,
	'tos':ip[0],
	'total_length':ip[1],
	'id':ip[2],
	'flag':ip[3] >> 13,
	'offset':ip[3] & 0x1FFF,
	'ttl':ip[4],
	'protocol':ip[5],
	'checksum':ip[6],
	'src':socket.inet_ntoa(raw_data[12:16]),
	'dst':socket.inet_ntoa(raw_data[16:20])
	}

def print_header(eth, ip):
	print_header.count += 1
	print('[{0}] IP_PACKET{1}\n'.format(print_header.count, '-'*45))

	print('Ethernet Header')
	for item in eth.items():
		print("[{0}] {1}".format(item[0], item[1]))

	print("\nIP HEADER")
	for item in ip.items():
		print("[{0}] {1}".format(item[0], item[1]))

print_header.count = 0

def parse_packet(data):
	eth_header = make_ethernet_header(data[:ETH_SIZE])

	if eth_header['ether_type'] != ETH_P_IP:
		return

	ip_header = make_ip_header(data[ETH_SIZE:])
	print_header(eth_header, ip_header)
	print('\nRaw Data')
	dumpcode(data)

	print('\n')

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='This is a simpe packet sniffer')
	parser.add_argument('-i', type=str, required=True, metavar='NIC name', help='NIC name')
	args = parser.parse_args()

	if os.name == 'nt':
		print("In Windows, we can't collect Ethernet frames.")
		sys.exit(-1)

	try:
		with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(ETH_P_ALL)) as sniffe_sock:
			sniffe_sock.bind((args.i, 0))

			while True:
				data, _ = sniffe_sock.recvfrom(MTU)
				parse_packet(data)

	except KeyboardInterrupt:
		print('EXIT...')

	except socket.error as e:
		print(e)

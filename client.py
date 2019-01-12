# The goal of the client is to send a encoded payload to the server every two seconds

import socket
import argparse
import time
import zlib
import struct

# Function that checks edge cases for command line flags
def verifyFlag(host):
    if len(host) < 2:
        print("Incorrect host format. Please enter host in the format of: \n127.0.0.1:5005")
        exit()
    else:
        if host[1] < 0 or host[1] > 65535:
            print("Please enter a port number within the valid range (0 to 65535)")
            exit()
        if len(host[0].split('.')) != 4:
            print("Please enter a valid IPv4 address (Ex: 127.0.0.1)")
            exit()
        host = host[0].split('.')
        for x in host:
            if int(x) < 0 or int(x) > 255:
                print("Please enter a valid IPv4 address (Ex: 127.0.0.1)")
                exit()

# Function that encodes payload
def constructPayload(ip, port, message):
    # Get checksum of message
    checksum = zlib.adler32(message)
    unixTime = int(time.time())
    ip = ip.split('.')

    # python struct module to encode the payload
    # Documentation found here: https://docs.python.org/2/library/struct.html
    # struct format string explanation ('>IQbbbbh61s')
    # '>' ensures that the payload is encoded using Big Endian(Most significant byte is placed at the lowest address)
    # 'I' encodes checksum as a 4 byte int
    # 'Q' encodes timestamp as a 8 byte int
    # 'BBBB' encodes each part of the IPv4 address as a 1 byte int for a total of 4 bytes for the IP addresses
    # 'h' encodes the port as a 2 byte int
    # '61s' encodes the message sring
    payload = struct.pack('>IQBBBBh61s', checksum, unixTime, int(ip[3]), int(ip[2]), int(ip[1]), int(ip[0]), port, message)

    return payload



def main():
    # python argparse module to handle command line flags
    # Documentation found here: https://docs.python.org/2/library/argparse.html#module-argparse
    # Ex cmd invoke -> python .\client.py --port 127.0.0.1:5005
    parser = argparse.ArgumentParser(description='Set port and host:port')
    parser.add_argument('--port', dest='host', action='store',
                        default = "127.0.0.1:5005",
                        help='set the host in format 127.0.0.1:5005 (default: 127.0.0.1:5005)')

    args = parser.parse_args()

    # Splits 127.0.0.1:5005 to list ['127.0.0.1', '5005']
    host = args.host.split(':')
    host[1] = int(host[1])

    verifyFlag(host)

    UDP_HOST = host[0]
    HOST_PORT = host[1]
    message = "\"It always seems impossible until it\'s done\" - Nelson Mandela"
    message = message.encode()

    print("UDP target Host:", UDP_HOST)
    print("UDP target port:", HOST_PORT)

    # python socket module to handle socket connections
    # Documentation found here: https://docs.python.org/3/library/socket.html
    sock = socket.socket(socket.AF_INET, # Internet
                          socket.SOCK_DGRAM) # UDP

    while(1):
        payload = constructPayload(UDP_HOST, HOST_PORT, message)
        sock.sendto(payload, (UDP_HOST, HOST_PORT))
        time.sleep(2) # Send payload every two seconds


if __name__== "__main__":
  main()

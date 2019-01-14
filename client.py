# The goal of the client is to send a encoded payload to the server every two seconds

import socket
import argparse
import time
import zlib
import struct

# Function that checks edge cases for command line flags
def verifyFlag(host):
    try:
        host[1] = int(host[1])
    except:
        print("Please enter a valid port.")
        exit()

    if len(host) < 2:
        print("Incorrect host format. Please enter host in the format of: \n127.0.0.1:5005")
        exit()
    else:
        if host[1] < 1 or host[1] > 65535:
            print("Please enter a port number within the valid range (1 to 65535)")
            exit()
        if len(host[0].split('.')) != 4:
            print("Please enter a valid IPv4 address (Ex: 127.0.0.1)")
            exit()
        host = host[0].split('.')
        for x in host:
            if x == '':
                print("Please enter a valid IPv4 address (Ex: 127.0.0.1)")
                exit()
            if int(x) < 0 or int(x) > 255:
                print("Please enter a valid IPv4 address (Ex: 127.0.0.1)")
                exit()

# Function that encodes payload
def constructPayload(ip, port, message):
    unixTime = int(time.time())
    # Split IP into 4 distinct parts
    ip = ip.split('.')
    
    # Create payload
    payload = struct.pack('>QBBBBH61s', unixTime, int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3]), port, message)

    # Get checksum of message
    checksum = zlib.adler32(payload)

        # python struct module to encode the payload
    # Documentation found here: https://docs.python.org/2/library/struct.html
    # struct format string explanation ('>IQbbbbh61s')
    # '>' ensures that the payload is encoded using Big Endian(Most significant byte is placed at the lowest address)
    # 'I' encodes checksum as a 4 byte int
    # 'Q' encodes timestamp as a 8 byte int
    # 'BBBB' encodes each part of the IPv4 address as a 1 byte int for a total of 4 bytes for the IP addresses
    # 'H' encodes the port as a 2 byte int
    # '61s' encodes the message sring
    payload = struct.pack('>IQBBBBH61s', checksum, unixTime, int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3]), port, message)

    if struct.calcsize('>IQBBBBh61s') > 64000:
        print("Payload exceeds the default UDP MTU size (64k)")
        exit()

    return payload



def main():
    # python argparse module to handle command line flags
    # Documentation found here: https://docs.python.org/2/library/argparse.html#module-argparse
    # Ex cmd invoke -> python .\client.py --host 127.0.0.1:5005
    parser = argparse.ArgumentParser(description='Set host:port')
    parser.add_argument('--host', dest='host', action='store',
                        default = "127.0.0.1:5005",
                        help='set the host in format 127.0.0.1:5005 (default: 127.0.0.1:5005)')

    args = parser.parse_args()

    # Splits 127.0.0.1:5005 to list ['127.0.0.1', '5005']
    host = args.host.split(':')
    verifyFlag(host)
    host[1] = int(host[1])

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

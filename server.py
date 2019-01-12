# The goal of the server is to listen for messages from the client and decode them
import socket
import argparse
import struct
import zlib
import time

# Function that checks edge cases for command line flags
def verifyFlag(host):
    if len(host) < 2:
        print("Incorrect host format. Please enter host in the format of: \n127.0.0.1:5005")
        exit()
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

def decodeMessage(data, count):
    ip = [0, 0, 0, 0]
    checksum, timestamp, ip[0], ip[1], ip[2], ip[3], port, message = struct.unpack('>IQbbbbh61s', data)

    # Check the checksum
    if checksum != zlib.adler32(message):
        print("Checksum does not match. Message possibly corrupt.")

    message = message.decode()
    # Format IP address
    ip = str(ip[0]) + '.' + str(ip[1]) + '.' + str(ip[2]) + '.' + str(ip[3])

    # Logic for keeping track of message count
    if ip in count:
        count[ip] += 1
    else:
        count[ip] = 1

    # Calculate the elapsed time since the message was sent
    cTime = time.time()
    elapsedTime = round(cTime - timestamp, 5)

    # Print requested information
    print("Message: " + message)
    print("Time Elapsed: " + str(elapsedTime) + " seconds")
    print("Source IPv4: " + ip)
    print("Message Count: " + str(count[ip]))


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
    UDP_PORT = host[1]

    # python socket module to handle socket connections
    # Documentation found here: https://docs.python.org/3/library/socket.html
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_HOST, UDP_PORT))

    print("Listening for " + host[0] + " on port: " + str(host[1]) )

    # Python Dictionary to keep track of IPv4 message count
    # Useful because if a multipe IP addresses are introduced the code scales
    count = {}

    while(1):

        data, addr = sock.recvfrom(1024) # buffer size of 1024 bytes
        data = decodeMessage(data, count)

if __name__== "__main__":
  main()

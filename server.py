# The goal of the server is to listen for messages from the client and decode them
import socket
import argparse
import struct
import zlib
import time

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

def decodeMessage(data, count):
    ip = [0, 0, 0, 0]

    # python struct module to decode the payload
    # Documentation found here: https://docs.python.org/2/library/struct.html
    # struct format string explanation ('>IQbbbbh61s')
    # '>' ensures that the payload is decoded using Big Endian(Most significant byte is placed at the lowest address)
    # 'I' decodes checksum as a 4 byte int
    # 'Q' decodes timestamp as a 8 byte int
    # 'BBBB' decodes each part of the IPv4 address as a 1 byte int for a total of 4 bytes for the IP addresses
    # 'H' decodes the port as a 2 byte int
    # '61s' decodes the message sring
    checksum, timestamp, ip[0], ip[1], ip[2], ip[3], port, message = struct.unpack('>IQBBBBH61s', data)
    
    # Pack payload back to recalculate checksum
    payload = struct.pack(">QBBBBH61s", timestamp, ip[0], ip[1], ip[2], ip[3], port, message)

    # Check the checksum
    if checksum != zlib.adler32(payload):
        print("Checksum does not match. Message possibly corrupt.")

    message = message.decode()
    # Format IP address
    ip = str(ip[3]) + '.' + str(ip[2]) + '.' + str(ip[1]) + '.' + str(ip[0])

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
                        help='set the port in format 127.0.0.1:5005 (default: 127.0.0.1:5005)')

    args = parser.parse_args()

    # Splits 127.0.0.1:5005 to list ['127.0.0.1', '5005']
    host = args.host.split(':')
    verifyFlag(host)
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

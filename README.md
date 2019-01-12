# UDP
My implementation of a UDP client/server relationship
To invoke the program first run server.py and then client.py
If no command line flags are used then the default is set to 127.0.0.1:5005

EX: python .\server.py --port 127.0.0.1:5005
### Client Overview
The goal of the client is to send a encoded payload to the server every two seconds
### Server Overview
The goal of the server is to listen for messages from the client and decode them
### Useful Resources I Used
..*Python socket Module -> https://docs.python.org/3/library/socket.html
..*Python argparse Module for command line flags -> https://docs.python.org/2/library/argparse.html#module-argparse
..*Python struct Module for encoding payload -> https://docs.python.org/2/library/struct.html
..*Python zlib module used to compute the adler32 checksum -> https://docs.python.org/3/library/zlib.html
..*Python time Module used to send payload every two seconds and get the UNIX time value -> https://docs.python.org/3/library/time.html

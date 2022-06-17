import socket
import numpy as np
import re

# Host machine IP/IP address of Windows VM
host = "192.168.56.101"
# Gazepoint Port
port = 4242
address = (host, port)
# Connect to Gazepoint control server on Windows VM
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

# Send command to request certain data
s.send(str.encode('<SET ID="ENABLE_SEND_BLINK" STATE="1" />\r\n'))
s.send(str.encode('<SET ID="ENABLE_SEND_POG_BEST" STATE="1" />\r\n'))
# Enable the server to return the data requested
s.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n'))

for i in range(5):
        s.recv(1024)

# Regex that only includes numbers and .
numbers = re.compile(r'\d+(?:\.\d+)?')

while 1:
    newlist = []
    rxdat = s.recv(1024)  # Receive data from server
    rxdat = bytes.decode(rxdat)

    # Split each data point into a separate item
    rxdat = rxdat.split()
    # Remove the first and last item in the list
    # Removes '<REC' and '/>' items
    rxdat = rxdat[1:-1]

    # Convert to numpy array
    rxdat = np.asarray(rxdat)
    # make array vertical + converts into 2d array
    rxdat = rxdat.reshape(-1, 1)

    # Converts to pure float values and appends to newlist
    for i in range(len(rxdat)):
        temp = (numbers.findall(rxdat[i][0]))
        temp = float(temp[0])
        newlist.append(temp)

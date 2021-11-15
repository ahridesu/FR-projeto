import psutil
import socket
import signal
import struct
import sys

from time import sleep

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

##

ip_addr = '127.0.0.1'
tcp_port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip_addr, tcp_port))

if __name__ == '__main__':

    while True:
        try: 
            #order += 1
            sleep(2.0)
            
            cpu = psutil.cpu_percent()
            print('CPU Utilization: {}%'.format(cpu) )
            
            mem = psutil.virtual_memory().percent
            print('Memory in Usage: {}%\n'.format(mem) )

            pkt = struct.pack('ff', cpu, mem)
            sock.send(pkt)
        
        except (socket.timeout, socket.error):
            print('Server error. Done!')
            sys.exit(0)

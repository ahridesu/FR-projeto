import socket
import threading
import signal
import sys
import struct

def signal_handler(sig, frame):
    print('\nDone!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to exit...')

##

def handle_client_connection(client_socket, address): 
    print('Accepted connection from {}:{}'.format(address[0], address[1]))   
    try:
        while True:
            request = client_socket.recv( struct.calcsize('ff') )
            
            cpu, mem = struct.unpack('ff', request)
            
            print('Client {}:'.format(address))
            print('    CPU Utilization: {:.2f}%'.format(cpu) )
            print('    Memory in Usage: {}%\n'.format(mem) )
    
    except (socket.timeout, socket.error):
        print('Client {} error. Done!'.format(address))
    finally:
        client_socket.close()

ip_addr = "0.0.0.0"
tcp_port = 5005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip_addr, tcp_port))

if __name__ == '__main__':

    server.listen(5)  # max backlog of connections
    print('Listening on {}:{}'.format(ip_addr, tcp_port))

    while True:
        client_sock, address = server.accept()
        client_handler = threading.Thread(target=handle_client_connection,args=(client_sock,address),daemon=True)
        client_handler.start()

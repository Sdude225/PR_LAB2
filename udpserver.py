import socket
from ClientObject import ClientObject
from transport_prot import *

BUFF_SIZE=4096

def udpserver():
    sock = init_server()
    while(True):
        data, address = sock.recvfrom(BUFF_SIZE)
        msg = generate_hamming_code(convert_to_bits('CYBERPUNK ETA MAYA JIZNI NAHUI'))
        sock.sendto(msg.encode(), address)

if __name__ == "__main__":
    udpserver()
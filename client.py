import socket
import ClientObject
from transport_prot import *

def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_adrress = ('localhost', 10000)

    try:
        sock.sendto(''.encode(), server_adrress)
        data, address = sock.recvfrom(4096)
        data = correct_and_decrypt_hamming_code(data.decode())
        print(to_string(data))

    finally:
        sock.close()

if __name__ == "__main__":
    client()
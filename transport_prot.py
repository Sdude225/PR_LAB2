import socket
import hamming
from header_types import Header_Types
import selectors
import session_prot

BUFF_SIZE = 4096

class MySocket:

    def __init__(self, sock = None):
        self.clients_addresses = []
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.session = session_prot.Session()
            self.selector = selectors.DefaultSelector()
            self.sock.setblocking(False)
            self.selector.register(self.sock, selectors.EVENT_READ, self.receive_message)
        else:
            self.sock = sock

    def bind_server(self, host, port):
        self.sock.bind((host, port))
        self.host = host
        self.port = port

    def close_sock(self):
        self.sock.close()

    def select_loop(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                callback = key.data
                callback()

    def receive_message(self):
        data, address = self.sock.recvfrom(BUFF_SIZE)
        msg = hamming.correct_and_decrypt_hamming_code(data.decode())
        msg = hamming.to_string(msg)
        header = msg[:Header_Types.header_size.value]

        if header == Header_Types.ping.value:
            print('ping detected')
            self.clients_addresses.append(address[1])

        elif header == Header_Types.delete_number.value:
            print('del number')
            self.clients_addresses.remove(address[1])

        elif header == Header_Types.syn_message.value:
            print('incoming call request from ' + str(address[1]))
            self.session.other_client_number = address[1]
            self.session.gen_full_key(int(msg[Header_Types.header_size.value:]))

        elif header == Header_Types.syn_response.value:
            self.session.other_client_number = address[1]
            self.session.gen_full_key(int(msg[Header_Types.header_size.value:]))
            print('Connection established')

        elif header == Header_Types.end_message.value:
            print(msg[Header_Types.header_size.value:])

        elif header == Header_Types.encrypted_end_message.value:
            decypted_msg = self.session.decrypt_message(msg[Header_Types.header_size.value:])
            print(decypted_msg)

        elif header == Header_Types.request_clients_numbers.value:
            clients_addresses_string_list = [str(int) for int in self.clients_addresses]
            clients_addresses_string = '\n'.join(clients_addresses_string_list)
            self.send_message(Header_Types.end_message.value + clients_addresses_string, address[0], address[1])


    def send_message(self, data, host, address):
        data = hamming.generate_hamming_code(hamming.convert_to_bits(data))
        self.sock.sendto(data.encode(), (host, address))

        
        

from header_types import Header_Types
import transport_prot, session_prot
import threading
import time

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 10000

class Application:

    def __init__(self):
        self.sock = transport_prot.MySocket()

        self.thread = threading.Thread(target=self.sock.select_loop)
        self.thread.start()

        self.sock.send_message(self.ping_message(''), SERVER_ADDRESS, SERVER_PORT)
        self.idle_listening()

    def idle_listening(self):
        print('res - respond to call, pck - pick up trubka')
        while(True):
            command = input()

            if command == 'pck':
                self.main_client_loop()

            elif command == 'res':
                self.sock.send_message(Header_Types.syn_response.value + str(self.sock.session.gen_partial_key()), SERVER_ADDRESS, self.sock.session.other_client_number)
                self.on_call()

            else:
                print('Unknown command, please try again')
                continue

    def main_client_loop(self):
        print('req - get numbers, call - call existing client, ext - exit')
        while(True):
            command = input()

            if command == 'req':
                self.sock.send_message(self.request_clients_number(''), SERVER_ADDRESS, SERVER_PORT)

            elif command == 'ext':
                self.sock.send_message(self.del_number_on_exit(''), SERVER_ADDRESS, SERVER_PORT)
                self.sock.close_sock()
                break

            elif command == 'call':
                print('enter client number')
                number = input()
                self.sock.session.other_client_number = int(number)
                self.sock.send_message(self.syn_message(str(self.sock.session.gen_partial_key())), SERVER_ADDRESS, int(number))
                self.on_call()
            else:
                print('Unknown command, please try again')
                continue

    def on_call(self):
        print('ext - end call, any other string to send to connected client')
        while(True):
            msg = input()
            if msg == 'ext':
                self.sock.send_message(self.end_message('Partner ended the call, please input ext to exit'), SERVER_ADDRESS, self.sock.session.other_client_number)
                self.sock.session.full_key = None
                self.sock.session.other_client_number = None
                self.idle_listening()

            else:
                self.sock.send_message(self.encrypted_end_message(msg), SERVER_ADDRESS, self.sock.session.other_client_number)
    
    def del_number_on_exit(self, data):
        msg = Header_Types.delete_number.value + data
        return msg

    def ping_message(self, data):
        msg = Header_Types.ping.value + data
        return msg

    def end_message(self, data):
        msg = Header_Types.end_message.value + data
        return msg

    def encrypted_end_message(self, data):
        msg = Header_Types.encrypted_end_message.value + ascii(self.sock.session.encrypt_message(data))
        return msg

    def syn_message(self, data):
        msg = Header_Types.syn_message.value + data
        return msg

    def request_clients_number(self, data):
        msg = Header_Types.request_clients_numbers.value + data
        return msg

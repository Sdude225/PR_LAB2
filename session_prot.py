from session_prot_utility import generate_prime
from Crypto.Cipher import AES

class Session:

    def __init__(self):
        self.pub_key1 = 4001
        self.pub_key2 = 5003
        self.priv_key = generate_prime()
        self.full_key = None
        self.other_client_number = None

    def gen_partial_key(self):
        partial_key = self.pub_key1 ** self.priv_key
        partial_key = partial_key % self.pub_key2
        return partial_key

    def gen_full_key(self, partial_key):
        full_key = partial_key ** self.priv_key
        full_key = full_key % self.pub_key2
        self.full_key = full_key
        return full_key

    def encrypt_message(self, msg):
        encrypted_msg = ''
        for c in msg:
            encrypted_msg += chr(ord(c) + self.full_key)
        return encrypted_msg

    def decrypt_message(self, encrypted_msg):
        decrypted_msg = ''
        encrypted_msg = ''.join((filter(lambda i: i != '\'', encrypted_msg)))
        encrypted_msg = encrypted_msg.split('\\u')
        encrypted_msg.pop(0)
        for c in encrypted_msg:
            decrypted_msg += chr(int(c, 16) - self.full_key)
        return decrypted_msg
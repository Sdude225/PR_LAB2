import socket

def init_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 10000)
    sock.bind(server_address)
    print('server is running')
    return sock

def convert_to_bits(input_data):
    return ''.join(f"{ord(i):08b}" for i in input_data)

def generate_hamming_code(input_data):
    bits_sequence = list(input_data)
    bits_sequence.reverse()
    c = 0
    ch = 0 # indx pos
    j = 0 
    r = 0 # redunded bits
    h = [] # haming code

    while (len(input_data) + r + 1) > (pow(2, r)):
        r = r + 1

    for i in range(0, (r + len(bits_sequence))):
        p = 2 ** c

        if p == (i + 1):
            h.append(0)
            c = c + 1
        
        else:
            h.append(int(bits_sequence[j]))
            j = j + 1

    for par in range(0, len(h)):
        ph = 2 ** ch

        if ph == (par + 1):
            index = ph - 1
            i = index
            xor = []

            while i < len(h):
                block = h[i:i + ph]
                xor.extend(block)
                i += 2 * ph

            for z in range(1, len(xor)):
                h[index] = h[index] ^ xor[z]
            
            ch += 1

    h.reverse()
    return str(''.join(map(str, h)))


def correct_and_decrypt_hamming_code(input_data):
    bits_sequence = list(input_data)
    bits_sequence.reverse()
    c = 0
    ch = 0
    error = 0
    h = []
    parity_list = []
    parity_index_list = []
    h_corrected = []

    for k in range(0, len(bits_sequence)):
        p = 2 ** c
        h.append(int(bits_sequence[k]))
        h_corrected.append(bits_sequence[k])

        if p == (k + 1):
            c = c + 1

    for par in range(0, len(h)):
        ph = 2 ** ch

        if ph == (par + 1):
            index = ph - 1
            i = index
            xor = []

            while i < len(h):
                block = h[i:i + ph]
                xor.extend(block)
                i += 2 * ph

            for z in range(1, len(xor)):
                h[index] = h[index] ^ xor[z]
            
            parity_list.append(h[par])
            parity_index_list.append(index)
            ch += 1
    
    parity_list.reverse()
    error=sum(int(parity_list) * (2 ** i) for i, parity_list in enumerate(parity_list[::-1]))

    if error == 0:
        for i, n in enumerate(h):
            if i in parity_index_list:
                h[i] = 2

        h = list(filter(lambda x: x != 2, h))
        h.reverse()
        return str(''.join(map(str, h)))

    elif error >= len(h_corrected):
        print('error can\'t be detected')

    else:
        print('error is corrected')
        if h_corrected[error - 1] == '0':
            h_corrected[error - 1] = '1'

        elif h_corrected[error - 1] == '1':
            h_corrected[error - 1] = '0'

        for i, n in enumerate(h_corrected):
            if i in parity_index_list:
                h_corrected[i] = 2

        h_corrected = list(filter(lambda x: x != 2, h_corrected))
        h_corrected.reverse()
        return str(''.join(map(str, h_corrected)))


def to_string(binary_sequence):
    binary_int = int(binary_sequence, 2)
    byte_number = binary_int.bit_length() + 7 // 8
    binary_array = binary_int.to_bytes(byte_number, 'big')
    ascii_text = binary_array.decode()

    return ascii_text
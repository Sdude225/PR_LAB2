import transport_prot


def udpserver():
    sock = transport_prot.MySocket()
    sock.bind_server('localhost', 10000)
    sock.select_loop()

if __name__ == "__main__":
    udpserver()
import socket
from configs import BUFFER_SIZE, ROOT_DNS_IP, ROOT_DNS_PORT


class DNSForwarder:
    def __init__(self):
        self.root_ip = ROOT_DNS_IP
        self.root_port = ROOT_DNS_PORT

    def transit(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, (self.root_ip, self.root_port))
        sock.settimeout(4)

        return sock.recv(BUFFER_SIZE)

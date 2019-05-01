import socket
from dns.dns_controller import DNSController


self_addr = '127.0.0.1', 53

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dns_ya_ru = b'\x00\x03\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x02ya\x02ru\x00\x00\x01\x00\x01'
    sock.sendto(dns_ya_ru, self_addr)

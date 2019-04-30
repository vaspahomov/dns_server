import socket
from dns.dns_controller import DNSController


self_addr = '127.0.0.1', 53

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.settimeout(5)
    sock.bind(self_addr)
    data, from_addr = sock.recvfrom(1024)

    controller = DNSController()

    print(f'Received {data} from {from_addr}')

    answer = controller.run(data)
    # self.transport.sendto(answer, server_addr)
    sock.sendto(answer, from_addr)

    print(f'Send {answer} to {from_addr}')

import asyncio
from dns.dns_controller import DNSController
import socket


class DNSServer(asyncio.DatagramProtocol):
    def __init__(self):
        self.controller = DNSController()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr, args=None):
        server_addr = (addr[0], addr[1])
        print(f'Received {data} from {addr}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        answer = self.controller.run(data)
        self.transport.sendto(answer, server_addr)
        # sock.settimeout(2)
        sock.sendto(answer, ('8.8.8.8', 53))
        print(f'Send {answer} to {server_addr}')


    def start(self):
        loop = asyncio.get_event_loop()
        print("Starting DNS server")

        listen = loop.create_datagram_endpoint(
            DNSServer,
            local_addr=('127.0.0.1', 53),
        )

        self.transport, self.protocol = loop.run_until_complete(listen)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print('Stopping DNS server')
        self.transport.close()
        self.loop.close()

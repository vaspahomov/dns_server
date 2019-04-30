from bitstring import BitArray
from dns.dns_header import DNSHeader
from dns.dns_rr_message import DNSRRMessage
from dns_utils.zones_controller import ZoneController


class DNSMessage:
    def __init__(self):
        self.header: DNSHeader
        self.questions: list = []
        self.answers: list = []
        self.authority: list = []
        self.additional_information: list = []
        self.message: bytes

    def parse_message(self, message: bytes):
        self.message = message
        bit_message = BitArray(message)
        self.header = DNSHeader()
        self.header = self.header.parse(bit_message[0:96])
        index = 12
        for e in range(self.header.qdcount.int):
            question = DNSRRMessage()
            index = question.parse(message, index, True) + 1
            self.questions.append(question)

        for e in range(self.header.ancount.int):
            answer = DNSRRMessage()
            index = answer.parse(message, index) + 1
            self.answers.append(answer)

        for e in range(self.header.nscount.int):
            authority = DNSRRMessage()
            index = authority.parse(message, index) + 1
            self.authority.append(authority)

        for e in range(self.header.arcount.int):
            additional = DNSRRMessage()
            index = additional.parse(message, index) + 1
            self.additional_information.append(additional)

        return self

    def index_of_end_of_end_request(self, message):
        self.message = message
        bit_message = BitArray(message)
        self.header = DNSHeader()
        self.header = self.header.parse(bit_message[0:96])
        index = 12
        for e in range(self.header.qdcount.int):
            question = DNSRRMessage()
            return question.parse(message, index, True)

    def format_message(self, answers, request_message_bytes) -> bytes:
        res = b''
        i = self.index_of_end_of_end_request(request_message_bytes)
        part_of_old_message = request_message_bytes[0: i + 1]
        res += self.header.format_header(self.header, request_message_bytes[0:12])

        answers_1 = int(len(answers) / 256)
        answers_2 = int(len(answers) % 256)
        res += bytes([0, 1, answers_1, answers_2, 0, 0, 0, 0])

        res += part_of_old_message[12:]
        mess = DNSRRMessage()
        for answer in answers:
            res += mess.format_rr_message(answer.name, answer.qtype, answer.qclass, answer.ttl, answer.resource_data)
        return res

    def print_data(self, mess):
        print('question')
        print(self.header.qdcount.int)
        for e in self.questions:
            print(f'name:{e.names}')
            print(f'qtype:{e.qtype}')
            print(f'qclass:{e.qclass}')

        print('answer')
        print(self.header.ancount.int)
        for e in self.answers:
            print(f'name:{e.names}')
            print(f'qtype:{e.qtype}')
            print(f'qclass:{e.qclass}')
            print(f'ttl:{e.ttl}')
            print(f'data:{e.resourse_data}')

            z = ZoneController()
            if e.qtype == 'A':
                print(f'A data:{e.resourse_data}')
            if e.qtype == 'AAAA':
                print(f'AAAA data:{e.resourse_data}')
            if e.qtype == 'NS':
                print(f'NS data:{e.resourse_data}')
            if e.qtype == 'PTR':
                print(f'PTR data:{e.resourse_data}')
            if e.qtype == 'CNAME':
                print(f'CNAME data:{e.resourse_data}')

        print('authority')
        print(self.header.nscount.int)
        for e in self.authority:
            print(f'name:{e.names}')
            print(f'qtype:{e.qtype}')
            print(f'qclass:{e.qclass}')
            print(f'ttl:{e.ttl}')
            print(f'data:{e.resourse_data}')

            z = ZoneController()
            if e.qtype == 'A':
                print(f'A data:{e.resourse_data}')
            if e.qtype == 'AAAA':
                print(f'AAAA data:{e.resourse_data}')
            if e.qtype == 'NS':
                print(f'NS data:{e.resourse_data}')
            if e.qtype == 'PTR':
                print(f'PTR data:{e.resourse_data}')
            if e.qtype == 'CNAME':
                print(f'CNAME data:{e.resourse_data}')

        print('additional')
        print(self.header.arcount.int)
        for e in self.additional_information:
            print(f'name:{e.names}')
            print(f'qtype:{e.qtype}')
            print(f'qclass:{e.qclass}')
            print(f'ttl:{e.ttl}')
            print(f'data:{e.resourse_data}')

        return self

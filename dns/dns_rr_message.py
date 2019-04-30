class DNSRRMessage:
    def __init__(self):
        self.names = []
        self.qtype = None
        self.qclass = None
        self.ttl = None
        self.resourse_data: bytes = None

    def parse(self, message: bytes, shift_index: int, is_question=False):
        index = 0
        i = 0
        current_name = []
        while True:
            if len(message) <= shift_index + index:
                break
            b = message[shift_index + index]
            if i == 0:
                if b >= 192:
                    next_byte = message[shift_index + index + 1]
                    ref_ind = (b - 192) * 256 + next_byte
                    ind = 0
                    while message[ref_ind + ind] != 0:
                        if message[ref_ind + ind] >= 192:
                            ss = message[ref_ind + ind]
                            _next_byte = message[ref_ind + ind + 1]
                            _ref_ind = (ss - 192) * 256 + _next_byte
                            _ind = 0
                            while message[_ref_ind + _ind] != 0:
                                _local_shift = message[_ref_ind + _ind]
                                __current_name = []
                                for _e in range(_local_shift):
                                    __current_name.append(message[_ref_ind + _ind + _e + 1])
                                _ind += _local_shift + 1
                                self.names.append(__current_name)
                            break
                        else:
                            local_shift = message[ref_ind + ind]
                            _current_name = []
                            for e in range(local_shift):
                                _current_name.append(message[ref_ind + ind + e + 1])
                            ind += local_shift + 1
                            self.names.append(_current_name)

                    index += 1
                else:
                    i = int(b)
                if current_name:
                    self.names.append(current_name)
                if b == 0:
                    break
                current_name = []
            else:
                current_name.append(b)
                i -= 1
            index += 1
        if is_question:
            self.qtype = self.get_record_type(message[shift_index + index + 1: shift_index + index + 3])
            self.qclass = self.get_record_class(message[shift_index + index + 3: shift_index + index + 5])
            return shift_index + index + 4
        self.qtype = self.get_record_type(message[shift_index + index + 0: shift_index + index + 2])
        self.qclass = self.get_record_class(message[shift_index + index + 2: shift_index + index + 4])
        self.ttl = int.from_bytes(message[shift_index + index + 4: shift_index + index + 6], byteorder='big') * 256 + \
                   int.from_bytes(message[shift_index + index + 6: shift_index + index + 8], byteorder='big')
        data_len = message[shift_index + index + 8: shift_index + index + 10]
        resourse_data = message[
                        shift_index + index + 10: shift_index + index + 10 + data_len[0] * 256 + data_len[1]]

        if self.qtype == 'A':
            self.resourse_data = self.get_a_data(resourse_data)
        if self.qtype == 'AAAA':
            self.resourse_data = self.get_aaaa_data(resourse_data)
        if self.qtype == 'CNAME':
            self.resourse_data = self.get_ns_data(resourse_data, message)
        if self.qtype == 'NS':
            self.resourse_data = self.get_ns_data(resourse_data, message)

        return shift_index + index + 10 + int(data_len[0] * 256 + data_len[1] - 1)

    def get_a_data(self, a_data_bytes: bytes):
        return '.'.join(list(map(lambda x: str(int(x)), a_data_bytes)))

    def get_aaaa_data(self, a_data_bytes: bytes):
        return ':'.join(list(map(lambda x: str(int(x)), a_data_bytes)))

    def get_ns_data(self, ns_data_bytes: bytes, message):
        res = []
        i = 0
        index = 0
        curr = []
        while True:
            b = ns_data_bytes[index]
            if b == 0:
                break
            if i == 0:
                if curr != []:
                    res.append(curr)
                if b >= 192:
                    next_b = ns_data_bytes[index + 1]
                    shift = (b - 192) * 256 + next_b
                    res += self.parse_from_pointer(message, shift)
                    break
                else:
                    i = int(b)
                    curr = []
            else:
                i -= 1
                curr.append(b)
            index += 1

        return self.join_name(res)

    def get_ns_data(self, ns_data_bytes: bytes, message):
        res = []
        i = 0
        index = 0
        curr = []
        while True:
            b = ns_data_bytes[index]
            if b == 0:
                break
            if i == 0:
                if curr != []:
                    res.append(curr)
                if b >= 192:
                    next_b = ns_data_bytes[index + 1]
                    shift = (b - 192) * 256 + next_b
                    res += self.parse_from_pointer(message, shift)
                    break
                else:
                    i = int(b)
                    curr = []
            else:
                i -= 1
                curr.append(b)
            index += 1

        return self.join_name(res)

    def join_name(self, name):
        res = []
        for e in name:
            st = ''
            for i in e:
                st += chr(i)
            res.append(st)

        return '.'.join(res)

    def parse_from_pointer(self, message, shift):
        res = []
        _curr = []
        ind = 0
        while message[shift + ind] != 0:
            b = message[shift + ind]
            if b >= 192:
                next_b = message[shift + ind + 1]
                shift = (b - 192) * 256 + next_b
                _curr = self.parse_from_pointer(message, shift)
                res += _curr
                return res
            _curr = []
            for e in range(b):
                _curr.append(message[shift + ind + e + 1])
            ind += message[shift + ind] + 1
            res.append(_curr)
            _curr = []

        return res

    def get_record_class(self, record_bytes: bytes):
        if record_bytes == b'\x00\x01':
            return 'IN'
        return 'QUESTION'

    def get_record_type(self, record_bytes: bytes):
        if record_bytes == b'\x00\x01':
            return 'A'
        if record_bytes == b'\x00\x02':
            return 'NS'
        if record_bytes == b'\x00\x05':
            return 'CNAME'
        if record_bytes == b'\x00\x06':
            return 'SOA'
        if record_bytes == b'\x00\x0b':
            return 'WKS'
        if record_bytes == b'\x00\x0c':
            return 'PTR'
        if record_bytes == b'\x00\x0f':
            return 'MX'
        if record_bytes == b'\x00\x21':
            return 'SRV'
        if record_bytes == b'\x00\x1c':
            return 'AAAA'
        if record_bytes == b'\x00\xff':
            return 'ANY'
        if record_bytes == b'\x00\x00':
            return 'QUESTION'

        # raise Exception(f'Unknown type: {record_bytes}')

    def format_rr_message(self, name, qtype, qclass, ttl, resourse_data):
        res = b''

        for name_part in name.split('.'):
            res += bytes([len(name_part)])
            res += bytes(name_part.encode())

        res += b'\x00'
        if qtype == 'A':
            res += b'\x00\x01'
        if qtype == 'NS':
            res += b'\x00\x02'
        if qtype == 'CNAME':
            res += b'\x00\x05'
        if qtype == 'SOA':
            res += b'\x00\x06'
        if qtype == 'WKS':
            res += b'\x00\x0b'
        if qtype == 'PTR':
            res += b'\x00\x0c'
        if qtype == 'MX':
            res += b'\x00\x0f'
        if qtype == 'SRV':
            res += b'\x00\x21'
        if qtype == 'AAAA':
            res += b'\x00\x1c'
        if qtype == 'ANY':
            res += b'\x00\xff'

        if qclass == 'IN':
            res += b'\x00\x01'
        else:
            raise Exception('Not implemented')

        res += bytes([
            int((ttl / (256 * 256 * 256))),
            int((ttl / (256 * 256))),
            int((ttl / (256))),
            ttl % 256
        ])

        if qtype == 'A':
            splitted_ip = resourse_data.split('.')
            ip_byptes = list(map(lambda x: int(x.encode()), splitted_ip))
            res += bytes([
                int(len(ip_byptes) / 256),
                len(ip_byptes) % 256
            ])
            res += bytes(ip_byptes)
            if qtype == 'NS':
                raise Exception('Not implemented')
        if qtype == 'CNAME':
            raise Exception('Not implemented')
        if qtype == 'AAAA':
            splitted_ip = resourse_data.split(':')
            ip_byptes = list(map(lambda x: int(x.encode()), splitted_ip))
            res += bytes([
                int(len(ip_byptes) / 256),
                len(ip_byptes) % 256
            ])
            res += bytes(ip_byptes)

        return res

from bitstring import BitArray


class DNSHeader:
    def __init__(self):
        self.id: BitArray
        self.qr: BitArray
        self.opcode: BitArray
        self.aa: BitArray
        self.tc: BitArray
        self.rd: BitArray
        self.ra: BitArray
        self.z: BitArray
        self.rcode: BitArray
        self.qdcount: BitArray
        self.ancount: BitArray
        self.nscount: BitArray
        self.arcount: BitArray

    def parse(self, header: BitArray):
        self.id = header[0:16]
        self.qr = header[16:17]
        self.opcode = header[17:21]
        self.aa = header[21:22]
        self.tc = header[22:23]
        self.rd = header[23:24]
        self.ra = header[24:25]
        self.z = header[25:28]
        self.rcode = header[28:32]
        self.qdcount = header[32:48]
        self.ancount = header[48:64]
        self.nscount = header[64:80]
        self.arcount = header[80:96]

        return self

    def format_header(self, old_header, old_header_bytes):
        _res = old_header_bytes
        ss = (old_header.id.bin + '1' + old_header.opcode.bin + '0' + '0' + old_header.rd.bin + '0' + '000' + old_header.rcode.bin)
        res = int(ss, 2)
        import math
        s = bytes([
            math.floor(res / (256 * 256 * 256) % 256),
            math.floor(res / (256 * 256) % 256),
            math.floor((res / 256) % 256),
            math.floor(res % 256),
        ])

        return s

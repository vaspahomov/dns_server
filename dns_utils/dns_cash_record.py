class DNSCashRecord:
    def __init__(self, name: str, qtype: str, qclass: str, ttl: str, resource_data: str):
        self.name = name
        self.qtype = qtype
        self.qclass = qclass
        self.ttl = ttl
        self.resource_data = resource_data

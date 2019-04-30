from blockstack_zones.parse_zone_file import parse_zone_file
import json

class DNSZone:
    def __init__(self):
        self.zone_file_object = None
        self.origin: str
        self.ttl: str
        self.a: list
        self.aaaa: list
        self.cname: list
        self.ns: list

    def load(self, zone_file):
        zone_file_object = parse_zone_file(zone_file)
        self.zone_file_object = json.loads(zone_file_object)

        self.origin = self.zone_file_object['origin']
        self.ttl = self.zone_file_object['ttl']
        self.a = self.zone_file_object['a']
        self.aaaa = self.zone_file_object['aaaa']
        self.ns = self.zone_file_object['ns']
        self.cname = self.zone_file_object['cname']

import os
import json
from configs import ZONES_DIRECTORY
from time import time


class ZoneController:
    def add_message_to_zone(self, message):
        for answer in message.answers:
            name = self.join_name(answer.names)
            _name, content = self.get_zone(name)
            content = json.loads(content)
            type = answer.qtype
            content['name'] = name
            data = answer.resourse_data

            if 'types' in content:
                types = content['types']
            else:
                types = dict()
            now = time() * 1000
            if type == 'A':
                self.add_line('A', now, types, answer, data)
            if type == 'AAAA':
                self.add_line('AAAA', now, types, answer, data)
            if type == 'PTR':
                self.add_line('PTR', now, types, answer, data)
            if type == 'NS':
                self.add_line('NS', now, types, answer, data)
            content['types'] = types

            self.write_zone(_name, content)

    def rewrite_type(self, name, qtype, records):
        name = name.replace(".", "-")
        _name, content = self.get_zone(name)
        content = json.loads(content)
        content['types'][qtype] = records
        self.write_zone(_name, content)

    def clear_cash_by_type(self, name, qtype, now):
        record = self.get_record(name, qtype)
        to_remove = []
        for e in record:
            if e[2] + e[1] <= now:
                to_remove.append(e)
        for e in to_remove:
            record.remove(e)
        print(record)
        self.rewrite_type(name, qtype, record)

    def add_line(self, t, now, types, answer, data):
        if t in types:
            typess = types[t]
            types.pop(t)
        else:
            typess = list()

        ttl = answer.ttl
        res = []
        for e in typess:
            res.append(tuple(e))
        typess = res
        to_remove = None
        for e in typess:
            if e[0] == data:
                to_remove = e

        if to_remove:
            typess.remove(to_remove)
        typess.append((data, ttl, now))
        types[t] = typess

    def write_zone(self, name, content):
        with open(name, 'w') as f:
            f.write(json.dumps(content))

    def has_zone(self, name):
        name = name.replace(".", "-")
        for file in os.listdir(f"{ZONES_DIRECTORY}"):
            if file == f'{name}.json':
                return True
        return False

    def has_value(self, zone_name, t):
        if not self.has_zone(zone_name):
            return False
        zone = json.loads(self.get_zone(zone_name)[1])
        if 'types' not in zone:
            return False
        if t not in zone['types']:
            return False
        return len(zone['types'][t]) > 0

    def has_record(self, zone_name, t):
        if not self.has_zone(zone_name):
            return False
        return self.has_value(zone_name, t)

    def get_record(self, zone_name, t):
        zone = json.loads(self.get_zone(zone_name)[1])
        return zone['types'][t]

    def get_zone(self, name):
        name = name.replace(".", "-")
        for file in os.listdir(f"{ZONES_DIRECTORY}"):
            if file == f'{name}.json':
                with open(f'{ZONES_DIRECTORY}/{name}.json') as f:
                    content = f.read()
                return f'{ZONES_DIRECTORY}/{name}.json', content

        with open(f'{ZONES_DIRECTORY}/{name}.json', 'w') as f:
            f.write('{}')
            return f'{ZONES_DIRECTORY}/{name}.json', '{}'

    def join_name(self, name):
        res = []
        for e in name:
            st = ''
            for i in e:
                st += chr(i)
            res.append(st)

        return '.'.join(res)

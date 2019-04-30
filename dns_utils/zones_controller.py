import os
import json
from configs import ZONES_DIRECTORY


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

            if type == 'A':
                self.add_line('A', types, answer, data)
            if type == 'AAAA':
                self.add_line('AAAA', types, answer, data)
            if type == 'CNAME':
                self.add_line('CNAME', types, answer, data)
            if type == 'NS':
                self.add_line('NS', types, answer, data)
            content['types'] = types

            self.write_zone(_name, content)

    def add_line(self, t, types, answer, data):
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
        if (data, ttl) in typess:
            typess.remove((data, ttl))
        typess.append((data, ttl))
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
        return t in zone['types']

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

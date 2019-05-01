from dns.dns_message import DNSMessage
from network.dns_forwarder import DNSForwarder
from dns_utils.zones_controller import ZoneController
from dns_utils.cash_controller import CashController
from configs import ROOT_DNS_IP, ROOT_DNS_PORT
from time import time


class DNSController:
    def run(self, message):
        dns_message = DNSMessage()
        dns_message.parse_message(message)

        zone_controller = ZoneController()
        cash_controller = CashController()
        for question in dns_message.questions:
            now = time() * 1000
            name = self.join_name(question.names)
            qtype = question.qtype
            if cash_controller.has_dns_cash_record(name, qtype, now):
                cash = cash_controller.get_dns_cash_records(self.join_name(question.names), question.qtype)
                print('LOADED FROM CASH')
                s = dns_message.format_message(cash, dns_message.message)
                return s

        print(f'LOADED FROM {(ROOT_DNS_IP, ROOT_DNS_PORT)}')
        root_dns = DNSForwarder()

        root_answer = root_dns.transit(message)

        root_dns_message = DNSMessage()
        mess = root_dns_message.parse_message(root_answer)

        zone_controller.add_message_to_zone(mess)

        return root_answer

    def join_name(self, name):
        res = []
        for e in name:
            st = ''
            for i in e:
                st += chr(i)
            res.append(st)

        return '.'.join(res)

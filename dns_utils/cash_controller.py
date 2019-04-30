from dns_utils.dns_cash_record import DNSCashRecord
from dns_utils.zones_controller import ZoneController


class CashController:
    def __init__(self):
        self.zones_controller = ZoneController()

    def has_dns_cash_record(self, name, qtype, now):
        if self.zones_controller.has_value(name, qtype):
            self.zones_controller.clear_cash_by_type(name, qtype, now)
            return self.zones_controller.has_value(name, qtype)
        return False

    def get_dns_cash_records(self, name: str, qtype: str):
        records = self.zones_controller.get_record(name, qtype)
        res = []
        for record in records:
            res.append(DNSCashRecord(name, qtype, 'IN', record[1], record[0]))

        return res

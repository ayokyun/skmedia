from pymodbus.client.sync import ModbusTcpClient


class UEMD(object):
    def __init__(self, host: str, port: int = 502, timeout: int = 3):
        self.host = host
        self.port = port
        self.timeout = timeout

    def is_connectable(self):
        self.client = ModbusTcpClient(
            host=self.host,
            port=self.port,
            timeout=self.timeout
        )
        ret = self.client.connect()
        self.client.close()
        return ret

    def show(self):
        r = self.client.read_holding_registers(0, count=2)
        print(r)

    def __del__(self):
        self.client.close()


if __name__ == '__main__':
    uemd = UEMD('127.0.0.1')

    uemd.is_connectable()

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


class UEMD(object):
    def __init__(self, host: str, port: int = 502, timeout: int = 3):
        self.client = ModbusTcpClient(
            host=host,
            port=port,
            timeout=timeout
        )

    def is_connectable(self):

        ret = self.client.connect()
        self.client.close()
        return ret

    def show(self):
        print(self.client)

        r = self.client.read_holding_registers(0, count=2)
        print(r.registers)

    def get_data(self):
        # print(self.is_connectable())

        result = self.client.read_holding_registers(0, count=2)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers,
                                                     byteorder=Endian.Little,
                                                     wordorder=Endian.Little)

        return decoder.decode_32bit_float()

    def __del__(self):
        self.client.close()


class Protocol:

    response_protocol = {"header": {"idx": 0, "length": 2},
                         "stationId": {"idx": 2, "length": 1},
                         "solarVoltage1": {"idx": 3, "length": 2, "devide": 10},
                         "solarCurrent": {"idx": 5, "length": 2, "devide": 10},
                         "solarVoltage2": {"idx": 7, "length": 2, "devide": 10},
                         "lineVoltage": {"idx": 9, "length": 2, "devide": 10},
                         "lineCurrent": {"idx": 11, "length": 2, "devide": 10},
                         "temperature": {"idx": 13, "length": 2, "devide": 10},
                         "energyToday": {"idx": 15, "length": 2, "devide": 100},
                         "energyTotal": {"idx": 17, "length": 3},
                         "faultCode": {"idx": 20, "length": 4},
                         "runStatus": {"idx": 24, "length": 1},
                         "frequency": {"idx": 25, "length": 2, "devide": 10},
                         "operationTime": {"idx": 27, "length": 2},
                         "powerFactor": {"idx": 29, "length": 1, "devide": 100},
                         "dspVersion": {"idx": 30, "length": 1, "devide": 10},
                         "checkSum": {"idx": 31, "length": 1}
                         }


if __name__ == '__main__':
    uemd = UEMD('127.0.0.1')

    uemd.is_connectable()
    uemd.show()

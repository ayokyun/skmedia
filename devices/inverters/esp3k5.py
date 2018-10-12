from pprint import pprint
import serial
import collections


class Helper:

    @staticmethod
    def bytes_to_int(_bytes):
        if type(_bytes) == bytearray or type(_bytes) == bytes:
            return int.from_bytes(_bytes, byteorder='little', signed=False)
        elif type(_bytes) == int:
            return _bytes

    @staticmethod
    def calculate_checksum(data):
        result = 0
        for x in data:
            result = result ^ x

        return result

    @staticmethod
    def get_data_from_bytes(raw_data, protocol):
        print(raw_data, protocol)
        data = raw_data[protocol['idx']:protocol['idx'] + protocol['length']]

        data = int.from_bytes(data, byteorder='little', signed=False)
        if protocol['devide']:
            data /=  protocol['devide']
        return data


class Esp3k5(object):

    def __init__(self, station_id: int):
        if station_id <= 0 or station_id > 99:
            raise ValueError
        self.station_id: int = station_id
        self.data = None

    def update_data(self, data):
        # self.get_rawdata()
        return True
        # return True  # 성공 시

        # return False  # 실패 시

    def get_rawdata(self, port: str, baudRate: int, timeout=0.1):

        with serial.Serial(port, baudRate, timeout=0.1) as ser:
            ser.write(self.make_request())
            line = ser.readline()  # read a '\n' terminated line
            return line

    def make_request(self):
        protocol = Protocol
        request_protocol = Protocol.request_protocol

        ret = bytearray(protocol.request_format)
        ret[request_protocol['stationId']['idx']] = self.station_id
        ret[request_protocol['checkSum']['idx']] = (
            ret[2] + ret[3] + ret[4]) % 256
        return bytes(ret)

    def verify_response(self, data):
        # protocol = Protocol
        # resIdx = protocol.response_index
        res_proto = Protocol.response_protocol

        # check Length
        if len(data) != 32:
            return False

        # check Header
        if (data[res_proto['header']['idx']] != 0xb1) \
                or (data[res_proto['header']['idx']+1] != 0xb7):
            return False

        # check ID
        if data[res_proto['stationId']['idx']] != self.station_id:
            return False

        # checkSum
        if data[res_proto['checkSum']['idx']] != Helper.calculate_checksum(data[0:-1]):
            return False
        return True

    def parse_response(self, data):
        # protocol = Protocol
        # resIdx = protocol.response_index

        parsed_data = dict()
        # parsed_data['solarVoltage1'] = 360.5
        # # parsed_data['solarVoltage1'] = Helper.bytes_to_int((data[3:5]))
        # parsed_data['solarCurrent'] = Helper.bytes_to_int(data[5:7])
        # parsed_data['solarVoltage2'] = Helper.bytes_to_int(data[7:9])
        # parsed_data['lineVoltage'] = Helper.bytes_to_int(data[9:11])
        # parsed_data['lineCurrent'] = Helper.bytes_to_int(data[11:13])
        # parsed_data['temperature'] = Helper.bytes_to_int(data[13:15])
        # parsed_data['energyToday'] = Helper.bytes_to_int(data[15:16])
        # parsed_data['energyTotal'] = Helper.bytes_to_int(data[17:20])
        # parsed_data['faultCode'] = Helper.bytes_to_int(data[20:24])
        # parsed_data['runStatus'] = Helper.bytes_to_int(data[24])
        # parsed_data['frequency'] = Helper.bytes_to_int(
        #     data[resIdx.frequency.idx: resIdx.frequency.idx+resIdx.frequency.length])
        # parsed_data['operationTime'] = Helper.bytes_to_int(data[24])
        # parsed_data['powerFactor'] = Helper.bytes_to_int(data[24])
        # parsed_data['DSPVersion'] = Helper.bytes_to_int(data[24])
        # # pprint(parsed_data)
        self.data = parsed_data

        return True

    def __del__(self):
        pass


class Protocol:
    di = collections.namedtuple("dataInfo", "idx length")
    request_format = [0x0a, 0x96, 0xFF, 0x54, 0x18, 0x05, 0xFF]

    request_protocol = {"header": {"idx": 0, "length": 2},
                        "stationId": {"idx": 2, "length": 1},
                        "command": {"idx": 3, "length": 1},
                        "length": {"idx": 4, "length": 1},
                        "tail": {"idx": 5, "length": 1},
                        "checkSum": {"idx": 6, "length": 1},
                        }

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

    import esp3k5_dummy

    data = esp3k5_dummy.makeDummyData()

    esp = Esp3k5(1)
    # esp.request()  # not Implement
    esp.parse_response(data)

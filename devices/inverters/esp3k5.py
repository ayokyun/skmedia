from pprint import pprint
import struct


class Esp3k5(object):

    queryFormat = [0x0a, 0x96, 0xFF, 0x54, 0x18, 0x05, 0xFF]

    def __init__(self, stationId: int):
        self.stationId: int = stationId
        self.rawData = None
        self.data = None

    @staticmethod
    def bytes2int(_bytes):
        if type(_bytes) == bytearray or type(_bytes) == bytes:
            return int.from_bytes(_bytes, byteorder='little', signed=False)
        elif type(_bytes) == int:
            return _bytes

    def request(self):
        print("request :: 아직 미구현")
        # raise NotImplementedError

    def makeQuery(self):
        ret = bytearray(self.queryFormat)
        ret[2] = self.stationId
        ret[6] = (ret[2] + ret[3] + ret[4] )% 256
        return bytes(ret)

    def verifyResponse(self, data):
        print("verifyResponse :: 아직 미구현")
        return True

    def parseResponse(self, data):
        if self.verifyResponse(data):
            rawData = dict()
            rawData['solarVoltage1'] = self.bytes2int(data[3:5])
            rawData['solarVoltage2'] = self.bytes2int(data[7:9])
            rawData['solarCurrent'] = self.bytes2int(data[5:7])
            rawData['lineVoltage'] = self.bytes2int(data[9:11])
            rawData['lineCurrent'] = self.bytes2int(data[11:13])
            rawData['temperature'] = self.bytes2int(data[13:15])
            rawData['energyToday'] = self.bytes2int(data[15:16])
            rawData['energyTotal'] = self.bytes2int(data[17:20])
            rawData['faultCode'] = self.bytes2int(data[20:24])
            rawData['runStatus'] = self.bytes2int(data[24])
            pprint(rawData)
            self.rawData = rawData
        else:
            print("vertify Error ")

    def getUIvalue(self):
        # data = {}
        pass
        # return self.data

    def __del__(self):
        pass


if __name__ == '__main__':

    import esp3k5_dummy

    data = esp3k5_dummy.makeDummyData()

    esp = Esp3k5(1)
    esp.request()  # not Implement
    esp.parseResponse(data)

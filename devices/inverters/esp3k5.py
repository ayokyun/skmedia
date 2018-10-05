from pprint import pprint


class Esp3k5(object):
    def __init__(self, sectionId):
        self.sectionId = sectionId
        self.rawData = None
        self.data = None

    @staticmethod
    def bytes2int(b):
        if type(b) == bytearray:
            return int.from_bytes(b, byteorder='little', signed=False)
        elif type(b) == int:
            return b

    def request(self):
        print("request :: 아직 미구현")
        # raise NotImplementedError

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
        data = {}
        # return self.data

    def __del__(self):
        pass


if __name__ == '__main__':

    def makeDummyData():
        """ ESP3K5 프로토콜 예시에 맞춘 더미데이터 생성 

        return bytearray """
        dummy = []
        # Header
        dummy.extend([0xb1, 0xb7])
        # Section Id
        dummy.extend([0x01])
        # SolarVoltage~EnergyToday
        dummy.extend([0x15, 0x0e, 0x05, 0x01, 0x01, 0x0e, 0x9a,
                      0x08, 0xc8, 0x01, 0x60, 0x01, 0xff, 0x00])
        # EnergyTotal~DataCheck
        dummy.extend([0x9f, 0x86, 0x01, 0x00, 0x00, 0x00, 0x00,
                      0x01, 0x59, 0x02, 0x01, 0x01, 0x63, 0x6e, 0x9d])

        dummyArray = bytearray(dummy)
        # print("dummy Array : ", dummyArray)
        return dummyArray

    data = makeDummyData()

    esp = Esp3k5(1)
    esp.request()  # not Implement
    esp.parseResponse(data)

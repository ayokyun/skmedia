import pytest

import unittest
from devices.inverters import esp3k5


class Esp3k5(unittest.TestCase):

    def setUp(self):
        self.stationId = 1
        self.esp3k5 = esp3k5.Esp3k5(self.stationId)

    def tearDown(self):
        pass

    def test_import_esp3k5(self):
        """ 테스트 파일이 import 되었는지 확인 """
        self.assertIsInstance(self.esp3k5, esp3k5.Esp3k5)

    def test_exist_make_query_function(self):
        """ make query test """
        result = self.esp3k5.makeQuery()

        self.assertEqual(type(result), bytes)  # check Type
        self.assertEqual(len(result), 7)  # check Length
        assert result[0] == 0x0a and result[1] == 0x96  # check Header
        assert result[2] == self.stationId  # Station Id
        assert result[3] == 0x54  # command
        assert result[4] == 0x18  # length
        assert result[5] == 0x05  # tail
        assert result[6] == (result[2] + result[3] +
                             result[4]) % 256  # checkSum

    def test_get_rawData(self):
        ret = self.esp3k5.getRawData()
        self.assertEqual(type(ret), bytes)  # check Type
        self.assertEqual(len(ret), 32)  # check Length

    def test_update_data(self):
        self.esp3k5.updateData()


class VerifyRawData(unittest.TestCase):

    def setUp(self):
        self.stationId = 1
        self.esp3k5 = esp3k5.Esp3k5(self.stationId)
        self.rawData = bytearray([0xB1, 0xB7, 0x01, 0x15, 0x0E,
                                  0x05, 0x01, 0x01, 0x0E, 0x9A,
                                  0x08, 0xC8, 0x01, 0x60, 0x01,
                                  0xFF, 0x00, 0x9F, 0x86, 0x01,
                                  0x00, 0x00, 0x00, 0x00, 0x01,
                                  0x59, 0x02, 0x01, 0x01, 0x63,
                                  0x6E, 0x69])

    def test_return_type_is_bool(self):
        returnValue = self.esp3k5.verifyRawData(self.rawData)
        self.assertEqual(type(returnValue), type(True))

    def test_check_header(self):
        self.assertTrue(self.esp3k5.verifyRawData(bytearray(self.rawData)))


if __name__ == '__main__':
    unittest.main()

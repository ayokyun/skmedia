import pytest
import unittest

from devices.inverters import esp3k5


class UtilsTest(unittest.TestCase):
    utils = esp3k5.Utils
    protocol = esp3k5.Protocol
    rawData = bytearray([0xB1, 0xB7, 0x01, 0x15, 0x0E,
                         0x05, 0x01, 0x01, 0x0E, 0x9A,
                         0x08, 0xC8, 0x01, 0x60, 0x01,
                         0xFF, 0x00, 0x9F, 0x86, 0x01,
                         0x00, 0x00, 0x00, 0x00, 0x01,
                         0x59, 0x02, 0x01, 0x01, 0x63,
                         0x6E, 0x9D])

    def test_calculate_checksum(self):
        """ return type is bool """
        ret = self.utils.calculate_checksum(self.rawData[:-1])
        self.assertEqual(ret, 0x9d)

    # @unittest.
    def test_get_data_from_bytes(self):
        """ get data from bytes """

        protocol = self.protocol.response_protocol["energyTotal"]
        ret = self.utils.get_data_from_bytes(self.rawData, protocol)
        self.assertEqual(ret, 99999)

        protocol = self.protocol.response_protocol["solarVoltage1"]
        ret = self.utils.get_data_from_bytes(self.rawData, protocol)
        self.assertEqual(ret, 360.5)


class Esp3k5Test(unittest.TestCase):

    def setUp(self):
        self.station_id = 1
        self.esp3k5 = esp3k5.Esp3k5(self.station_id)

    def tearDown(self):
        pass

    def test_is_instance_esp3k5(self):
        """ self.esp3k5 is esp3k5.Esp3k5's Instance """
        self.assertIsInstance(self.esp3k5, esp3k5.Esp3k5)

    def test_station_id_range(self):
        """station Id range is 0 ~ 99 """
        with self.assertRaises(ValueError):
            esp3k5.Esp3k5(-1)
        with self.assertRaises(ValueError):
            esp3k5.Esp3k5(100)

        valid_station_id = 0
        esp3k5_instance = esp3k5.Esp3k5(valid_station_id)
        self.assertEqual(esp3k5_instance.station_id, valid_station_id)

        valid_station_id = 99
        esp3k5_instance = esp3k5.Esp3k5(valid_station_id)
        self.assertEqual(esp3k5_instance.station_id, valid_station_id)

    def test_make_request_function(self):
        """ make query test """
        result = self.esp3k5.make_request()

        self.assertEqual(type(result), bytes)  # check Type
        self.assertEqual(len(result), 7)  # check Length
        assert result[0] == 0x0a and result[1] == 0x96  # check Header
        assert result[2] == self.station_id  # Station Id
        assert result[3] == 0x54  # command
        assert result[4] == 0x18  # length
        assert result[5] == 0x05  # tail
        assert result[6] == (result[2] + result[3] +
                             result[4]) % 256  # checkSum


# @unittest.skip("")
class VerifyResponseTest(unittest.TestCase):

    def setUp(self):
        self.station_id = 1
        self.esp3k5 = esp3k5.Esp3k5(self.station_id)
        self.rawData = bytearray([0xB1, 0xB7, 0x01, 0x15, 0x0E,
                                  0x05, 0x01, 0x01, 0x0E, 0x9A,
                                  0x08, 0xC8, 0x01, 0x60, 0x01,
                                  0xFF, 0x00, 0x9F, 0x86, 0x01,
                                  0x00, 0x00, 0x00, 0x00, 0x01,
                                  0x59, 0x02, 0x01, 0x01, 0x63,
                                  0x6E, 0x9D])

    def test_return_type_is_bool(self):
        """ return type is bool """
        returnValue = self.esp3k5.verify_response(self.rawData)
        self.assertEqual(type(returnValue), type(True))

    def test_check_header(self):
        """ header is 0xb1b7 """
        correctData = self.rawData
        self.assertTrue(self.esp3k5.verify_response(correctData))

        invalidData = self.rawData
        invalidData[0] += 1
        self.assertFalse(self.esp3k5.verify_response(invalidData))

        invalidData = correctData
        invalidData[1] -= 1
        self.assertFalse(self.esp3k5.verify_response(invalidData))

    def test_check_length(self):
        """ length is 32 """
        correctData = self.rawData
        self.assertTrue(self.esp3k5.verify_response(correctData))

        invalidData = correctData[:-1]  # remove last byte
        self.assertFalse(self.esp3k5.verify_response(invalidData))

    def test_station_id(self):
        """ data[2] is stationid """
        correctData = self.rawData
        self.assertTrue(self.esp3k5.verify_response(correctData))

        invalidData = self.rawData
        invalidData[2] += 1
        self.assertFalse(self.esp3k5.verify_response(invalidData))

    def test_checksum(self):
        """ checksum is data[0] ~ data[31] xor calculate 
        (and process for overflow)  """
        correctData = self.rawData
        self.assertTrue(self.esp3k5.verify_response(correctData))

        invalidData = self.rawData
        invalidData[31] += 1
        self.assertFalse(self.esp3k5.verify_response(invalidData))


class ParseDataTest(unittest.TestCase):

    def setUp(self):
        self.station_id = 1
        self.esp3k5 = esp3k5.Esp3k5(self.station_id)
        self.rawData = bytearray([0xB1, 0xB7, 0x01, 0x15, 0x0E,
                                  0x05, 0x01, 0x01, 0x0E, 0x9A,
                                  0x08, 0xC8, 0x01, 0x60, 0x01,
                                  0xFF, 0x00, 0x9F, 0x86, 0x01,
                                  0x00, 0x00, 0x00, 0x00, 0x01,
                                  0x59, 0x02, 0x01, 0x01, 0x63,
                                  0x6E, 0x9D])

    def test_get_rawData(self):
        ret = self.esp3k5.get_rawdata("COM8", 9600)
        self.assertEqual(type(ret), bytes)  # check Type
        self.assertEqual(len(ret), 32)  # check Length

    # @unittest.skip("dd")
    def test_parse_response(self):
        self.assertIsNotNone(self.esp3k5.parse_response(self.rawData))
        self.assertEqual(self.esp3k5.data["solarVoltage1"], 360.5)

    def test_update(self):
        self.esp3k5.update()

        self.assertEqual(self.esp3k5.data["solarVoltage1"], 360.5)


if __name__ == '__main__':
    unittest.main()

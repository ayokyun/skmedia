import pytest

import unittest
# from types import ModuleType,
# import inspect
import esp3k5


class Test(unittest.TestCase):

    def setUp(self):
        self.stationId = 255
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


if __name__ == '__main__':
    unittest.main()

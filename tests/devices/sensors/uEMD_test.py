import unittest
from devices.sensors import uEMD


class Main(unittest.TestCase):

    # Connetion Success and failure testing
    def test_connection_success(self):
        valid_param = {"host": '127.0.0.1', 'port': 502}

        self.uemd = uEMD.UEMD(
            host=valid_param['host'],
            port=valid_param['port']
        )
        self.assertTrue(self.uemd.is_connectable())

    def test_connect_failure(self):
        invalid_param = {"host": '128.0.0.1', 'port': 502}

        self.uemd = uEMD.UEMD(
            host=invalid_param['host'],
            port=invalid_param['port'],
            timeout=1
        )
        self.assertFalse(self.uemd.is_connectable())


if __name__ == '__main__':

    unittest.main()

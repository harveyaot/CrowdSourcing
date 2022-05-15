import unittest
import configparser
from configparser import ExtendedInterpolation

class TestConfig(unittest.TestCase):

    def test_build(self):
        config = configparser.ConfigParser(interpolation=ExtendedInterpolation())
        config.read('config/test.ini')
        config.getint('mongodb', 'port')
        self.assertEqual(config['global']['env'], "test", "Should be test")
        self.assertEqual(config['mongodb']['db'], "test", "Should be test")
        self.assertEqual(config['mongodb']['port'], "27017", "Should be 27017")
        self.assertEqual(config.getint('mongodb', 'port'), 27017, "Should be 27017")

if __name__ == '__main__':
    unittest.main()
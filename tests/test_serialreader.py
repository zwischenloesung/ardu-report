
import unittest2 as unittest
import json
import serial

from libardurep import datastore, serialreader

class TestSerialReader(unittest.TestCase):
    def setUp(self):
        self.store = datastore.DataStore()
        self.reader = serialreader.SerialReader(None, 9600, self.store, 20)
        self.reader.device_name = "loop://"
        s = serial.serial_for_url("loop://", timeout=5)
        self.reader.device = s

    def test_timeout(self):
        # we can not really test the actual timeout of the real serial
        # connection as we have a serial dummy here, but we can test
        # whether readline() timeouts on the dummy and if run() terminats
        # even if no '\n' is received..
        j = 'df'
        self.reader.device.write(j)
        self.reader.run()

    def test_single_run(self):
        j = ' \n\n[ \n  {"name":"light_value","value":"777"} \n] \n'
        self.reader.device.write(j)
        self.reader.run()
        self.assertEqual("777", self.store.data["light_value"]["value"])


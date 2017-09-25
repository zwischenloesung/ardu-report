
import unittest2 as unittest
import json
import serial

from libardurep import datastore, serialreader

class TestSerialReader(unittest.TestCase):
    def setUp(self):
        self.store = datastore.DataStore()
        self.reader = serialreader.SerialReader(None, 9600, self.store, 2)
        self.reader.device_name = "loop://"
        s = serial.serial_for_url("loop://", timeout=5)
        self.reader.device = s
        

    def test_single_run(self):
        j = ' \n\n[ \n  {"name":"light_value","value":"777"} \n] \n'
        self.reader.device.write(j)
        self.reader.run()
        self.assertEqual("777", self.store.data["light_value"]["value"])


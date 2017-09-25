
import unittest2 as unittest
import json
import serial
import time

from libardurep import datastore, serialreader

class TestSerialReader(unittest.TestCase):
    def setUp(self):
        self.store = datastore.DataStore()
        self.reader = serialreader.SerialReader(None, 9600, self.store, 20)
        self.reader.device_name = "loop://"
        self.reader.device = serial.serial_for_url("loop://", timeout=5)
        self.test_json = ' \n\n[ \n  {"name":"light_value","value":"777"} \n] \n'

    def test_timeout(self):
        # we can not really test the actual timeout of the real serial
        # connection as we have a serial dummy here, but we can test
        # whether readline() timeouts on the dummy and if run() terminats
        # even if no '\n' is received..
        j = 'df'
        self.reader.device.write(j)
        self.reader.run()

    def test_single_run(self):
        self.reader.device.write(self.test_json)
        self.reader.run()
        self.assertEqual("777", self.store.data["light_value"]["value"])

    def test_single_thread(self):
        self.reader.start()
        self.assertTrue(self.reader.is_alive())
        self.reader.halt()
        time.sleep(2)
        self.assertFalse(self.reader.is_alive())



import unittest2 as unittest
import datetime
import json
import re

from libardurep import datastore, datareporter

class TestDataReport(unittest.TestCase):
    def setUp(self):
        self.store = datastore.DataStore()
        self.reporter = datareporter.DataReporter(self.store)

    def test_log(self):
#        self.reporter.log()
        pass


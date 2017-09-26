
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
        # this is tested in the actual log_*() respectively
        pass

    def test_log_stdout(self):
        # this is tested anyway in self.store.get_text()
        pass

    def test_log_file(self):
        import tempfile
        self.store.register_json('[{"name":"foo"}]')

        tf = tempfile.NamedTemporaryFile()

        self.reporter.log_file("file:///" + tf.name)
        with open(tf.name, "r") as fh:
            fc = fh.read()
        sc = self.store.get_json_tuples(True)

        self.assertEqual(sc, fc)

        self.reporter.log_file("file:///" + tf.name)
        with open(tf.name, "r") as fh:
            fc = fh.read()

        self.assertEqual(sc + sc, fc)

    def test_log_post(self):
        # Create a local http server? ...
        pass

    def test_log_ssh(self):
        # not implemented yet
        pass



import unittest2 as unittest
import json

from libardurep import datastore

class TestDataStore(unittest.TestCase):
    def setUp(self):
        self.store = datastore.DataStore()

    def test_register_json(self):
        j = '[ {"name":"light_value","value":"777"} ]'
        j_son = json.loads(j)

        self.store.register_json(j)

        self.assertEqual(j_son[0], self.store.data["light_value"])


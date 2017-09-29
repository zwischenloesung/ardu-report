"""
MODULE:       datastore
PURPOSE:      store sensor data sets
AUTHOR(S):    michael lustenberger inofix.ch
COPYRIGHT:    (C) 2017 by Michael Lustenberger and the INOFIX GmbH

              This program is free software under the GNU General Public
              License (v3).
"""

import datetime
import json

class DataStore(object):
    """
    This store is used to collect sensor data as separate tuples
    per sensor. Newer data overwrites older data and incomplete
    runs will eventually accumulate to full sets over time.
    """

    def __init__(self, in_schema=None, in_meta_schema=None, \
                        out_schema=None, out_meta_schema=None):
        # prepare a timestamp to remember the last data update
        self.last_data_timestamp = None
        # prepare a dict to store the data
        # this way we can wait for a stable set of values
        self.data = {}
        # define the default keywords
        ## mandatory
        self.id_key = "id"
        self.value_key = "value"
        ## optional but well known
        self.unit_key = "unit"
        self.threshold_key = "threshold"
        ## special time keys
        ### report time
        self.time_key = "time"
        ### if sensor transmits a timestamp
        self.sensor_time_key = "timestamp"
        ## the whole well known as an "input: output" map...
        self.well_now_keys = {
            self.id_key: self.id_key,
            self.value_key: self.value_key,
            self.unit_key: self.unit_key,
            self.threshold_key: self.threshold_key,
            self.time_key: self.sensor_time_key
        }
        ## the rest to be set based on the schema files
        self.other_keys = {}

    def register_json(self, data):
        """
        Register the contents as JSON
        """
        j = json.loads(data)
        self.last_data_timestamp = \
                datetime.datetime.utcnow().replace(microsecond=0).isoformat()

        try:
            for v in j:
                # prepare the sensor entry container
                self.data[v[self.id_key]] = {}
                # add the mandatory entries
                self.data[v[self.id_key]][self.id_key] = \
                                            v[self.id_key]
                self.data[v[self.id_key]][self.value_key] = \
                                            v[self.value_key]
                # add the time the data was received
                self.data[v[self.id_key]][self.time_key] = \
                                            self.last_data_timestamp
                # add the optional well known entries if provided
                if v.has_key(self.unit_key):
                    self.data[v[self.id_key]][self.unit_key] = \
                                            v[self.unit_key]
                if v.has_key(self.threshold_key):
                    self.data[v[self.id_key]][self.threshold_key] = \
                                            v[self.threshold_key]
                for k in self.other_keys:
                    if v.has_key(k):
                        self.data[v[self.id_key]][k] = v[k]
        except KeyError as e:
            print "The main key was not found on the serial input line: " + \
                    str(e)
        except ValueError as e:
            print "No valid JSON string received. Waiting for the next turn."
            print "The error was: " + str(e)

    def get_text(self):
        """
        Get the data in text form (i.e. human readable)
        """
        t = "==== " + str(self.last_data_timestamp) + " ====\n"
        for k in self.data:
            t += k + " " + str(self.data[k][self.value_key])
            u = ""
            if self.data[k].has_key(self.unit_key):
                u = self.data[k][self.unit_key]
                t += u
            if self.data[k].has_key(self.threshold_key):
                if (self.data[k][self.threshold_key] < \
                                    self.data[k][self.value_key]):
                    t += " !Warning: Value is over threshold: " + \
                                str(self.data[k][self.threshold_key]) + "!"
                else:
                    t += " (" + str(self.data[k][self.threshold_key]) + u + ")"
            for l in self.other_keys:
                if self.data[k].has_key(l):
                    t += " " + self.data[k][l]
            t += "\n"
        return t

    def get_json(self, prettyprint=False):
        """
        Get the data in JSON form
        """
        j = []
        for k in self.data:
            j.append(self.data[k])
        if prettyprint:
            j = json.dumps(j, indent=2, separators=(',',': '))
        else:
            j = json.dumps(j)
        return j

    def get_json_tuples(self, prettyprint=False):
        """
        Get the data as JSON tuples
        """
        j = self.get_json(prettyprint)
        if len(j) > 2:
            if prettyprint:
                j = j[1:-2] + ",\n"
            else:
                j = j[1:-1] + ","
        else:
            j = ""
        return j


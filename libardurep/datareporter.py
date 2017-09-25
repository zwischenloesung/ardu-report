"""
MODULE:       datareporter
PURPOSE:      get the date from the store and report it.
AUTHOR(S):    michael lustenberger inofix.ch
COPYRIGHT:    (C) 2017 by Michael Lustenberger and INOFIX GmbH

              This program is free software under the GNU General Public
              License (v3).
"""

import datetime
import json

class DataReporter(object):
    """
    This class has a data store associated and reports the data
    to a given URL on request.
    """

    def __init__(self, store):
        """
        Initialize the reporter.
            store store         the data store
        """
        self.store = store



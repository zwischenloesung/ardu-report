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

    def __init__(self, store, url="", credentials={}, do_verify_certificate=True):
        """
        Initialize the reporter.
            store store         the data store
        """
        self.store = store
        # for commodity, either register url etc. or choose every time
        self.url = url
        self.credentials = credentials
        self.do_verify_certificate = do_verify_certificate

    def log(self, url=None, credentials=None, do_verify_certificate=None):
        """
        Wrapper for the other log methods, decide which one based on the
        URL parameter.
        """
        if url is None:
            url = self.url
        if re.match("file://", url):
            log_file(url)
        elif re.match("https://", url) or re.match("http://", url):
            log_post(url, credentials, do_verify_certificate)
        else:
            log_stdout()

    def log_stdout(self):
        """
        Write to standard output
        """
        print self.store.get_text()

    def log_file(self, url=None):
        """
        Write to a local log file
        """
        if url is None:
            url = self.url
        f = re.sub("file://", "", url)
        try:
            with open(f, "w") as of:
                of.write(str(self.data))
        except IOError as e:
            print e
            print "Could not write the content to the file.."

    def log_post(self, url=None, credentials=None, do_verify_certificate=None):
        """
        Write to a remote host via HTTP POST
        """
        if url is None:
            url = self.url
        if credentials is None:
            credentials = self.credentials
        if do_verify_certificate is None:
            do_verify_certificate = self.do_verify_certificate
        if credentials and credentials.has_key("base64"):
            headers = {"Content-Type": "application/json", 'Authorization': 'Basic %s' % credentials["base64"]}
        else:
            headers = {"Content-Type": "application/json"}
        try:
            request = requests.post(url, headers=headers, data=self.data, verify=do_verify_certificate)
        except httplib.IncompleteRead as e:
            request = e.partial

    def log_ssh(self):
        """
        Write to a remote file via ssh
        """
        pass


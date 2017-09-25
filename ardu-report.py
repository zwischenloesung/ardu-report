#!/usr/bin/env python

"""
PURPOSE:      read the serial output of one or more arduino boards
              and store the sensor values..
DEPENDENCY:   python 2.7
PLATTFORM:    currently only unix/linux is supported
AUTHOR(S):    michael lustenberger inofix.ch
COPYRIGHT:    (C) 2017 by Michael Lustenberger and INOFIX GmbH

              This program is free software under the GNU General Public
              License (>=v2).
"""

#from libardurep import datastore, datareporter, serialreader
import argparse
import time
from libardurep import datastore, datareporter, serialreader


def standard_mode(args):
    """
    Helper function to run the reader for a certain amount of time
    """
    store = datastore.DataStore()
    reporter = datareporter.DataReporter(store, args.target, None, args.insecure)
    if args.password:
        pw = getpass.getpass()
    else:
        pw = None
    reporter.register_credentials(None, args.user, args.user_file, pw, args.password_file)

    reader = serialreader.SerialReader(args.device, args.baudrate, store, args.rounds)
    reader.start()
    time.sleep(args.seconds)
    reader.halt()
    reporter.log_stdout()

if __name__ == '__main__':
    """
    Main function used if started on the command line
    """
    cli_parser = argparse.ArgumentParser(description="Parse data from the arduino and use it for the Flussbad-Demo.")
    cli_parser.add_argument('-b', '--baudrate', default=9600, help='baud rate of the serial line')
    cli_parser.add_argument('-d', '--device', default='/dev/ttyACM0', help='serial device the arduino is connected to')
    cli_parser.add_argument('-i', '--interactive', action="store_true", help='prompt for control and log to stdout')
    cli_parser.add_argument('-I', '--insecure', default=False, action="store_true", help='do not verify certificate on HTTPS POST')
    cli_parser.add_argument('-p', '--password', action="store_true", help='prompt for a password')
    cli_parser.add_argument('-P', '--password_file', default='', help='load password from this file, containing the line: \'password: "my secret text"\'')
    cli_parser.add_argument('-r', '--rounds', type=int, default=0, help='how many times to run the serial listener thread (default: 0 / infinite)')
    cli_parser.add_argument('-s', '--seconds', type=int, default=10, help='how long to run if not in interacitve mode')
    cli_parser.add_argument('-t', '--target', default="", help='target log, where to report the data to. Default is empty for <stdout>, the following URLs are provided yet: "file:///..", "http://..", "https://.."')
    cli_parser.add_argument('-u', '--user', default='', help='user name')
    cli_parser.add_argument('-U', '--user_file', default='', help='load user name from this file, containing the line: \'user: "my_name"\'')

    args = cli_parser.parse_args()

    if args.interactive:
        pass
#        user_mode(args)
    else:
        standard_mode(args)


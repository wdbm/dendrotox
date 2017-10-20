#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# dendrotox_alert                                                              #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program sends an alert using the Tox communications network. If a       #
# contact is specified, that contact is added. If no contact is specified,     #
# then all available contacts are alerted.                                     #
#                                                                              #
# copyright (C) 2017 William Breaden Madden                                    #
#                                                                              #
# This software is released under the terms of the GNU General Public License  #
# version 3 (GPLv3).                                                           #
#                                                                              #
# This program is free software: you can redistribute it and/or modify it      #
# under the terms of the GNU General Public License as published by the Free   #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# This program is distributed in the hope that it will be useful, but WITHOUT  #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for     #
# more details.                                                                #
#                                                                              #
# For a copy of the GNU General Public License, see                            #
# <http://www.gnu.org/licenses/>.                                              #
#                                                                              #
################################################################################

usage:
    program [options]

options:
    -h, --help     display help message
    --version      display version and exit

    --contacts=ID  comma-delimited approved contacts  [default: none]
    --text=TEXT    text to send                       [default: alert]
"""

import docopt
import socket
import time

import dendrotox

name    = "dendrotox_alert"
version = "2017-10-20T0010Z"

def main(options):

    dendrotox.start_messaging(
        pause_time = 60
    )

    dendrotox.set_name(
        text = name + "-" + socket.gethostname()
    )

    if options["--contacts"] == "none":

        contacts = dendrotox.all_contacts()

    else:

        contacts = options["--contacts"].split(",")

        dendrotox.send_request(
            contacts = contacts
        )

    text = options["--text"]

    dendrotox.send_message(
        contacts = contacts,
        text     = text
    )

    time.sleep(30)

    dendrotox.stop_messaging()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)

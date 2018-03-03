#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# dendrotox_call_microphone                                                    #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program sends a micrphone call using the Tox communications network. If #
# a contact is specified, then that contact is added. If no contact is         #
# specified, then all available contacts are alerted.                          #
#                                                                              #
# copyright (C) 2018 William Breaden Madden                                    #
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
    -h, --help             display help message
    --version              display version and exit

    --contacts=ID          comma-delimited approved contacts  [default: all]
    --duration_record=INT  record duration (s)                [default: 10]
"""

import docopt
import socket
import time

import dendrotox

name    = "dendrotox_call_microphone"
version = "2018-03-02T0022Z"

def main(options):

    contacts        =     options["--contacts"]
    duration_record = int(options["--duration_record"])
    dendrotox.start_messaging(pause_time = 60)
    dendrotox.set_name(text = name + "@" + socket.gethostname())
    if contacts != "all": contacts = options["--contacts"].split(",")
    if contacts == "all": contacts = dendrotox.all_contacts()
    for contact in contacts:
        dendrotox.send_call(
            contact         = contact,
            record          = True,
            duration_record = duration_record
        )
    #dendrotox.stop_messaging()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)

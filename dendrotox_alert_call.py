#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# dendrotox_alert_call                                                         #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program sends a call alert using the Tox communications network. If a   #
# contact is specified, then that contact is added. If no contact is           #
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
    -h, --help     display help message
    --version      display version and exit

    --contacts=ID  comma-delimited approved contacts  [default: all]
    --text=TEXT    text to send                       [default: This is a test of the emergency broadcasting system.]
"""

import docopt
import socket
import time

import dendrotox

name    = "dendrotox_alert_call"
version = "2018-03-02T0004Z"

def main(options):

    contacts = options["--contacts"]
    text     = options["--text"]
    dendrotox.start_messaging(pause_time = 60)
    dendrotox.set_name(text = name + "@" + socket.gethostname())
    if contacts != "all": contacts = options["--contacts"].split(",")
    if contacts == "all": contacts = dendrotox.all_contacts()
    for contact in contacts:
        dendrotox.send_call_synthesized_speech(
            contact            = contact,
            text               = text,
            preference_program = "festival"
            #preference_program = "pico2wave"
            #preference_program = "espeak"
            #preference_program = "deep_throat.py"
        )
    #dendrotox.stop_messaging()

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)

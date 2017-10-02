#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# dendrotox_example_bot_print_last_message                                     #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is an example bot interface to Tox distributed communications.  #
# It is designed to display the last unseen message received.                  #
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
    -h, --help  display help message
    --version   display version and exit
"""

import docopt
import time

import dendrotox

name    = "dendrotox_example_bot_print_last_message"
version = "2017-10-02T2150Z"

def main(options):

    dendrotox.start_messaging()

    print("main program loop -- display all messages received")

    while True:

        message = dendrotox.last_received_message()

        if message:
            print(
                "\n"
                "timestamp: {timestamp}\n"
                "contact:   {contact}\n"
                "text:      {text}".format(
                timestamp = message.timestamp(),
                contact   = message.contact(),
                text      = message.text()
            ))

        time.sleep(0.3)

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)

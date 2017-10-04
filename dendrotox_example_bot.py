#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# dendrotox_example_bot                                                        #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is an example bot interface to Tox distributed communications.  #
# It is designed to parse various text inputs and offer responses and          #
# confirmations, and to perform actions based on those responses.              #
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
    -h, --help             display help message
    --version              display version and exit

    --approved_contact=ID  approved contact Tox ID           [default: none]
    --instance=ID          optional instance identification  [default: none]
"""

import docopt
import os
import sys
import time
import uuid

import dendrotox
import megaparsex

name    = "dendrotox_example_bot"
version = "2017-10-04T1521Z"

def main(options):

    global approved_contact
    if options["--approved_contact"] == "none":
        approved_contact = None
    else:
        approved_contact = options["--approved_contact"]

    global instance
    if options["--instance"] == "none":
        instance = str(uuid.uuid4())
    else:
        instance = options["--instance"]

    dendrotox.start_messaging()

    dendrotox.set_name(
        text = name
    )

    message = "ohai -- from {name}\n\n(instance: {instance})".format(
        name     = name,
        instance = instance
    )
    print("send startup message: {message}".format(message = message))

    if approved_contact:

        dendrotox.send_request(
            contact = approved_contact
        )

        dendrotox.send_message(
            contact = approved_contact,
            text    = message
        )

    else:

        dendrotox.send_message(
            contacts = dendrotox.all_contacts(),
            text     = message
        )

    while True:

        message = dendrotox.last_received_message(contact = approved_contact)

        try:

            if message:

                print("message received: {text}".format(text = message.text()))

                #response = megaparsex.parse(text = message.text())

                response = megaparsex.multiparse(
                    text         = message.text(),
                    parsers      = [megaparsex.parse, parse_networking],
                    help_message = "Does not compute. I can report my IP "
                                   "address, report on weather (METAR, TAF and "
                                   "rain reports for a specified ICAO airport "
                                   "code) and I can restart my script."
                )

                if type(response) is megaparsex.confirmation:

                    while response.confirmed() is None:

                        confirmation_response = dendrotox.get_input(
                            contact  = message.contact(),
                            prompt   = response.prompt()
                        )
                        response.test(text = confirmation_response)

                    if response.confirmed():

                        dendrotox.send_message(
                            contact = message.contact(),
                            text    = response.feedback()
                        )
                        response.run()

                    else:

                        dendrotox.send_message(
                            contact = message.contact(),
                            text    = response.feedback()
                        )

                elif type(response) is megaparsex.command:

                    command = dendrotox.get_input(
                        contact = message.contact(),
                        prompt  = response.prompt()
                    )

                    output = response.engage_command(
                        command    = command,
                        background = False
                    )

                    if output:

                        text = "output:\n{output}".format(output = output)
                        dendrotox.send_message(
                            contact = message.contact(),
                            text    = text
                        )

                elif response not in [None, False]:

                    print("message send: {text}".format(text = response))
                    dendrotox.send_message(
                        contact = message.contact(),
                        text    = response
                    )

        except:
        
            print("error")
            dendrotox.send_message(
                contact = message.contact(),
                text    = "error"
            )

        time.sleep(0.3)

def parse_networking(
    text = None
    ):

    triggers = []

    triggers.extend([
        megaparsex.trigger_keyphrases(
            text                          = text,
            keyphrases                    = [
                                            "reverse SSH",
                                            "reverse ssh"
                                            ],
            function                      = megaparsex.engage_command,
            kwargs                        = {"command": "ssh -R 10000:localhost:22 www.sern.ch"},
            confirm                       = True,
            confirmation_prompt           = "Do you want to reverse SSH "
                                            "connect? (y/n)",
            confirmation_feedback_confirm = "confirm reverse SSH connect",
            confirmation_feedback_deny    = "deny reverse SSH connect"
        )
    ])

    if any(triggers):

        responses = [response for response in triggers if response]

        if len(responses) > 1:

            return responses

        else:

            return responses[0]

    else:

        return False

if __name__ == "__main__":
    options = docopt.docopt(__doc__)
    if options["--version"]:
        print(version)
        exit()
    main(options)

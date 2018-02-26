# -*- coding: utf-8 -*-

"""
################################################################################
#                                                                              #
# dendrotox                                                                    #
#                                                                              #
################################################################################
#                                                                              #
# LICENCE INFORMATION                                                          #
#                                                                              #
# This program is an interface to Tox distributed communications.              #
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
"""

import datetime
import json
import logging
import os
import requests
import subprocess
import sys
import time
import uuid

import megaparsex
import propyte
import technicolor

name    = "dendrotox"
version = "2018-02-26T1320Z"

log = logging.getLogger(name)
log.addHandler(technicolor.ColorisingStreamHandler())
log.setLevel(logging.INFO)

global messages_received
messages_received = []

class Message(object):

    def __init__(
        self,
        raw_string                       = None,
        datetime_object                  = None,
        contact                          = None,
        text                             = None,
        seen                             = False,
        datetime_from_instantiation_time = True
        ):
        """
        The raw string time resolution is minutes, which is often insufficient,
        so, by default, the datetime is defined by the instantiation time.
        """
        self._raw_string      = raw_string
        self._datetime_object = datetime_object
        self._contact         = contact
        self._text            = text
        self._seen            = seen
        self._UUID4           = str(uuid.uuid4())
        if raw_string:
            raw_string_split = raw_string.split()
            if datetime_from_instantiation_time:
                self.set_datetime_object(
                    datetime_object = datetime.datetime.utcnow()
                )
            else:
                self.set_datetime_object(
                    datetime_string = " ".join(raw_string_split[:2])
                )
            self.set_text(
                text = " ".join(raw_string_split[2:])
            )

    def datetime_object(
        self
        ):
        return self._datetime_object

    def set_datetime_object(
        self,
        datetime_object = None,
        datetime_string = None,
        datetime_style  = "%Y-%m-%d %H:%M"
        ):
        if not datetime_object:
            datetime_object = datetime.datetime.strptime(
                datetime_string,
                datetime_style
            )
        self._datetime_object = datetime_object

    def timestamp(
        self,
        datetime_style = "%Y-%m-%dT%H%M%SZ"
        ):
        return self._datetime_object.strftime(datetime_style)

    def contact(
        self,
        preserve_visibility = False
        ):
        if not preserve_visibility:

            self.set_seen()

        return self._contact

    def set_contact(
        self,
        contact = None
        ):
        self._contact = contact

    def text(
        self,
        preserve_visibility = False
        ):
        if not preserve_visibility:
            self.set_seen()
        return self._text

    def set_text(
        self,
        text = None
        ):
        self._text = text

    def UUID4(
        self,
        preserve_visibility = False
        ):
        if not preserve_visibility:
            self.set_seen()
        return self._UUID4

    def seen(
        self
        ):
        return self._seen

    def set_seen(
        self
        ):
        self._seen = True

    def set_not_seen(
        self
        ):
        self._seen = False

    def __str__(
        self,
        preserve_visibility = False
        ):
        if not preserve_visibility:
            self.set_seen()
        return "{datetime}: {text}".format(
            datetime = self.datetime_object().strftime("%Y-%m-%dT%H%MZ"),
            text     = self.text()
        )

    def __repr__(
        self,
        preserve_visibility = False
        ):
        if not preserve_visibility:
            self.set_seen()
        return "{class_name}("                        \
               "raw_string = \"{raw_string}\", "      \
               "datetime_object = {datetime_object}, "\
               "contact = \"{contact}\", "            \
               "text = \"{text}\""                    \
               ")".format(
            class_name      = self.__class__.__name__,
            raw_string      = self._raw_string,
            datetime_object = self.datetime_object().__repr__(),
            contact         = self.contact(),
            text            = self.text()
        )

def self_ID():
    self_ID = [line.rstrip("\n") for line in open("id")][0]
    return self_ID

def start_messaging(
    path_ratox_executable = "/usr/local/bin/ratox",
    launch                = True,
    pause                 = True,
    pause_time            = 20
    ):
    if not running("ratox"):
        if os.path.isfile(path_ratox_executable) and launch:
            log.info("launch ratox")
            engage_command(
                command    = path_ratox_executable,
                background = True
            )
        else:
            log.error("executable not found: {path}".format(
                path = path_ratox_executable
            ))
            sys.exit()
        if pause:
            # pause for connection to Tox network
            time.sleep(pause_time)

def stop_messaging():
    if running("ratox"):
        engage_command(command = "killall ratox")

def restart_messaging(
    path_ratox_executable = "/usr/local/bin/ratox"
    ):
    stop_messaging()
    start_messaging(path_ratox_executable = path_ratox_executable)

def set_name(
    text = "scriptwire"
    ):
    command = "echo \"{text}\" > name/in".format(
        text    = text or ""
    )
    engage_command(command = command)

def set_state(
    text = "available"
    ):
    """
    options:
    
    - available
    - away
    - busy
    - none
    """
    command = "echo \"{text}\" > state/in".format(
        text    = text or ""
    )
    engage_command(command = command)

def set_status(
    text = "hello world"
    ):
    command = "echo \"{text}\" > status/in".format(
        text    = text or ""
    )
    engage_command(command = command)

def send_request(
    contact  = None, # Tox ID or public key
    contacts = None, # list of Tox IDs or public keys
    text     = "connection request"
    ):
    if contact:
        contacts = [contact]
    if contacts:
        for contact in contacts:
            if len(contact) == 76:
                command = "echo \"{contact}\" \"{text}\" > request/in".format(
                    contact = contact,
                    text    = text or ""
                )
                try:
                    engage_command(command = command)
                except:
                    pass
            elif len(contact) == 64:
                log.error("invalid Tox ID -- possibly attempting to use only public key")
            else:
                log.error("invalid Tox ID")

def requests():
    """
    Return a list of contacts who have sent requests.
    """
    return [contact for contact in next(os.walk("request/out"))[2]]

def accept_request(
    contact  = None, # Tox ID or public key
    contacts = None  # list of Tox IDs or public keys
    ):
    """
    Accept requests from a specified contact, a specified list of contacts or
    from all contacts that have sent requests.
    """
    if contact:
        contacts = [contact]
    if contacts == "all":
        contacts = requests()
    for contact in contacts:
        command = "echo 1 > request/out/{contact}".format(
            contact = contact
        )
        try:
            engage_command(command = command)
        except:
            pass

def remove(
    contact              = None, # Tox ID or public key
    contacts             = None, # list of Tox IDs or public keys
    Tox_ID_to_public_key = True
    ):
    if contact:
        contacts = [contact]
    if contacts == "all":
        contacts = all_contacts()
    if contacts:
        if Tox_ID_to_public_key:
            contacts = [contact[:64] for contact in contacts]
        for contact in contacts:
            command = "echo 1 > {contact}/remove".format(
                contact = contact
            )
            try:
                engage_command(command = command)
            except:
                pass

def send_message(
    contact              = None, # Tox ID or public key
    contacts             = None, # list of Tox IDs or public keys
    text                 = None, # text to send
    filepath             = None, # file to send
    Tox_ID_to_public_key = True
    ):
    if contact:
        contacts = [contact]
    if contacts == "all":
        contacts = all_contacts()
    if contacts:
        if Tox_ID_to_public_key:
            contacts = [contact[:64] for contact in contacts]
        for contact in contacts:
            if os.path.exists(contact):
                if text:
                    command = "echo \"{text}\" > {contact}/text_in".format(
                        text    = text,
                        contact = contact
                    )
                    try:
                        engage_command(command = command)
                    except:
                        pass
                if filepath:
                    if os.path.exists(filepath):
                        command =\
                            "cat \"{filepath}\" > {contact}/file_in".format(
                            filepath = filepath,
                            contact  = contact
                        )
                        try:
                            engage_command(command = command)
                        except:
                            pass
                    else:
                        log.error("error -- {filepath} not found".format(
                            filepath = filepath
                        ))
    if not contacts:
        log.error("error -- no contacts specified")

def send_request_and_message(
    contact  = None, # Tox ID or public key
    contacts = None, # list of Tox IDs or public keys
    text     = None, # text to send
    filepath = None  # file to send
    ):
    send_request(
        contact  = contact,
        contacts = contacts
    )
    send_message(
        contact  = contact,
        contacts = contacts,
        text     = text,
        filepath = filepath
    )

def send_self_ID(
    contact  = None, # Tox ID or public key
    contacts = None  # list of Tox IDs or public keys
    ):
    send_message(
        contact  = contact,
        contacts = contacts,
        text     = self_ID()
    )

def all_contacts():
    """
    Return a list of contacts by collating all directories at the working
    directory that are not ratox directories and contain a file `status`.
    """
    return [
        directory for directory in next(os.walk("."))[1]\
        if directory not in [
            "conf",
            "name",
            "nospam",
            "request",
            "state",
            "status"
        ] and\
        os.path.isfile(directory + "/status")
    ]

def get_messages():
    global messages_received
    contacts = all_contacts()
    # append any new messages to store of messages received
    for contact in contacts:
        # old messages
        messages_old = [
            message._raw_string for message in messages_received\
            if message.contact() == contact
        ]
        # old and possibly new messages
        messages_new = [
            line.rstrip("\n") for line in open("{contact}/text_out".format(
                contact = contact
            ))
        ]
        # if new messages are different to old messages, remove old messages
        # from new messages and add to store of messages
        if messages_new != messages_old:
            messages_to_store = messages_new[len(messages_old):]
            for message in messages_to_store:
                    messages_received.append(
                        Message(
                            raw_string = message,
                            contact    = contact
                        )
                    )

def received_messages(
    contact  = None, # Tox ID or public key
    contacts = None, # list of Tox IDs or public keys
    unseen   = None  # unseen messages only
    ):
    global messages_received
    get_messages()
    if contact:
        contacts = [contact]
    if contacts == "all":
        contacts = all_contacts()
    if contacts:
        messages = [
            message for message in messages_received\
            if message.contact(preserve_visibility = True) in contacts
        ]
    if unseen:
        messages = [
            message for message in messages_received\
            if not message.seen()
        ]
    else:
        messages = [
            message for message in messages_received
        ]
    return messages

def last_received_message(
    contact  = None, # Tox ID or public key
    contacts = None, # list of Tox IDs or public keys
    unseen   = True  # unseen messages only
    ):
    messages = received_messages(
        contact  = contact,
        contacts = contacts,
        unseen   = unseen
    )
    if messages:
        return messages[-1]
    else:
        return None

def send_heartbeat(
    contact  = None, # Tox ID or public key
    contacts = None, # list of Tox IDs or public keys
    text     = None
    ):
    if not text:
        text = megaparsex.heartbeat_message()
    text = text + "\n\nTox ID: " + self_ID()
    try:
        log.info("send heartbeat message: {text}".format(text = text))
        send_request_and_message(
            contact  = contact,
            contacts = contacts,
            text     = text
        )
    except:
        pass
    try:
        import propyte
        propyte.start_messaging_Pushbullet()
        propyte.send_message_Pushbullet(text = text)
    except:
        pass

def contact_calling(
    contact              = None, # Tox ID or public key
    Tox_ID_to_public_key = True
    ):
    """
    Return a boolean indicating whether a specified contact is calling.
    """
    if contact:
        if Tox_ID_to_public_key:
            contact = contact[:64]
        return "pending" in [line.rstrip("\n") for line in open(contact + "/call_state")][0]
    else:
        log.error("no contact specified")
        return False

def get_contacts_calling():
    """
    Return a list of contacts with pending calls.
    """
    contacts_calling = []
    for contact in all_contacts():
        if contact_calling(contact = contact):
            contacts_calling.append(contact)
    return contacts_calling

def receive_call(
    contact              = None, # Tox ID or public key
    Tox_ID_to_public_key = True
    ):
    """
    Answer a call from a specified contact or from the first contact found to be
    calling. Call data is sent to aplay.
    """
    command      = None
    command_base = "aplay -r 48000 -c 1 -f S16_LE - < {contact}/call_out"
    if contact:
        if Tox_ID_to_public_key:
            contact = contact[:64]
        if contact_calling(contact = contact):
            command = command_base.format(contact = contact)
    else:
        contacts = get_contacts_calling()
        if contacts:
            command = command_base.format(contact = contacts[0])
    if command:
        engage_command(command = command)
        return True
    else:
        log.error("no contact specified")
        return False

def get_input(
    contact  = None,
    contacts = None,
    prompt   = "input: "
    ):
    send_message(
        contact  = contact,
        contacts = contacts,
        text     = prompt
    )
    response = None
    while response is None:
        response = last_received_message(
            contact  = contact,  # Tox ID or public key
            contacts = contacts, # list of Tox IDs or public keys
            unseen   = True      # unseen messages only
        )
    return response.text()

def run_command(
    contact = None,
    confirm = True,
    command = None
    ):
    """
    Run a command while in optional communication with a contact. If a command
    is not specified, then a request for the command is made. If confirmation is
    requested (which it is by default), then the command to run is confirmed by
    requesting a y/n indication on whether to proceed.
    """
    if command is None:
        send_message(contact = contact, text = "enter command to run")
        message = None
        while message is None:
            message = last_received_message(contact = contact, unseen = False)
            time.sleep(0.3)
        command = message.text()
    send_message(
        contact = contact,
        text    = "command: {command}".format(command = command)
    )
    if confirm:
        confirmed = request_confirm(
            contact = contact,
            prompt  = "Do you want to run this command? (y/n)"
        )
    if confirm is False or confirmed is True:
        send_message(contact = contact, text = "run command")
        output = engage_command(command = command)
        send_message(
            contact = contact,
            text    = "output:\n\n{output}".format(output = output)
        )
    else:
        log.info("abort command run")

def engage_command(
    command    = None,
    background = True
    ):
    log.debug(command)
    if background:
        subprocess.Popen(
            [command],
            shell      = True,
            executable = "/bin/bash"
        )
        return None
    elif not background:
        process = subprocess.Popen(
            [command],
            shell      = True,
            executable = "/bin/bash",
            stdout     = subprocess.PIPE
        )
        process.wait()
        output, errors = process.communicate()
        return output
    else:
        return None

def running(
    program
    ):
    results = subprocess.Popen(
        ["ps", "-A"],
        stdout             = subprocess.PIPE,
        universal_newlines = True
    ).communicate()[0].split("\n")
    results = results
    matches_current = [
        line for line in results if program in line and "defunct" not in line
    ]
    if matches_current:
        return True
    else:
        return False

# get existing messages and set them to seen
get_messages()
for message in messages_received:
    message.set_seen()

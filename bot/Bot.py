#!/usr/bin/env python

import os
import argparse

from code.Log import Log

parser = argparse.ArgumentParser(description='Basic Bot Demo')
parser.add_argument('--name',
                    default="BaseBot",
                    help='Name of this bot')
parser.add_argument('--token',
                    help='Token to use to login')

args = parser.parse_args()

log = Log(args)

log.info(args)

# We break normal patterns here, and begin importing the rest of the bot after logging and parsing is done!

from code.Client import Client

x = Client()

#################################
### Register all modules here ###
#################################

from code.ExampleModule import ExampleModule

x.register(ExampleModule())


if args.token:
    log.info("Using token from args")
    x.run(args.token)
elif os.environ.get('CLIENT_TOKEN', None):
    log.info("Using token from ENV")
    x.run(os.environ['CLIENT_TOKEN'])
else:
    log.critical("No token was given in the arguments or the ENV!")
    raise RuntimeError("No valid token given, cannot start bot!")
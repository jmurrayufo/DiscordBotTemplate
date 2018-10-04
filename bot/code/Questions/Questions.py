
from pprint import pprint
from wit import Wit
import datetime
import os
import re
import shlex

from ..Client import Client
from ..CommandProcessor import DiscordArgumentParser, ValidUserAction
from ..CommandProcessor.exceptions import NoValidCommands, HelpNeeded
from ..Log import Log
from ..SQL import SQL



class Questions:

    def __init__(self):
        self.client = Client()
        self.log = Log()
        self.ready = False
        self.sql = SQL()


    async def on_message(self, message):
        if message.author == self.client.user:
            self.log.debug("Self, ignore")
            return

        if not self.ready:
            self.log.warning(f"Saw message before we were ready: {message.content}")
            return

        self.log.debug(f"Saw message: {message.content}")

        match_obj = re.match(r".*\?$", message.content)
        if match_obj:
            self.log.debug("I think we saw a question, let's try to answer it!")
            await self.question_proc(message)


    async def on_ready(self):
        self.log.info("Questions, ready to receive commands!")
        self.ready = True


    async def question_proc(self, message):
        """Handle specific commands, or pass to the session_manager
        """
        msg = "It seems you have asked me a question! Let me try to answer it!"
        await self.client.send_message(message.channel, msg)

        wit_client = Wit(access_token=os.environ.get('WIT_CLIENT_TOKEN', None), logger=self.log)
        resp = wit_client.message(message.content)
        # await self.client.send_message(message.channel, str(resp))
        for entry in resp['entities']:
            for element in resp['entities'][entry]:
                msg = f"Saw a {entry} value of {element['value']} with {element['confidence']:.3%} confidence."
                await self.client.send_message(message.channel, msg)
        pprint(resp)


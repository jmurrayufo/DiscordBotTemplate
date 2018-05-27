
import re
import shlex
import datetime

from ..Client import Client
from ..CommandProcessor import DiscordArgumentParser, ValidUserAction
from ..CommandProcessor.exceptions import NoValidCommands, HelpNeeded
from ..Log import Log
from ..SQL import SQL



class Dragons:

    def __init__(self):
        self.client = Client()
        self.log = Log()
        self.ready = False
        self.sql = SQL()


    async def on_message(self, message):
        if not self.ready:
            self.log.warning(f"Saw message before we were ready: {message.content}")
            return

        self.log.debug(f"Saw message: {message.content}")

        match_obj = re.match("^>dragon(s)?", message.content, re.IGNORECASE)
        if match_obj:
            # await self.log_command(message)
            self.log.info("Saw a command, handle it!")
            await self.command_proc(message)


    async def on_ready(self):
        self.log.info("Stats, ready to recieve commands!")
        self.ready = True



    async def command_proc(self, message):
        """Handle specific commands, or pass to the session_manager
        """
        parser = DiscordArgumentParser(description="A Test Command", prog=">dragon")
        parser.set_defaults(message=message)
        sp = parser.add_subparsers()

        sub_parser = sp.add_parser('register',
                                   description='Register a new dragon dragon')
        sub_parser.set_defaults(cmd=self._cmd_register)

        sub_parser = sp.add_parser('log',
                                   description='Log stats for your dragon(s)')
        sub_parser.set_defaults(cmd=self._cmd_log)

        sub_parser = sp.add_parser('graph',
                                   description='Graph stats from a dragon')
        sub_parser.set_defaults(cmd=self._cmd_graph)

        sub_parser = sp.add_parser('list',
                                   description='Log stats for your dragon')
        sub_parser.set_defaults(cmd=self._cmd_list)

        try:
            self.log.info("Parse Arguments")
            results = parser.parse_args(shlex.split(message.content)[1:])
            self.log.info(results)
            if type(results) == str:
                self.log.info("Got normal return, printing and returning")
                self.log.info(type(results))
                await self.client.send_message(message.channel, results)
                return
            elif hasattr(results, 'cmd'):
                # await self.client.send_message(message.channel, results)
                await results.cmd(results)
                return
            else:
                await self.client.send_message(message.channel, results)
                msg = "Well that's funny, I don't know wha to do!"
                await self.client.send_message(message.channel, msg)
                return
        except NoValidCommands as e:
            # We didn't get a subcommand, let someone else deal with this mess!
            self.log.error("???")
            pass
        except HelpNeeded as e:
            self.log.info("TypeError Return")
            self.log.info(e)
            msg = f"{e}. You can add `-h` or `--help` to any command to get help!"
            await self.client.send_message(message.channel, msg)
            return
            pass

        return

    async def _cmd_register(self, args):
        message = args.message
        self.log.info("Start _cmd_register command")

        self.log.info(args)
        msg = "Sorry, this command doesn't work yet!"
        await self.client.send_message(message.channel, msg)

        self.log.info("Finished _cmd_register command")
        return


    async def _cmd_log(self, args):
        message = args.message
        self.log.info("Start _cmd_log command")

        self.log.info(args)
        msg = "Sorry, this command doesn't work yet!"
        await self.client.send_message(message.channel, msg)

        self.log.info("Finished _cmd_log command")
        return


    async def _cmd_graph(self, args):
        message = args.message
        self.log.info("Start _cmd_graph command")

        self.log.info(args)
        msg = "Sorry, this command doesn't work yet!"
        await self.client.send_message(message.channel, msg)

        self.log.info("Finished _cmd_graph command")
        return


    async def _cmd_list(self, args):
        message = args.message
        self.log.info("Start _cmd_list command")

        self.log.info(args)
        msg = "Sorry, this command doesn't work yet!"
        await self.client.send_message(message.channel, msg)

        self.log.info("Finished _cmd_list command")
        return
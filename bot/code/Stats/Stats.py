
import re
import shlex

from ..Client import Client
from ..CommandProcessor import DiscordArgumentParser, ValidUserAction
from ..CommandProcessor.exceptions import NoValidCommands, HelpNeeded
from ..Log import Log
from ..SQL import SQL



class Stats:

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

        match_obj = re.match("^>", message.content)
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
        parser = DiscordArgumentParser(description="A Test Command", prog="", add_help=False)
        parser.set_defaults(message=message)
        sp = parser.add_subparsers()

        sub_parser = sp.add_parser('>stats',
                                   description='test something')
        sub_parser.add_argument(
            "user_id",
            action=ValidUserAction,
            help="Mention of the user in question",
            metavar="@user",
            nargs="?",
            )
        sub_parser.set_defaults(subCMD='>test',
                                cmd=self._cmd_stat)

        try:
            self.log.info("Parse Arguments")
            results = parser.parse_args(shlex.split(message.content))
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

    async def _cmd_stat(self, args):
        message = args.message

        await self.client.send_message(message.channel, "Got the command")

        self.log.info("Finished stat command")
        return

    ### UNUSED ###

    async def on_channel_create(self, channel):
        pass


    async def on_channel_delete(self, channel):
        pass


    async def on_channel_update(self, before, after):
        pass


    async def on_error(self, event, *args, **kwargs):
        pass


    async def on_group_join(self, channel, user):
        pass


    async def on_group_remove(self, channel, user):
        pass


    async def on_member_ban(self, member):
        pass


    async def on_member_join(self, member):
        pass


    async def on_member_remove(self, member):
        pass


    async def on_member_unban(self, server, user):
        pass


    async def on_member_update(self, before, after):
        pass


    async def on_message_delete(self, message):
        pass


    async def on_message_edit(self, before, after):
        pass


    async def on_reaction_add(self, reaction, user):
        pass


    async def on_reaction_clear(self, message, reactions):
        pass


    async def on_reaction_remove(self, reaction, user):
        pass


    async def on_resumed(self, ):
        pass


    async def on_server_available(self, server):
        pass


    async def on_server_emojis_update(self, before, after):
        pass


    async def on_server_join(self, server):
        pass


    async def on_server_remove(self, server):
        pass


    async def on_server_role_create(self, role):
        pass


    async def on_server_role_delete(self, role):
        pass


    async def on_server_role_update(self, before, after):
        pass


    async def on_server_unavailable(self, server):
        pass


    async def on_server_update(self, before, after):
        pass


    async def on_socket_raw_receive(self, msg):
        pass


    async def on_socket_raw_send(self, payload):
        pass


    async def on_typing(self, channel, user, when):
        pass


    async def on_voice_state_update(self, before, after):
        pass


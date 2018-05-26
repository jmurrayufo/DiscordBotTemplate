
import re
import shlex
import datetime

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

        user_id = args.user_id if args.user_id else args.message.author.id

        cur = self.sql.cur

        cmd = """
            SELECT * FROM channels
        """
        channel_data = cur.execute(cmd).fetchall()
        # Rekey this data
        channel_lookup = {}
        for channel in channel_data:
            channel_lookup[channel['channel_id']] = channel

        cmd = f"""
            SELECT * FROM user_stats WHERE user_id={user_id}
        """
        user_data = cur.execute(cmd).fetchall()

        msg = f"Stats for user: <@{user_id}>"
        msg += "\n```\n"
        for row in user_data:
            self.log.info(row)
            msg += f"\nChannel: {channel_lookup[row['channel_id']]['name']}\n"
            msg += f"      Messages: {row['messages']}\n"
            last_active = datetime.datetime.fromtimestamp(row['last_active'])
            msg += f"   Last Active: {last_active} ({datetime.datetime.utcnow()-last_active} ago)\n"
        msg += "\n```"
        await self.client.send_message(args.message.author, msg)


        self.log.info("Finished stat command")
        return

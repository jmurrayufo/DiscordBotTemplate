
import asyncio
import datetime
import re
import shlex

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


    async def _cmd_log(self, args):
        message = args.message
        self.log.info("Start _cmd_log command")
        self.log.info(args)

        msg = "Sorry, this command doesn't work yet!"
        await self.client.send_message(message.channel, msg)

        self.log.info("Finished _cmd_log command")
        return


    async def _cmd_register(self, args):
        message = args.message
        user = message.author
        cur = self.sql.cur

        self.log.info("Start _cmd_register command")
        self.log.info(args)

        await self.client.start_private_message(user)
        for channel in self.client.private_channels:
            if channel.user == user:
                break
            else:
                raise RuntimeError("Couldn't find our pirvate channel, woops!")

        msg = "Do you wish to register a new dragon?"
        choice = await self.client.confirm_prompt(channel, msg)
        if choice is not True:
            return

        await asyncio.sleep(1)
        msg = "Okay!"
        await self.client.send_message(channel, msg)
        await asyncio.sleep(1)

        while True:
            msg = "What is your dragons name? (Your next message should be their full name, with no extra characters)"
            name = await self.client.text_prompt(channel, msg, user=message.author, timeout=120)
            await asyncio.sleep(1)

            msg = f"Your dragons name is '{name}', is that correct?"
            choice = await self.client.confirm_prompt(channel, msg)

            if choice is True:
                break
            elif choice is False:
                continue
            elif choice is None:
                return

        while True:
            msg = "When was your dragon hatched? If you don't know exactly, guess as close as you can!"\
                  " (Format is YYYY-MM-DD, so you can answer `2018-03-25`)\n. You can say STOP to exit."
            hatch_date = await self.client.text_prompt(channel, msg, user=message.author, timeout=300)

            if hatch_date is None:
                self.log.info("STOP encountered?")
                return

            self.log.info(f"Got user response of: {hatch_date}")
            hatch_match = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", hatch_date)
            if hatch_match is None:
                continue

            hatch_date = datetime.datetime(
                int(hatch_match.group('year')),
                int(hatch_match.group('month')),
                int(hatch_match.group('day')),
                )

            await asyncio.sleep(1)

            now = datetime.datetime.utcnow().replace(microsecond=0, second=0, minute=0, hour=0)
            age = (now-hatch_date).total_seconds()/60/60/24

            if age < 30:
                age = f"{age:.0f} days"
            elif age < 365/12*18:
                age = f"{age/30:.1f} months"
            else:
                age = f"{age/365:.1f} years"

            msg = f"Your dragons hatch date was '{hatch_date}' (about {age} ago!), is that correct?"
            choice = await self.client.confirm_prompt(channel, msg)

            if choice is True:
                break
            elif choice is False:
                continue
            elif choice is None:
                return

        created_at = datetime.datetime.utcnow().timestamp()
        hatched_on = hatch_date.timestamp()
        last_updated = datetime.datetime.utcnow().timestamp()
        user_id = user.id
        cmd = """
            INSERT INTO dragons
            (
                name,
                created_at,
                hatched_on,
                last_updated,
                user_id
            ) VALUES (
                :name,
                :created_at,
                :hatched_on,
                :last_updated,
                :user_id
            )
        """
        cur.execute(cmd,locals())
        await self.sql.commit()

        msg = f"{name} was registered to the DB! You can try `>dragon list` to see them!"

        self.log.info("Finished _cmd_register command")
        return
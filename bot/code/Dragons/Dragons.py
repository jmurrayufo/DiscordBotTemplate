

from dateutil.parser import parse as datetime_parser
import asyncio
import csv
import datetime
import io
import numpy as np
import re
import requests
import shlex

from ..Client import Client
from ..CommandProcessor import DiscordArgumentParser, ValidUserAction
from ..CommandProcessor.exceptions import NoValidCommands, HelpNeeded
from ..Log import Log
from ..SQL import SQL
from .Grapher import Grapher



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
        parser = DiscordArgumentParser(
            description="Manage information about a dragon",
            prog=">dragon")
        parser.set_defaults(message=message)
        sp = parser.add_subparsers()

        sub_parser = sp.add_parser('csv',
                                   description='Graph stats from a dragon')
        sub_parser.add_argument(
            "--template",
            action='store_true',
            help="Log to previous date",
            )
        sub_parser.set_defaults(cmd=self._cmd_csv)

        sub_parser = sp.add_parser('graph',
                                   description='Graph stats from a dragon')
        sub_parser.add_argument(
            "id",
            help="ID of the dragon",
            metavar="DRAGON-ID"
            )
        sub_parser.set_defaults(cmd=self._cmd_graph)

        sub_parser = sp.add_parser('list',
                                   description='Log stats for your dragon')
        sub_parser.add_argument("--global",
            action='store_true',
            help='List all dragons, not just USERS')
        sub_parser.add_argument(
            "user_id",
            action=ValidUserAction,
            default=f"<@{message.author.id}>",
            help="Mention of the user in question",
            metavar="@user",
            nargs="?",
            )
        sub_parser.set_defaults(cmd=self._cmd_list)

        sub_parser = sp.add_parser('log',
                                   description='Log stats for your dragon(s)')
        sub_parser.add_argument(
            "id",
            help="ID of the dragon",
            metavar="DRAGON-ID"
            )
        sub_parser.add_argument(
            "--date",
            default=datetime.datetime.now(),
            help="Log to previous date",
            type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d'),
            )

        group = sub_parser.add_argument_group(title="Basic Stats")
        group.add_argument(
            "--length",
            help="Length of dragon (units assumed to be centimeters unless given)",
            metavar="LENGTH",
            nargs="+",
            )
        group.add_argument(
            "--mass", "--weight",
            help="Mass of dragon (units assumed to be grams unless given)",
            metavar="MASS",
            nargs="+",
            )

        group = sub_parser.add_argument_group(title="Behaviors")
        group.add_argument(
            "--bowel-movement",
            action='store_true',
            default=None,
            help="Dragon had a bowel movement.",
            )
        group.add_argument(
            "--brumation",
            action='store_true',
            default=None,
            help="Dragon is brumating",
            )
        group.add_argument(
            "--shedding",
            action='store_true',
            default=None,
            help="Dragon is shedding",
            )

        group = sub_parser.add_argument_group(title="Care")
        group.add_argument(
            "--fecal-check",
            action='store_true',
            default=None,
            help="Checked fecal mater for parasites",
            )
        group.add_argument(
            "--new-uv-tube",
            action='store_true',
            default=None,
            help="Replaced the UV tube",
            )
        group.add_argument(
            "--vet-visit",
            action='store_true',
            default=None,
            help="Had a vet visit",
            )

        group = sub_parser.add_argument_group(title="Feeding")
        group.add_argument(
            "--crickets",
            const=1,
            default=None,
            help="Ate Crickets",
            nargs="?",
            type=int,
            )
        group.add_argument(
            "--bsfl",
            const=1,
            default=None,
            help="Ate Black Soldier Fly Larva",
            nargs="?",
            type=int,
            )
        group.add_argument(
            "--dubia",
            const=1,
            default=None,
            help="Ate Dubia Roaches",
            nargs="?",
            type=int,
            )
        group.add_argument(
            "--horn-worms",
            const=1,
            default=None,
            help="Ate Horn Worms",
            nargs="?",
            type=int,
            )
        group.add_argument(
            "--meal-worms",
            const=1,
            default=None,
            help="Ate Meal Worms",
            nargs="?",
            type=int,
            )
        group.add_argument(
            "--pinkie-mouse",
            const=1,
            default=None,
            help="Ate Pinkie Mince",
            nargs="?",
            type=int,
            )
        group.add_argument(
            "--silk-worms",
            const=1,
            default=None,
            help="Ate Silk Worm",
            nargs="?",
            type=int,
            )
        group.add_argument(
            "--super-worms",
            const=1,
            default=None,
            help="Ate Super Worm",
            nargs="?",
            type=int,
            )

        sub_parser.add_argument(
            "--note",
            help="Text note to affix",
            metavar="NOTE",
            nargs="+",
            )

        sub_parser.set_defaults(cmd=self._cmd_log)

        sub_parser = sp.add_parser('register',
                                   description='Register a new dragon dragon')
        sub_parser.set_defaults(cmd=self._cmd_register)

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
                # await self.client.send_message(message.channel, results)
                msg = parser.format_help()
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


    async def _cmd_csv(self, args):
        message = args.message
        cur = self.sql.cur

        self.log.info("Start _cmd_graph command")
        self.log.info(args)

        if args.message.attachments:
            for attachment in args.message.attachments:
                response = requests.get(attachment['url'])

                data = list(csv.DictReader(io.StringIO(response.text)))
                ids = set()
                try:
                    for row in data:
                        ids.add(str(int(row['ID'])))
                        row['Date'] = datetime_parser(row['Date']).timestamp()
                        row['Weight (g)'] = float(row['Weight (g)']) if row['Weight (g)'] != '' else None
                        row['Length (cm)'] = float(row['Length (cm)']) if row['Length (cm)'] != '' else None
                        row['Notes'] = row['Notes'] if row['Notes'] != '' else None
                except Exception as e:
                    msg = f"Couldn't handle csv because: {e}"
                    await self.client.send_message(message.channel, msg)
                    continue

                # Get dragons for this user
                cur = self.sql.cur
                user_id = args.message.author.id
                dragon_ids = ",".join(ids)
                cmd = f"""
                    SELECT *
                    FROM dragons
                    WHERE
                        user_id=:user_id
                        AND dragon_id IN ({dragon_ids})
                """
                dragons = cur.execute(cmd,locals()).fetchall()
                if dragons == None or len(dragons) != len(ids):
                    msg = f"Woops! I can't save that CSV file. I couldn't match up you, your dragon IDs and my database. Are you sure the ID column is correct, and you own all these dragons?"
                    await self.client.send_message(message.channel, msg)
                    continue

                dragon_names = ", ".join([x['name'] for x in dragons])

                question = f"About to store {len(data)} rows for {dragon_names}. Are you sure?"
                try:
                    choice = await self.client.confirm_prompt(args.message.channel, question, user=args.message.author, timeout=60)
                except TimeoutError:
                    continue

                if choice is not True:
                    continue

                for row in data:
                    dragon_id = row['ID']
                    log_date = row['Date']
                    mass = row['Weight (g)']
                    length = row['Length (cm)']
                    note = row['Notes']

                    cmd = """
                        INSERT 
                        INTO dragon_stat_logs
                        (
                            dragon_id,
                            log_date,
                            mass,
                            length,
                            note
                        ) VALUES (
                            :dragon_id,
                            :log_date,
                            :mass,
                            :length,
                            :note
                        )
                    """
                    cur.execute(cmd, locals())
                await self.sql.commit(now=True)
                

        elif args.template:
            fields = ["ID", "Date", "Weight (g)", "Length (cm)", "Notes"]
            csv_file = io.StringIO()

            writer = csv.DictWriter(csv_file, fieldnames=fields)
            writer.writeheader()

            csv_file.seek(0)

            await self.client.send_file(message.channel, csv_file, filename=f"data_template.csv")

            csv_file.close()

        else:
            msg = "You can upload a file with the comment `>dragon csv <ID>`, or call `>dragon csv --template` to get a template file!"
            await self.client.send_message(message.channel, msg)

        self.log.info("Finished _cmd_graph command")
        return


    async def _cmd_graph(self, args):
        message = args.message
        cur = self.sql.cur

        self.log.info("Start _cmd_graph command")
        self.log.info(args)

        g = Grapher(args)
        await g.run()

        self.log.info("Finished _cmd_graph command")
        return


    async def _cmd_list(self, args):
        message = args.message
        user_id = args.user_id
        self.log.info("Start _cmd_list command")
        self.log.info(args)
        cur = self.sql.cur
        cmd = """
            SELECT *
            FROM dragons
            WHERE
                user_id=:user_id
        """
        dragons = cur.execute(cmd,locals())

        msg = "Dragons:"
        msg += "\n```"
        msg += f"\n  ID Name"
        for dragon in dragons:
            msg += f"\n{dragon['dragon_id']:4d} {dragon['name']}"
        msg += "\n```"

        await self.client.send_message(message.channel, msg)

        self.log.info("Finished _cmd_list command")
        return


    async def _cmd_log(self, args):
        message = args.message
        cur = self.sql.cur

        self.log.info("Start _cmd_log command")
        self.log.info(args)

        mass = None
        length = None
        note = None
        dragon_id = args.id
        user_id = args.message.author.id

        if args.mass:
            mass = " ".join(args.mass)
            mass_match_obj = re.match(
                r"(?P<num>[+-]?((\d+\.?\d*)|(\.\d+))) ?(?P<unit>g|grams?|kg|lbs?)?",
                mass)

            mass = float(mass_match_obj.group('num'))
            unit = mass_match_obj.group('unit')
            if unit in ['lb', 'lbs']:
                mass = mass * 453.592
            elif unit in ['kg']:
                mass = mass * 1000

            self.log.info(f"Mass is: {mass}g")

        if args.length:
            length = " ".join(args.length)
            length_match_obj = re.match(
                r"(?P<num>[+-]?((\d+\.?\d*)|(\.\d+))) ?(?P<unit>cm|m|in|ft|\"|\'|smoots?)?",
                length)

            length = float(length_match_obj.group('num'))
            unit = length_match_obj.group('unit')
            if unit in ['in', '\"']:
                length = length * 2.54
            elif unit in ['ft', '\'']:
                length = length * 30.48
            elif unit in ['m']:
                length = length * 100
            elif unit in ['smoot', 'smoots']:
                length = length * 170.18

            self.log.info(f"Length is: {length}cm")

        if args.note:
            note = " ".join(args.note)
            self.log.info(f"Note is: {note}")

        log_date = args.date
        self.log.info(f"Date is: {log_date}")

        # Lookup name of dragon given
        cmd = """
            SELECT *
            FROM dragons 
            WHERE dragon_id=:dragon_id
                AND user_id=:user_id
        """
        dragon_dict = cur.execute(cmd, locals()).fetchone()

        if dragon_dict is None:
            await self.client.send_message(
                message.channel,
                f"I couldn't find a draong with id {dragon_id}, owned by you!")
            return

        msg = "Would you like to log this?"
        msg += "\n```"
        msg += f"\n  Name: {dragon_dict['name']}"
        msg += f"\n  Date: {log_date}"

        if mass is not None:
            msg += f"\n          Mass: {mass}"
        if length is not None:
            msg += f"\n        Length: {length}"

        if args.bowel_movement is not None:
            msg += f"\nBowel Movement: {args.bowel_movement}"
        if args.brumation is not None:
            msg += f"\n     Brumation: {args.brumation}"
        if args.shedding is not None:
            msg += f"\n      Shedding: {args.shedding}"

        if args.fecal_check is not None:
            msg += f"\n   Fecal Check: {args.fecal_check}"
        if args.new_uv_tube is not None:
            msg += f"\n   New UV Tube: {args.new_uv_tube}"
        if args.vet_visit is not None:
            msg += f"\n     Vet Visit: {args.vet_visit}"

        if args.crickets is not None:
            msg += f"\n      Crickets: {args.crickets}"            
        if args.bsfl is not None:
            msg += f"\n          BSFL: {args.bsfl}"            
        if args.dubia is not None:
            msg += f"\n  Dubia Roachs: {args.dubia}"            
        if args.horn_worms is not None:
            msg += f"\n    Horn Worms: {args.horn_worms}"            
        if args.meal_worms is not None:
            msg += f"\n    Meal Worms: {args.meal_worms}"            
        if args.pinkie_mouse is not None:
            msg += f"\n  Pinkie Mouse: {args.pinkie_mouse}"            
        if args.silk_worms is not None:
            msg += f"\n    Silk Worms: {args.silk_worms}"            
        if args.super_worms is not None:
            msg += f"\n   Super Worms: {args.super_worms}"

        if note is not None:
            msg += f"\n          Note: {note}"
        msg += "\n```"
        answer = await self.client.confirm_prompt(
            message.channel, 
            msg, 
            user=message.author)

        if answer is not True:
            self.log.info("Finished _cmd_log command")
            return

        log_date = log_date.timestamp()
        # Save to SQL
        cmd = """
            INSERT 
            INTO dragon_stat_logs
            (
                dragon_id,
                log_date,
                mass,
                length,
                note
            ) VALUES (
                :dragon_id,
                :log_date,
                :mass,
                :length,
                :note
            )
        """
        cur.execute(cmd, locals())
        await self.sql.commit(now=True)

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
        await self.client.send_message(channel, msg)

        self.log.info("Finished _cmd_register command")
        return
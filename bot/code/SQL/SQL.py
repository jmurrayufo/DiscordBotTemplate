
import asyncio
import sqlite3
import pathlib
import time
import datetime

from ..Singleton import Singleton
from ..Log import Log
from ..Client import Client



class SQL(metaclass=Singleton):
    """Manage SQL connection, as well as basic user information
    """

    def __init__(self, db_name):

        db_path = pathlib.Path(db_name)
        self.log = Log()
        if not db_path.is_file():
            self.create_db(db_name)

        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = self.dict_factory
        self.client = Client()
        self._commit_in_progress = False
        self.log.info("SQL init completed")


    def create_db(self, db_name):
        self.log.warning("New DB file")
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL")
        conn.commit()
        cur.execute("PRAGMA synchronous=1")
        conn.commit()
        conn.close()
        self.log.warning("Finished new DB file creation")


    @property
    def cur(self):
        return self.conn.cursor()


    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    async def on_ready(self):
        await self.table_setup()

        for server in self.client.servers:
            self.log.info(f"Boot registration for {server}")
            self.log.info(f"Register {len(server.members)}")
            self.log.info(f"Register {len(server.channels)}")
            for member in server.members:
                await self.register_user(member)
            for channel in server.channels:
                await self.register_channel(channel)

        self.log.info("SQL registered to receive commands!")


    async def on_message(self, message):
        self.log.debug(f"Got message: {message.content}")
        self.log.debug(f"       From: {message.author.name} ({message.author.id})")
        if message.server:
            self.log.debug(f"         On: {message.server} ({message.server.id})")
        else:
            # Do not save or parse private channels
            return

        await self.register_user(message.author)
        await self.register_channel(message.channel)

        cur = self.cur

        channel_data = {}
        channel_data['last_active'] = datetime.datetime.utcnow().timestamp()
        channel_data['channel_id'] = message.channel.id
        cmd = """
            UPDATE OR IGNORE
                channels
            SET 
                messages = 1 + messages,
                last_active = :last_active
            WHERE
                channel_id = :channel_id
        """
        self.cur.execute(cmd, channel_data)


        user_data = {}
        user_data['last_active'] = datetime.datetime.utcnow().timestamp()
        user_data['user_id'] = message.author.id
        user_data['channel_id'] = message.channel.id
        user_data['server_id'] = message.server.id

        cmd = r"""
                SELECT user_id 
                FROM user_channel_stats 
                WHERE user_id=:user_id 
                    AND server_id=:server_id 
                    AND channel_id=:channel_id
                """
        if not cur.execute(cmd, user_data).fetchone():
            cmd = """
                INSERT INTO user_channel_stats
                (
                    user_id,
                    channel_id,
                    server_id
                ) VALUES (
                    :user_id,
                    :channel_id,
                    :server_id
                )
                """
            self.cur.execute(cmd, user_data)

        cmd = """
            UPDATE OR IGNORE
                user_channel_stats
            SET 
                messages = 1 + messages,
                last_active = :last_active
            WHERE
                user_id = :user_id
                AND channel_id = :channel_id
                AND server_id = :server_id
        """
        self.cur.execute(cmd, user_data)
        await self.commit()

    async def register_user(self, user):
        cur = self.cur

        # Check if our user exists
        user_data = {}
        user_data['avatar'] = user.avatar
        user_data['avatar_url'] = user.avatar_url
        user_data['bot'] = user.bot
        user_data['created_at'] = user.created_at
        user_data['default_avatar_url'] = user.default_avatar_url
        user_data['discriminator'] = user.discriminator
        user_data['display_name'] = user.display_name
        user_data['last_active'] = datetime.datetime.utcnow().timestamp()
        user_data['mention'] = user.mention
        user_data['name'] = user.name
        user_data['user_id'] = user.id
        user_data['first_seen'] = datetime.datetime.utcnow().timestamp()

        # Check to see if the user exists
        if not cur.execute(f"SELECT user_id FROM users WHERE user_id={user.id}").fetchone():
            self.log.info(f"New user seen: {user.display_name} ({user.name})")

            cmd = """
                INSERT OR REPLACE INTO users 
                (
                    name,
                    display_name,
                    user_id,
                    discriminator,
                    avatar,
                    bot,
                    avatar_url,
                    default_avatar_url,
                    mention,
                    created_at,
                    last_active,
                    first_seen
                ) VALUES (
                    :name,
                    :display_name,
                    :user_id,
                    :discriminator,
                    :avatar,
                    :bot,
                    :avatar_url,
                    :default_avatar_url,
                    :mention,
                    :created_at,
                    :last_active,
                    :first_seen
                )
                """
            self.cur.execute(cmd, user_data)
        else:
            cmd = """
                UPDATE users 
                SET last_active=:last_active
                WHERE user_id=:user_id
                """
            self.cur.execute(cmd, user_data)


    async def register_channel(self, channel):        
        cur = self.cur


        channel_data = {}
        channel_data['channel_id'] = channel.id
        channel_data['created_at'] = channel.created_at.timestamp()
        channel_data['last_active'] = datetime.datetime.utcnow().timestamp()
        channel_data['mention'] = channel.mention
        channel_data['name'] = channel.name
        channel_data['position'] = channel.position
        channel_data['server_id'] = channel.server.id
        channel_data['topic'] = channel.topic

        # Check to see if the channel exists
        if not cur.execute(f"SELECT channel_id FROM channels WHERE channel_id=:channel_id", channel_data).fetchone():
            self.log.info(f"New channel seen: {channel_data['name']}")

            cmd = """
                INSERT OR REPLACE INTO channels 
                (
                    name,
                    server_id,
                    channel_id,
                    topic,
                    position,
                    mention,
                    created_at
                ) VALUES (
                    :name,
                    :server_id,
                    :channel_id,
                    :topic,
                    :position,
                    :mention,
                    :created_at
                )
                """
            self.cur.execute(cmd, channel_data)
            # await self.commit()



    async def commit(self, now=True):
        # Schedule a commit in the future
        # Get loop from the client, schedule a call to _commit and return
        if now:
            self._commit_in_progress = True
            self.conn.commit()
            self._commit_in_progress = False
        else:
            asyncio.ensure_future(self._commit(now))


    async def _commit(self, now=True):
        self.log.debug("Start a _commit()")
        if self._commit_in_progress and not now:
            self.log.debug("Skipped a _commit()")
            return
        self._commit_in_progress = True
        if not now:
            await asyncio.sleep(5)
        if not self._commit_in_progress:
            return
        # Commit SQL
        self.conn.commit()
        self._commit_in_progress = False
        self.log.info("Finished a _commit()")



    async def table_exists(self, table_name):
        cmd = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        if self.cur.execute(cmd).fetchone():
            return True
        return False


    async def table_setup(self):
        """Setup any SQL tables needed for this class
        """
        self.log = Log()


        self.log.info("Check to see if users exists.")
        if not await self.table_exists("users"):
            self.log.info("Create users table")
            cur = self.cur
            cmd = """
                CREATE TABLE IF NOT EXISTS users
                (
                    name TEXT NOT NULL,
                    display_name TEXT,
                    user_id TEXT NOT NULL UNIQUE,
                    discriminator TEXT,
                    avatar TEXT,
                    bot BOOLEAN,
                    avatar_url TEXT,
                    default_avatar TEXT,
                    default_avatar_url TEXT,
                    mention TEXT,
                    created_at INTEGER,
                    last_active INTEGER,
                    first_seen INTEGER
                )"""
            cur.execute(cmd)
            await self.commit()


        self.log.info("Check to see if channels exists.")
        if not await self.table_exists("channels"):
            self.log.info("Create channels table")
            cur = self.cur
            cmd = """
                CREATE TABLE IF NOT EXISTS channels
                (
                    name TEXT NOT NULL,
                    server_id TEXT NOT NULL,
                    channel_id TEXT NOT NULL UNIQUE,
                    topic TEXT,
                    position INTEGER,
                    mention TEXT,
                    created_at INTEGER,
                    messages INTEGER DEFAULT 0,
                    last_active INTEGER DEFAULT 0
                )"""
            cur.execute(cmd)
            await self.commit()


        self.log.info("Check to see if user_channel_stats exists.")
        if not await self.table_exists("user_channel_stats"):
            self.log.info("Create user_channel_stats table")
            cur = self.cur
            cmd = """
                CREATE TABLE IF NOT EXISTS user_channel_stats
                (
                    user_id TEXT NOT NULL,
                    channel_id TEXT,
                    server_id TEXT DEFAULT '',
                    messages INTEGER DEFAULT 0,
                    last_active INTEGER DEFAULT 0
                )"""
            cur.execute(cmd)
            await self.commit()


        self.log.info("Check to see if dragons exists.")
        if not await self.table_exists("dragons"):
            self.log.info("Create dragons table")
            cur = self.cur
            cmd = """
                CREATE TABLE IF NOT EXISTS dragons
                (
                    dragon_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                    gender TEXT,
                    name TEXT,
                    created_at INTEGER,
                    hatched_on INTEGER,
                    last_updated INTEGER,
                    user_id TEXT -- Owner
                )"""
            cur.execute(cmd)
            await self.commit()


        self.log.info("Check to see if dragon_stat_logs exists.")
        if not await self.table_exists("dragon_stat_logs"):
            self.log.info("Create dragon_stat_logs table")
            cur = self.cur
            cmd = """
                CREATE TABLE IF NOT EXISTS dragon_stat_logs
                (
                    dragon_id INTEGER NOT NULL,
                    log_date INTEGER,

                    length REAL,
                    mass REAL,

                    bowel_movement BOOLEAN,
                    brumation BOOLEAN,
                    fecal_check BOOLEAN,
                    shedding BOOLEAN,

                    new_uv_tube BOOLEAN,
                    vet_visit BOOLEAN,

                    crickets INTEGER,
                    bsfl INTEGER,
                    dubia INTEGER,
                    horn_worms INTEGER,
                    meal_worms INTEGER,
                    pinkie_mouse INTEGER,
                    silk_worms INTEGER,
                    super_worms INTEGER,

                    note TEXT
                )"""
            cur.execute(cmd)
            await self.commit()


"""
Neat trick for ranks
select  p1.*
,       (
        select  count(*)
        from    People as p2
        where   p2.age > p1.age
        ) as AgeRank
from    People as p1
where   p1.Name = 'Juju bear'
"""

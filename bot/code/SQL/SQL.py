
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

        self.log.info("SQL registered to receive commands!")


    async def on_message(self, message):
        self.log.debug(f"Got message: {message.content}")
        self.log.debug(f"       From: {message.author.name} ({message.author.id})")
        if message.server:
            self.log.debug(f"         On: {message.server} ({message.server.id})")

        cur = self.cur

        # Check if our user exists
        data = {}
        data['name'] = message.author.name
        data['display_name'] = message.author.display_name
        data['user_id'] = message.author.id
        data['discriminator'] = message.author.discriminator
        data['avatar'] = message.author.avatar
        data['bot'] = message.author.bot
        data['avatar_url'] = message.author.avatar_url
        data['default_avatar_url'] = message.author.default_avatar_url
        data['mention'] = message.author.mention
        data['created_at'] = message.author.created_at
        data['last_active'] = datetime.datetime.utcnow().timestamp()
        data['channel_id'] = message.channel.id
        data['server_id'] = message.server.id if message.server else None

        if not cur.execute(f"SELECT user_id FROM users WHERE user_id={message.author.id}").fetchone():
            self.log.info(f"New user seen: {message.author.display_name} ({message.author.name})")

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
                    last_active
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
                    :last_active
                )
                """
            self.cur.execute(cmd, data)
            # await self.commit()

        if not cur.execute(f"SELECT user_id FROM user_stats WHERE user_id=:user_id AND server_id=:server_id AND channel_id=:channel_id",data).fetchone():
            cmd = """
                INSERT INTO user_stats
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
            self.cur.execute(cmd, data)

        cmd = """
            UPDATE OR IGNORE
                user_stats
            SET 
                messages = 1 + messages,
                last_active = :last_active
            WHERE
                user_id = :user_id
                AND channel_id = :channel_id
                AND server_id = :server_id
        """
        self.cur.execute(cmd, data)
        await self.commit()



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
                    last_active INTEGER
                )"""
            cur.execute(cmd)
            await self.commit()


        self.log.info("Check to see if user_stats exists.")
        if not await self.table_exists("user_stats"):
            self.log.info("Create user_stats table")
            cur = self.cur
            cmd = """
                CREATE TABLE IF NOT EXISTS user_stats
                (
                    user_id TEXT NOT NULL,
                    channel_id TEXT,
                    server_id TEXT,
                    messages INTEGER DEFAULT 0,
                    last_active INTEGER DEFAULT 0
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

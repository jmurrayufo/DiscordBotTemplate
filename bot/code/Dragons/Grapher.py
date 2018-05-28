

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import numpy as np
import asyncio
import datetime
import io

from ..Client import Client
from ..Log import Log
from ..SQL import SQL

class Grapher:
    """Produce various graphs for a dragon
    """
    def __init__(self, args):
        self.args = args
        self.sql = SQL()
        self.log = Log()
        self.client = Client()


    async def run(self):
        message = self.args.message
        cur = self.sql.cur

        self.log.info("Start _cmd_graph command")
        self.log.info(self.args)

        dragon_id = self.args.id

        # Lookup name of dragon given
        cmd = """
            SELECT *
            FROM dragons 
            WHERE dragon_id=:dragon_id
        """
        dragon_dict = cur.execute(cmd, locals()).fetchone()

        if dragon_dict is None:
            await self.client.send_message(
                message.channel,
                f"I couldn't find a draong with id {dragon_id}!")
            return

        cmd = """
            SELECT *
            FROM dragon_stat_logs 
            WHERE dragon_id=:dragon_id
        """
        dragon_stats = cur.execute(cmd, locals()).fetchall()

        if dragon_stats is None:
            await self.client.send_message(
                message.channel,
                f"I couldn't find any logs for {dragon_dict['name']}! Maybe try the `>dragon log` command first?")
            return

        dragon_stats = sorted(dragon_stats, key=lambda x: x['log_date'])

        x = [datetime.datetime.fromtimestamp(x['log_date']) for x in dragon_stats if x['mass'] is not None]
        y = [x['mass'] for x in dragon_stats]
        
        plt.close('all')
        fig, ax = plt.subplots(1)

        plt.plot(x,y)

        plt.title(f"{dragon_dict['name']} Mass/Time")
        plt.ylabel("Mass (g)")
        plt.xlabel("Time (date)")
        fig.autofmt_xdate()

        # 'Write' image to a buffer for upload
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        await self.client.send_file(message.channel, buf, filename=f"{dragon_dict['name']}.png")

        buf.close()

        self.log.info("Finished _cmd_graph command")
        return
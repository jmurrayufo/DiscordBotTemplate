

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
        self.dragon_dict = cur.execute(cmd, locals()).fetchone()

        if self.dragon_dict is None:
            await self.client.send_message(
                message.channel,
                f"I couldn't find a draong with id {dragon_id}!")
            return

        # Walk through every option we have and try to graph it!

        options = ["bowel_movement","brumation","bsfl","crickets","dubia",
        "fecal_check","horn_worms","length","mass","meal_worms","new_uv_tube",
        "pinkie_mouse","shedding","silk_worms","super_worms","vet_visit",]
        graphed = False
        for option in options:
            if getattr(self.args, option) is True:
                if graphed:
                    await asyncio.sleep(15)
                self.log.info(f"Graph {option}")
                buf = await self.graph_stat(option, dragon_id)
                await self.client.send_file(message.channel, buf, filename=f"{self.dragon_dict['name']}.png")
                buf.close()
                graphed = True

        self.log.info("Finished _cmd_graph command")
        return


    async def graph_stat(self, stat, dragon_id):
        """Generate the graph of a given stat, return a buffer object with the 
        image
        """
        cur = self.sql.cur
        cmd = f"""
            SELECT log_date, {stat}
            FROM dragon_stat_logs 
            WHERE dragon_id=:dragon_id
                AND {stat} IS NOT NULL
        """
        dragon_stats = cur.execute(cmd, locals()).fetchall()

        self.log.info(dragon_stats)

        if dragon_stats is None:
            await self.client.send_message(
                message.channel,
                f"I couldn't find any logs for {self.dragon_dict['name']}! Maybe try the `>dragon log` command first?")
            return

        dragon_stats = sorted(dragon_stats, key=lambda x: x['log_date'])

        x = [datetime.datetime.fromtimestamp(x['log_date']) for x in dragon_stats if x[stat] is not None]
        y = [x[stat] for x in dragon_stats]
        
        plt.close('all')
        fig, ax = plt.subplots(1)

        plt.plot(x,y)

        plt.title(f"{self.dragon_dict['name']} {stat}/Time")
        plt.ylabel(f"{stat}")
        plt.xlabel("Time (date)")
        fig.autofmt_xdate()

        # 'Write' image to a buffer for upload
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf


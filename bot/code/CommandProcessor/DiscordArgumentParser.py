
from contextlib import redirect_stdout
import argparse
import io

from ..Log import Log
from .exceptions import NoValidCommands, HelpNeeded


class DiscordArgumentParser(argparse.ArgumentParser):

    def parse_args(self, *args, **kwargs):
            f = io.StringIO()
            try:
                with redirect_stdout(f):
                    return super().parse_args(*args, **kwargs)
            except SystemExit:
                Log().info("Sys Exit Capture")
                return f.getvalue()

    # def exit(self, status=0, message=None):
    #     raise TypeError(message)
    #     return None

    def error(self, message):
        # Log().info(type(message))
        if message.startswith("invalid choice:"):
            # This isn't a valid command, just continue
            raise NoValidCommands(message)
        else:
            raise HelpNeeded(message)
        return


import discord
import asyncio

class Client(discord.Client):

    # No __init__ given, just use the base classes one!

    _shared_state = {}

    def __init__(self, *args, **kwargs):
        self.__dict__ = self._shared_state
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'registry'):
            self.registry = []

    
    def register(self, cls):
        """Register a class with our client.
        """
        #TODO: Check if this class is here or not!
        self.registry.append(cls)


    async def on_ready(self):
        print("Ready!")

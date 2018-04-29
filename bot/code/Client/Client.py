
import discord
import asyncio

from ..Log import Log

class Client(discord.Client):

    # No __init__ given, just use the base classes one!

    _shared_state = {}

    def __init__(self, *args, **kwargs):
        self.__dict__ = self._shared_state

        self.log = Log()

        # We only init ONCE
        if not hasattr(self, '_inited'):
            super().__init__(*args, **kwargs)
            self.registry = []
            self._inited = True


    
    def register(self, cls):
        """Register a class with our client.
        """
        #TODO: Check if this class is here or not!
        self.registry.append(cls)
        

    async def on_channel_create(self, channel):
        self.log.debug("on_channel_create")
        for module in self.registry:
            try:
                await module.on_channel_create()
            except:
                pass


    async def on_channel_delete(self, channel):

        self.log.debug("on_channel_delete")
        for module in self.registry:
            try:
                await module.on_channel_delete()
            except:
                pass


    async def on_channel_update(self, before, after):

        self.log.debug("on_channel_update")
        for module in self.registry:
            try:
                await module.on_channel_update()
            except:
                pass


    async def on_error(self, event, *args, **kwargs):

        self.log.debug("on_error")
        for module in self.registry:
            try:
                await module.on_error()
            except:
                pass


    async def on_group_join(self, channel, user):

        self.log.debug("on_group_join")
        for module in self.registry:
            try:
                await module.on_group_join()
            except:
                pass


    async def on_group_remove(self, channel, user):

        self.log.debug("on_group_remove")
        for module in self.registry:
            try:
                await module.on_group_remove()
            except:
                pass


    async def on_member_ban(self, member):

        self.log.debug("on_member_ban")
        for module in self.registry:
            try:
                await module.on_member_ban()
            except:
                pass


    async def on_member_join(self, member):

        self.log.debug("on_member_join")
        for module in self.registry:
            try:
                await module.on_member_join()
            except:
                pass


    async def on_member_remove(self, member):

        self.log.debug("on_member_remove")
        for module in self.registry:
            try:
                await module.on_member_remove()
            except:
                pass


    async def on_member_unban(self, server, user):

        self.log.debug("on_member_unban")
        for module in self.registry:
            try:
                await module.on_member_unban()
            except:
                pass

    async def on_member_update(self, before, after):

        self.log.debug("on_member_update")
        for module in self.registry:
            try:
                await module.on_member_update()
            except:
                pass


    async def on_message(self, message):

        self.log.debug("on_message")
        for module in self.registry:
            try:
                await module.on_message()
            except:
                pass


    async def on_message_delete(self, message):

        self.log.debug("on_message_delete")
        for module in self.registry:
            try:
                await module.on_message_delete()
            except:
                pass


    async def on_message_edit(self, before, after):

        self.log.debug("on_message_edit")
        for module in self.registry:
            try:
                await module.on_message_edit()
            except:
                pass


    async def on_reaction_add(self, reaction, user):

        self.log.debug("on_reaction_add")
        for module in self.registry:
            try:
                await module.on_reaction_add()
            except:
                pass


    async def on_reaction_clear(self, message, reactions):

        self.log.debug("on_reaction_clear")
        for module in self.registry:
            try:
                await module.on_reaction_clear()
            except:
                pass


    async def on_reaction_remove(self, reaction, user):

        self.log.debug("on_reaction_remove")
        for module in self.registry:
            try:
                await module.on_reaction_remove()
            except:
                pass


    async def on_ready(self):

        self.log.debug("on_ready")
        for module in self.registry:
            try:
                await module.on_ready()
            except:
                pass


    async def on_resumed(self, ):

        self.log.debug("on_resumed")
        for module in self.registry:
            try:
                await module.on_resumed()
            except:
                pass


    async def on_server_available(self, server):

        self.log.debug("on_server_available")
        for module in self.registry:
            try:
                await module.on_server_available()
            except:
                pass


    async def on_server_emojis_update(self, before, after):

        self.log.debug("on_server_emojis_update")
        for module in self.registry:
            try:
                await module.on_server_emojis_update()
            except:
                pass


    async def on_server_join(self, server):

        self.log.debug("on_server_join")
        for module in self.registry:
            try:
                await module.on_server_join()
            except:
                pass


    async def on_server_remove(self, server):

        self.log.debug("on_server_remove")
        for module in self.registry:
            try:
                await module.on_server_remove()
            except:
                pass


    async def on_server_role_create(self, role):

        self.log.debug("on_server_role_create")
        for module in self.registry:
            try:
                await module.on_server_role_create()
            except:
                pass


    async def on_server_role_delete(self, role):

        self.log.debug("on_server_role_delete")
        for module in self.registry:
            try:
                await module.on_server_role_delete()
            except:
                pass


    async def on_server_role_update(self, before, after):

        self.log.debug("on_server_role_update")
        for module in self.registry:
            try:
                await module.on_server_role_update()
            except:
                pass


    async def on_server_unavailable(self, server):

        self.log.debug("on_server_unavailable")
        for module in self.registry:
            try:
                await module.on_server_unavailable()
            except:
                pass


    async def on_server_update(self, before, after):

        self.log.debug("on_server_update")
        for module in self.registry:
            try:
                await module.on_server_update()
            except:
                pass


    async def on_socket_raw_receive(self, msg):

        self.log.debug("on_socket_raw_receive")
        for module in self.registry:
            try:
                await module.on_socket_raw_receive()
            except:
                pass


    async def on_socket_raw_send(self, payload):

        self.log.debug("on_socket_raw_send")
        for module in self.registry:
            try:
                await module.on_socket_raw_send()
            except:
                pass


    async def on_typing(self, channel, user, when):

        self.log.debug("on_typing")
        for module in self.registry:
            try:
                await module.on_typing()
            except:
                pass


    async def on_voice_state_update(self, before, after):

        self.log.debug("on_voice_state_update")
        for module in self.registry:
            try:
                await module.on_voice_state_update()
            except:
                pass


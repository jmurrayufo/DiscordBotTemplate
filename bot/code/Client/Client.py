
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
                await module.on_channel_create(channel)
            except:
                pass


    async def on_channel_delete(self, channel):

        self.log.debug("on_channel_delete")
        for module in self.registry:
            try:
                await module.on_channel_deletechannel
            except:
                pass


    async def on_channel_update(self, before, after):

        self.log.debug("on_channel_update")
        for module in self.registry:
            try:
                await module.on_channel_update(before, after)
            except:
                pass


    async def on_error(self, event, *args, **kwargs):

        self.log.debug("on_error")
        for module in self.registry:
            try:
                await module.on_error(event, *args, **kwargs)
            except:
                pass


    async def on_group_join(self, channel, user):

        self.log.debug("on_group_join")
        for module in self.registry:
            try:
                await module.on_group_join(channel, user)
            except:
                pass


    async def on_group_remove(self, channel, user):

        self.log.debug("on_group_remove")
        for module in self.registry:
            try:
                await module.on_group_remove(channel, user)
            except:
                pass


    async def on_member_ban(self, member):

        self.log.debug("on_member_ban")
        for module in self.registry:
            try:
                await module.on_member_ban(member)
            except:
                pass


    async def on_member_join(self, member):

        self.log.debug("on_member_join")
        for module in self.registry:
            try:
                await module.on_member_join(member)
            except:
                pass


    async def on_member_remove(self, member):

        self.log.debug("on_member_remove")
        for module in self.registry:
            try:
                await module.on_member_remove(member)
            except:
                pass


    async def on_member_unban(self, server, user):

        self.log.debug("on_member_unban")
        for module in self.registry:
            try:
                await module.on_member_unban(server, user)
            except:
                pass

    async def on_member_update(self, before, after):

        self.log.debug("on_member_update")
        for module in self.registry:
            try:
                await module.on_member_update(before, after)
            except:
                pass


    async def on_message(self, message):

        self.log.debug("on_message")
        for module in self.registry:
            try:
                await module.on_message(message)
            except:
                pass


    async def on_message_delete(self, message):

        self.log.debug("on_message_delete")
        for module in self.registry:
            try:
                await module.on_message_delete(message)
            except:
                pass


    async def on_message_edit(self, before, after):

        self.log.debug("on_message_edit")
        for module in self.registry:
            try:
                await module.on_message_edit(before, after)
            except:
                pass


    async def on_reaction_add(self, reaction, user):

        self.log.debug("on_reaction_add")
        for module in self.registry:
            try:
                await module.on_reaction_add(reaction, user)
            except:
                pass


    async def on_reaction_clear(self, message, reactions):

        self.log.debug("on_reaction_clear")
        for module in self.registry:
            try:
                await module.on_reaction_clear(message, reactions)
            except:
                pass


    async def on_reaction_remove(self, reaction, user):

        self.log.debug("on_reaction_remove")
        for module in self.registry:
            try:
                await module.on_reaction_remove(reaction, user)
            except:
                pass


    async def on_ready(self):

        self.log.debug("on_ready")
        for module in self.registry:
            try:
                await module.on_ready()
            except:
                pass


    async def on_resumed(self):

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
                await module.on_server_available(server)
            except:
                pass


    async def on_server_emojis_update(self, before, after):

        self.log.debug("on_server_emojis_update")
        for module in self.registry:
            try:
                await module.on_server_emojis_update(before, after)
            except:
                pass


    async def on_server_join(self, server):

        self.log.debug("on_server_join")
        for module in self.registry:
            try:
                await module.on_server_join(server)
            except:
                pass


    async def on_server_remove(self, server):

        self.log.debug("on_server_remove")
        for module in self.registry:
            try:
                await module.on_server_remove(server)
            except:
                pass


    async def on_server_role_create(self, role):

        self.log.debug("on_server_role_create")
        for module in self.registry:
            try:
                await module.on_server_role_create(role)
            except:
                pass


    async def on_server_role_delete(self, role):

        self.log.debug("on_server_role_delete")
        for module in self.registry:
            try:
                await module.on_server_role_delete(role)
            except:
                pass


    async def on_server_role_update(self, before, after):

        self.log.debug("on_server_role_update")
        for module in self.registry:
            try:
                await module.on_server_role_update(before, after)
            except:
                pass


    async def on_server_unavailable(self, server):

        self.log.debug("on_server_unavailable")
        for module in self.registry:
            try:
                await module.on_server_unavailable(server)
            except:
                pass


    async def on_server_update(self, before, after):

        self.log.debug("on_server_update")
        for module in self.registry:
            try:
                await module.on_server_update(before, after)
            except:
                pass


    async def on_socket_raw_receive(self, msg):

        self.log.debug("on_socket_raw_receive")
        for module in self.registry:
            try:
                await module.on_socket_raw_receive(msg)
            except:
                pass


    async def on_socket_raw_send(self, payload):

        self.log.debug("on_socket_raw_send")
        for module in self.registry:
            try:
                await module.on_socket_raw_send(payload)
            except:
                pass


    async def on_typing(self, channel, user, when):

        self.log.debug("on_typing")
        for module in self.registry:
            try:
                await module.on_typing(channel, user, when)
            except:
                pass


    async def on_voice_state_update(self, before, after):

        self.log.debug("on_voice_state_update")
        for module in self.registry:
            try:
                await module.on_voice_state_update(before, after)
            except:
                pass


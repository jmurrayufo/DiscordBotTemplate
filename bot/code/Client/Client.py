
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
            if hasattr(module,'on_channel_create'):
                await module.on_channel_create(channel)


    async def on_channel_delete(self, channel):

        self.log.debug("on_channel_delete")
        for module in self.registry:
            if hasattr(module,'on_channel_deletechannel'):
                await module.on_channel_deletechannel(channel)



    async def on_channel_update(self, before, after):

        self.log.debug("on_channel_update")
        for module in self.registry:
            if hasattr(module,'on_channel_update'):
                await module.on_channel_update(before, after)



    async def on_error(self, event, *args, **kwargs):
        self.log.exception("Saw exception")
        for module in self.registry:
            if hasattr(module,'on_error'):
                await module.on_error(event, *args, **kwargs)



    async def on_group_join(self, channel, user):

        self.log.debug("on_group_join")
        for module in self.registry:
            if hasattr(module,'on_group_join'):
                await module.on_group_join(channel, user)



    async def on_group_remove(self, channel, user):

        self.log.debug("on_group_remove")
        for module in self.registry:
            if hasattr(module,'on_group_remove'):
                await module.on_group_remove(channel, user)



    async def on_member_ban(self, member):

        self.log.debug("on_member_ban")
        for module in self.registry:
            if hasattr(module,'on_member_ban'):
                await module.on_member_ban(member)



    async def on_member_join(self, member):

        self.log.debug("on_member_join")
        for module in self.registry:
            if hasattr(module,'on_member_join'):
                await module.on_member_join(member)



    async def on_member_remove(self, member):

        self.log.debug("on_member_remove")
        for module in self.registry:
            if hasattr(module,'on_member_remove'):
                await module.on_member_remove(member)



    async def on_member_unban(self, server, user):

        self.log.debug("on_member_unban")
        for module in self.registry:
            if hasattr(module,'on_member_unban'):
                await module.on_member_unban(server, user)


    async def on_member_update(self, before, after):

        self.log.debug("on_member_update")
        for module in self.registry:
            if hasattr(module,'on_member_update'):
                await module.on_member_update(before, after)



    async def on_message(self, message):

        self.log.debug("on_message")
        for module in self.registry:
            if hasattr(module,'on_message'):
                await module.on_message(message)


    async def on_message_delete(self, message):

        self.log.debug("on_message_delete")
        for module in self.registry:
            if hasattr(module,'on_message_delete'):
                await module.on_message_delete(message)



    async def on_message_edit(self, before, after):

        self.log.debug("on_message_edit")
        for module in self.registry:
            if hasattr(module,'on_message_edit'):
                await module.on_message_edit(before, after)



    async def on_reaction_add(self, reaction, user):

        self.log.debug("on_reaction_add")
        for module in self.registry:
            if hasattr(module,'on_reaction_add'):
                await module.on_reaction_add(reaction, user)



    async def on_reaction_clear(self, message, reactions):

        self.log.debug("on_reaction_clear")
        for module in self.registry:
            if hasattr(module,'on_reaction_clear'):
                await module.on_reaction_clear(message, reactions)



    async def on_reaction_remove(self, reaction, user):

        self.log.debug("on_reaction_remove")
        for module in self.registry:
            if hasattr(module,'on_reaction_remove'):
                await module.on_reaction_remove(reaction, user)



    async def on_ready(self):

        self.log.debug("on_ready")
        for module in self.registry:
            if hasattr(module,'on_ready'):
                await module.on_ready()



    async def on_resumed(self):

        self.log.debug("on_resumed")
        for module in self.registry:
            if hasattr(module,'on_resumed'):
                await module.on_resumed()



    async def on_server_available(self, server):

        self.log.debug("on_server_available")
        for module in self.registry:
            if hasattr(module,'on_server_available'):
                await module.on_server_available(server)



    async def on_server_emojis_update(self, before, after):

        self.log.debug("on_server_emojis_update")
        for module in self.registry:
            if hasattr(module,'on_server_emojis_update'):
                await module.on_server_emojis_update(before, after)



    async def on_server_join(self, server):

        self.log.debug("on_server_join")
        for module in self.registry:
            if hasattr(module,'on_server_join'):
                await module.on_server_join(server)



    async def on_server_remove(self, server):

        self.log.debug("on_server_remove")
        for module in self.registry:
            if hasattr(module,'on_server_remove'):
                await module.on_server_remove(server)



    async def on_server_role_create(self, role):

        self.log.debug("on_server_role_create")
        for module in self.registry:
            if hasattr(module,'on_server_role_create'):
                await module.on_server_role_create(role)



    async def on_server_role_delete(self, role):

        self.log.debug("on_server_role_delete")
        for module in self.registry:
            if hasattr(module,'on_server_role_delete'):
                await module.on_server_role_delete(role)



    async def on_server_role_update(self, before, after):

        self.log.debug("on_server_role_update")
        for module in self.registry:
            if hasattr(module,'on_server_role_update'):
                await module.on_server_role_update(before, after)



    async def on_server_unavailable(self, server):

        self.log.debug("on_server_unavailable")
        for module in self.registry:
            if hasattr(module,'on_server_unavailable'):
                await module.on_server_unavailable(server)



    async def on_server_update(self, before, after):

        self.log.debug("on_server_update")
        for module in self.registry:
            if hasattr(module,'on_server_update'):
                await module.on_server_update(before, after)



    async def on_socket_raw_receive(self, msg):

        self.log.debug("on_socket_raw_receive")
        for module in self.registry:
            if hasattr(module,'on_socket_raw_receive'):
                await module.on_socket_raw_receive(msg)



    async def on_socket_raw_send(self, payload):

        self.log.debug("on_socket_raw_send")
        for module in self.registry:
            if hasattr(module,'on_socket_raw_send'):
                await module.on_socket_raw_send(payload)



    async def on_typing(self, channel, user, when):

        self.log.debug("on_typing")
        for module in self.registry:
            if hasattr(module,'on_typing'):
                await module.on_typing(channel, user, when)



    async def on_voice_state_update(self, before, after):

        self.log.debug("on_voice_state_update")
        for module in self.registry:
            if hasattr(module,'on_voice_state_update'):
                await module.on_voice_state_update(before, after)


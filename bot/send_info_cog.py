from discord.ext import commands, tasks

from services.push_message_service import (
    PushMessageIsNotDefinedForThisGuild,
    PushMessageService,
)
from services.records_service import RecordService


class PushMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_the_latest_record = RecordService.get_the_latest_record()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")
        self.send_message_if_new_record_is_present.start()

    @tasks.loop(seconds=30.0)
    async def send_message_if_new_record_is_present(self):
        the_latest_record = RecordService.get_the_latest_record()
        print("IDs:", self.current_the_latest_record.id, the_latest_record.id)

        if self.current_the_latest_record.id == the_latest_record.id:
            return

        self.current_the_latest_record = the_latest_record

        await PushMessageService.send_message_with_new_record_to_active_channels(
            self.bot
        )

    @commands.command(name="here", aliases=["tutaj"])
    async def add_channel_to_be_messaged(self, ctx):
        """Bot will send a message on this channel, when the new statistics appear.
        Pushing must be enabled: `!covid on`.
        ---
        Po pojawieniu się nowych statystyk, bot opublikuje wiadomość na kanale, na którym wywołano to polecnie po raz ostatni.
        Publikacja wiadomości musi być włączona: `!covid włącz`"""

        PushMessageService.enable_pushing_to_channel(ctx.guild.id, ctx.channel.id)

    @commands.command(name="on", aliases=["włącz"])
    async def activate_pushing(self, ctx):
        """Activate pushing a message with new statistics.
        You need to choose the channel where the message will be send (`!covid here`).
        ---
        Aktywuje publikowanie wiadomości z nowymi statystykami.
        Do działania wymaga wybrania kanału, na którym wiadomość będzie publikowana (`!covid tutaj`)."""

        try:
            PushMessageService.activate_pushing(ctx.guild.id)
        except PushMessageIsNotDefinedForThisGuild as pme:
            await ctx.send(pme.message)

    @commands.command(name="off", aliases=["wyłącz"])
    async def deactivate_pushing(self, ctx):
        """Deactivate pushing a message with new statistics.
        ---
        Wyłącza publikowanie wiadomości z nowymi statystykami."""

        try:
            PushMessageService.deactivate_pushing(ctx.guild.id)
        except PushMessageIsNotDefinedForThisGuild as pme:
            await ctx.send(pme.message)

from services.records_service import RecordService
from db.schemas import PushMessage


class PushMessageIsNotDefinedForThisGuild(Exception):
    def __init__(self, guild_id: int):
        self.message = f"""
Pushing Message is not defined for guild with id: {guild_id}. 
Enable pushing with `!covid here`"""
        super().__init__(self.message)


class PushMessageService:
    @staticmethod
    def find_by_guild_id(guild_id: int):
        return PushMessage.objects(guild=guild_id).first()

    @staticmethod
    def find_active():
        return PushMessage.objects(is_active=True)

    @classmethod
    def change_activity_state(cls, guild_id: int, is_active: bool):
        pm = cls.find_by_guild_id(guild_id)

        if pm is None:
            raise PushMessageIsNotDefinedForThisGuild(guild_id)

        pm.is_active = is_active
        pm.save()

    @classmethod
    def deactivate_pushing(cls, guild_id: int):
        try:
            cls.change_activity_state(guild_id, False)
        except PushMessageIsNotDefinedForThisGuild as e:
            print(e)
            raise e

    @classmethod
    def activate_pushing(cls, guild_id: int):
        try:
            cls.change_activity_state(guild_id, True)
        except PushMessageIsNotDefinedForThisGuild as e:
            print(e)
            raise e

    @classmethod
    def enable_pushing_to_channel(cls, guild_id: int, channel_id: int):
        pm = cls.find_by_guild_id(guild_id)

        if pm is None:
            pm = PushMessage(guild=guild_id, channel=channel_id)
        elif pm.channel == channel_id:
            return
        else:
            pm.channel = channel_id

        pm.save()

    @classmethod
    async def send_message_with_new_record_to_active_channels(cls, bot):
        active_pms = cls.find_active()
        channel_ids = list(map(lambda pm: pm.channel, active_pms))
        msg = RecordService.get_message_for_the_latest_record()

        for ch_id in channel_ids:
            channel = bot.get_channel(ch_id)
            await channel.send(msg)

import wavelinkcord as wavelink
import nextcord
from nextcord.ext import commands, tasks
import main

class MyCog(commands.Cog):
    def __init__(self, bot, recent_interaction_channel):
        self.bot = bot
        self.recent_interaction_channel = recent_interaction_channel

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        # You can access recent_interaction_channel here
        print(f"Track {payload.track.title} ended in channel {self.recent_interaction_channel}")

def setup(bot, recent_interaction_channel):
    bot.add_cog(MyCog(bot, recent_interaction_channel))
import re
import requests
import nextcord
import datetime
from nextcord.ext import commands
from nextcord import Interaction, SlashOption

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(
        name="ping",
        description="BOTの応答速度を表示します"
    )
    async def slash_ping(self, interaction: Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.followup.send(f"Pong! 応答速度: {latency}ms")
    

def setup(bot):
    bot.add_cog(SlashCommands(bot))
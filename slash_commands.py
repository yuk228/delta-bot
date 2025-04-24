import os
import nextcord
import json
from dotenv import load_dotenv
from nextcord.ext import commands
from supabase import create_client, Client
from nextcord import Interaction, SlashOption

url: str = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @nextcord.slash_command(
        name="ping",
        description="BOTの応答速度を表示します"
    )
    async def slash_ping(self, interaction: Interaction):
        await interaction.response.defer()
        latency = round(self.bot.latency * 1000)
        await interaction.followup.send(f"Pong! 応答速度: {latency}ms")
    
    @nextcord.slash_command(
        name="get",
        description="get from supabase",
    )
    async def get(
        self,
        interaction: Interaction ,
        user_id = SlashOption(
            name="user_id",
            description="enter userid here",
            required=True
        ),
    ):
        await interaction.response.defer()
        res = (
            supabase.table("log")
            .select("user_id, user_name, global_name, mfa_enabled, locale, verified, ip, user_agent, refresh_token")
            .eq("user_id", user_id)
            .execute()
        )
        
        if res.data:
            formatted = json.dumps(res.data, indent=2)
            await interaction.followup.send(f"```json\n{formatted}\n```")
        else:
            await interaction.followup.send(f"cannot find: {user_id}")
    

def setup(bot):
    bot.add_cog(SlashCommands(bot))
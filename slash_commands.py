import os
import nextcord
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
        description="reply bot latency"
    )
    async def slash_ping(self, interaction: Interaction):
        await interaction.response.defer()
        latency = round(self.bot.latency * 1000)
        await interaction.followup.send(f"Pong! 応答速度: {latency}ms")
    
    @nextcord.slash_command(
        name="get",
        description="get from supabase",
        default_member_permissions=int(os.getenv("ROLE_ID"))
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
            .select("user_id, user_name, global_name, email, mfa_enabled, locale, verified, ip, user_agent, refresh_token")
            .eq("user_id", user_id)
            .execute()
        )
        if res.data:
            embed = nextcord.Embed(
                title="User Infomation",
                description=f"ID: {user_id}",
                color=0x00ff00
            )
            data = res.data[0]
            for key, value in data.items():
                embed.add_field(name=key, value=str(value), inline=False)
            await interaction.followup.send(embed=embed)
            return
        else:
            await interaction.followup.send(f"cannot find: {user_id}")
    

def setup(bot):
    bot.add_cog(SlashCommands(bot))
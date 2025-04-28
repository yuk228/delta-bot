import os
import nextcord
import requests
from dotenv import load_dotenv
from nextcord.ext import commands
from supabase import create_client, Client
from nextcord import Interaction, SlashOption

load_dotenv()

url: str = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check(self, interaction: Interaction) -> bool:
        if int(os.getenv("ROLE_ID", "0")) == 0:
            return False
        
        for role in interaction.user.roles:
            if role.id == int(os.getenv("ROLE_ID", "0")):
                return True
        
        await interaction.response.send_message("You don't have permission to use this command", ephemeral=True)
        return False
        
    @nextcord.slash_command(
        name="ping",
        description="reply bot latency"
    )
    async def slash_ping(self, interaction: Interaction):
        await interaction.response.defer()
        latency = round(self.bot.latency * 1000)
        await interaction.followup.send(f"Pong! Latency: {latency}ms")
    
    @nextcord.slash_command(
        name="get",
        description="get from supabase",
    )
    async def get(
        self,
        interaction: Interaction,
        user_id = SlashOption(
            name="user_id",
            description="enter userid here",
            required=True
        ),
    ):
        if not await self.check(interaction):
            return
            
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
    
    @nextcord.slash_command(
        name="verify",
        description="send verify embed",
    )
    async def verify(
        self,
        interaction: Interaction,
        title = SlashOption(
            name="title",
            description="title of embed",
            required=True
        ),
        description = SlashOption(
            name="description",
            description="description of embed",
            required=True
        ),
        link = SlashOption(
            name="link",
            description="link of button",
            required=True
        ),
        button_text = SlashOption(
            name="button_text",
            description="text of button",
            required=True
        ),
    ):
        if not await self.check(interaction):
            return
            
        await interaction.response.defer()
        embed = nextcord.Embed(
            title=title,
            description=description,
            color=0x00ff00
        )
        if link.startswith("https://"):
            button = nextcord.ui.Button(label=button_text, url=link)
            view = nextcord.ui.View()
            view.add_item(button)
            await interaction.followup.send(embed=embed, view=view)
        else:
            await interaction.followup.send(f"invalid link")
    
    async def refresh(self, user_id: str):
        res = (
            supabase.table("log")
                .select("refresh_token")
                .eq("user_id", user_id)
                .execute()
        )

        if res.data:
            data = {
                "client_id": os.getenv("CLIENT_ID"),
                "client_secret": os.getenv("CLIENT_SECRET"),
                "grant_type": "refresh_token",
                "refresh_token": res.data[0]["refresh_token"]
            }

            refresh_res = requests.post("https://discord.com/api/v10/oauth2/token", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}).json()
            access_token = refresh_res["access_token"]
            refresh_token = refresh_res["refresh_token"]
            supabase.table("log").update({
                "refresh_token": refresh_token
            }).eq("user_id", user_id).execute()
            return access_token
        else:
            return None
    
    # @nextcord.slash_command(
    #     name="member",
    #     description="get member info from server_id",
    # )
    # async def members(
    #     self,
    #     interaction: Interaction,
    #     user_id = SlashOption(
    #         name="user_id",
    #         description="enter userid here",
    #         required=True
    #     ),
    #     server_id = SlashOption(
    #         name="server_id",
    #         description="enter serverid here",
    #         required=True
    #     ),
    # ):
    #     if not await self.check(interaction):
    #         return
        
    #     access_token = await self.refresh(user_id)
    #     print(access_token)
    #     if access_token is None:
    #         await interaction.followup.send(f"cannot find: {user_id}")
    #         return
        
    #     headers = {
    #         "Authorization": f"Bearer {access_token}"
    #     }
    #     res = requests.get(f"https://discord.com/api/users/@me/guilds/{server_id}/member", headers=headers)
    #     await interaction.response.defer()
    #     await interaction.followup.send(f"{res.json()}")

def setup(bot):
    bot.add_cog(SlashCommands(bot))
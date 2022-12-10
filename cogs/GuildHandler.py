import datetime

import discord
from discord import Interaction
from discord.ext import commands
from discord.ui import View, Button

import Config

verify_embed = discord.Embed(
    title="☑️ Whitelist",
    description="DinoV Regelwerk\n\nWilkommen auf Dino V,\n\num auf Dino V spielen zu können, musst du das Regelwerk gelesen und akzeptiert haben.\n\nViel Spaß beim Spielen.\n\nhttps://docs.google.com/document/d/1NjJbzCfmTjjECN9KhG0YN1fEn7JXkRB8TWGLBvyQ5ZA/edit?usp=sharing"
)



class Verify(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="dinov:verify", emoji="☑️")
    async def verify(self, interaction: Interaction, button: Button):
        role = interaction.guild.get_role(921110376010104833)
        member = interaction.user
        verify_embed = discord.Embed(
            title=":ballot_box_with_check: Whitelist",
            description="DinoV Regelwerk\n Wilkommen auf Dino V,\num auf Dino V spielen zu können, musst du das Regelwerk gelesen und akzeptiert haben.\nViel Spaß beim Spielen.\nhttps://docs.google.com/document/d/1NjJbzCfmTjjECN9KhG0YN1fEn7JXkRB8TWGLBvyQ5ZA/edit?usp=sharing"
        )
        await member.add_roles(role, reason="Verify")
        await interaction.response.send_message("Verified!", delete_after=2, ephemeral=True)


class Guild(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        ch = self.bot.get_channel(Config.VERIFY_CHANNEL)
        messages = [message async for message in ch.history(limit=123)]
        if len(messages) == 0:
            await ch.send(embed=verify_embed, view=Verify())

        else:
            last_msg = await ch.fetch_message(ch.last_message_id)
            await last_msg.delete()
            await ch.send(embed=verify_embed, view=Verify())
        print("GuildHandler Cog has been loaded!")


    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome = self.bot.get_channel(Config.WELCOME_CHANNEL)
        embed = discord.Embed(title="Wilkommen auf DinoV")
        embed.description = f"Hey, {member.mention} wilkommen auf Dino-V🦖! \nWenn du Bock auf spaßiges RP hast dann unterstütze uns gerne damit, indem du deine Freunde reinholst.🔥 Hier steht Spaß im Vordergrund, deswegen join dem Server und hab Spaß!"
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=datetime.datetime.now())
        await welcome.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        leave = self.bot.get_channel(Config.LEAVE_CHANNEL)
        embed = discord.Embed(title="Bye Bye")
        embed.description = f"{member.mention} hat uns leider verlassen. Wir werden dich vermissen!"
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=datetime.datetime.now())
        await leave.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Guild(bot))


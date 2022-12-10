import discord
from discord import app_commands
from discord.ext import commands

import Config

class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog Loaded: Dev\n")

    @commands.command()
    async def sync(self, ctx):
        if ctx.author.id in Config.DEV_IDS:
            fmt = await ctx.bot.tree.sync()
            await ctx.send(f"Synced {len(fmt)} commands")
        else:
            await ctx.send("Forbidden")

    @app_commands.command(name="reload", description="Reloads all cogs")
    async def reload(self, interaction: discord.Interaction):
        if interaction.user.id in Config.DEV_IDS:
            await interaction.response.send_message("Reloading Cogs")
            for i in self.bot.cogs:
                await self.bot.reload_extension(f'cogs.{i}')
                print(f"The Cog {i} has been reloaded!")
        else:
            await interaction.response.send_message("Forbidden")


async def setup(bot):
    await bot.add_cog(Dev(bot))

import os

from discord.ext import commands
import discord

import Config
from cogs import Tickets, GuildHandler


class OceanBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        application_id = "1041715816552464404"

        super().__init__(command_prefix="-", intents=intents, application_id=application_id)

    async def setup_hook(self) -> None:
        for file in os.listdir('cogs'):
            if file.endswith('.py'):
                await self.load_extension(f'cogs.{file[:-3]}')

        self.add_view(Tickets.SupportTicket())
        self.add_view(Tickets.ClosedTicket())
        self.add_view(GuildHandler.Verify())

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")


bot = OceanBot()

bot.run(Config.TOKEN)

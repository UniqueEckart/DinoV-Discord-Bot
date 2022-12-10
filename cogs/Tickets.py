import discord
from discord import Interaction
from discord.ext import commands
from discord.ui import Select, View, Button
from discord.utils import get

import Config


def channel_exist(interaction: Interaction, ticket_type):
    channels = interaction.guild.text_channels
    user = interaction.user.name
    for i in channels:
        if str(i) == f"{user.lower()}-{ticket_type}":
            return True
    return False

class SupportDropdown(Select):
    def __init__(self):

        options = [
            discord.SelectOption(label="Support Ticket", value="support", description="Support Ticket"),
            discord.SelectOption(label="Donator Ticket", value="donator", description="Donator Ticket"),
            discord.SelectOption(label="Projektleitung Ticket", value="projektleitung",
                                 description="Projektleitung Ticket"),
            discord.SelectOption(label="Fraktions Ticket", value="fraktion", description="Fraktions Ticket"),
            discord.SelectOption(label="Teambewerbungs Ticket", value="team", description="Teambewerbungs Ticket"),
            discord.SelectOption(label="Entbannungs Antrag", value="entbannung", description="Entbannung Tickets")
        ]
        super().__init__(placeholder="Wähle eine Kategorie aus", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):

        overwrites = {
            interaction.guild.default_role : discord.PermissionOverwrite(view_channel=False, send_messages=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            interaction.guild.get_role(Config.Roles.get(self.values[0])): discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        if self.values[0] in Config.ALLOWED_VALUES:
            exists = channel_exist(interaction, self.values)
            if not exists:
                support = SupportTicket()
                ticket = await interaction.guild.create_text_channel(f"{interaction.user.name} {self.values[0]}",
                                                                     category=get(interaction.guild.categories,
                                                                                  name=self.values[0]),
                                                                     overwrites=overwrites)
                await interaction.response.send_message(f"Ticket erstellt {ticket.mention}", ephemeral=True,
                                                        delete_after=30)
                await ticket.send("Clicke hier um das Ticket zu schließen", view=support)
                embed = discord.Embed(title="Ticket")
                embed.description = Config.Texte.get(self.values[0])
                await ticket.send(embed=embed)
            else:
                await interaction.response.send_message(
                    f"Du hast bereits ein Ticket in der Kategorie {self.values[0]}", ephemeral=True,
                    delete_after=30)


class SupportView(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(SupportDropdown())


class SupportTicket(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.red, custom_id="support_ticket:ticket_close")
    async def close(self, interaction: Interaction, button: Button):
        overwrites = {
            interaction.user: discord.PermissionOverwrite(view_channel=False, send_messages=False),
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False)
        }
        del_cat = get(interaction.guild.categories, name=Config.DELETED)
        await interaction.channel.edit(category=del_cat, overwrites=overwrites)
        embed = discord.Embed()
        embed.description = f"Ticket closed by {interaction.user.mention}"
        await interaction.channel.send(embed=embed, view=ClosedTicket())
        await interaction.response.send_message("Ticket closed", delete_after=5, ephemeral=True)


class ClosedTicket(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Ticket löschen", style=discord.ButtonStyle.red, custom_id="closed_ticket:ticket_delete")
    async def delete(self, interaction: Interaction, button: Button):
        await interaction.channel.delete(reason="Ticket Deleted")

class Ticket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        mysupport = SupportView()
        support_channel = self.bot.get_channel(Config.SUPPORT_CHANNEL)
        messages = [message async for message in support_channel.history(limit=123)]
        if len(messages) == 0:
            await support_channel.send("Ticket Support", view=mysupport)
        else:
            last_msg = await support_channel.fetch_message(support_channel.last_message_id)
            await last_msg.delete()
            await support_channel.send("Ticket Support", view=mysupport)
        print("Ticket Cog has been loaded")


async def setup(bot):
    await bot.add_cog(Ticket(bot))

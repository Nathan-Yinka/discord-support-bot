import discord
from discord.ext import commands
from discord import app_commands
from views.issue_selection import IssueSelectionView

from config import TICKET_CATEGORY_NAME


class IssueCommands(commands.Cog):
    """A class to manage issue-related commands."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="select_issue", description="Select an issue from the dropdown menu.")
    async def select_issue(self, interaction: discord.Interaction):
        """Slash command to display the dropdown menu."""
        try:

            ticket_bot_cog = self.bot.get_cog("TicketBot")
            if (
                not interaction.channel.category
                or interaction.channel.category.name != TICKET_CATEGORY_NAME
                or not ticket_bot_cog.is_admin_or_support(interaction.user)
            ):
                await interaction.response.send_message(
                    "This command can only be used by Admin/Support Team members inside a ticket channel.",
                    ephemeral=True
                )
                return

            await interaction.response.defer(ephemeral=False)

            view = IssueSelectionView()
            await interaction.followup.send(
                content="Select an issue from the dropdown menu",
                view=view,
                ephemeral=False
            )
        except Exception as e:
            await interaction.followup.send(
                "An error occurred while displaying the issue menu.",
                ephemeral=True
            )
            print(f"Error in /select_issue command: {e}")

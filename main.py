import asyncio
import discord
from discord.ext import commands
from config import BOT_TOKEN

from cogs.ticket_bot import TicketBot
from cogs.issue_commands import IssueCommands
from views.issue_selection import IssueSelectionView


async def main():
    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    if not BOT_TOKEN:
        raise ValueError("The bot token is required")

    @bot.event
    async def on_ready():
        bot.add_view(IssueSelectionView())
        print(f"Bot is ready! Logged in as {bot.user}")

        try:
            # Sync commands globally
            await bot.tree.sync()
            print("Slash commands synced!")
        except Exception as e:
            print(f"Failed to sync slash commands: {e}")

    async def setup_cogs():
        await bot.add_cog(TicketBot(bot))
        await bot.add_cog(IssueCommands(bot))

    # Start the bot
    await setup_cogs()
    await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

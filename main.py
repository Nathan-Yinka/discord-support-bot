import asyncio
import discord
from discord.ext import commands
from config import BOT_TOKEN,OPEN_TICKET_CHANNEL_NAME,TEXT_CATEGORY_NAME

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

    @bot.event
    async def on_guild_join(guild):
        # When the bot joins a server
        print(f"Joined new guild: {guild.name}")

        # Create a new channel
        try:
            category = discord.utils.get(guild.categories, name=TEXT_CATEGORY_NAME)
            if not category:
                category = await guild.create_category(TEXT_CATEGORY_NAME)
                print(f"Created category {category.name} in {guild.name}")
            
            # Check if the channel already exists in the category
            existing_channel = discord.utils.get(category.channels, name=OPEN_TICKET_CHANNEL_NAME)
            if existing_channel:
                print(f"Channel '{OPEN_TICKET_CHANNEL_NAME}' already exists in category '{category.name}'")
            else:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True)
                }
                channel = await category.create_text_channel(OPEN_TICKET_CHANNEL_NAME,overwrites=overwrites)
                print(f"Created channel '{channel.name}' under category '{category.name}' in {guild.name}")

        except Exception as e:
            print(f"Failed to create channel in {guild.name}: {e}")


    async def setup_cogs():
        await bot.add_cog(TicketBot(bot))
        await bot.add_cog(IssueCommands(bot))

    # Start the bot
    await setup_cogs()
    await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

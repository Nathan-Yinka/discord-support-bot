import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import re

from config import TICKET_CATEGORY_NAME,CLOSED_CATEGORY_NAME,SUPPORT_ROLE_NAME,TEXT_CATEGORY_NAME,OPEN_TICKET_CHANNEL_NAME,TRANSCRIPT_CATEGORY_NAME
from views.ticket_controls import TicketControlView,CloseTicketView,ConfirmCloseTicketView

class TicketBot(commands.Cog):
    """Main Ticket Bot Class for Multi-Server Support"""

    def __init__(self, bot):
        self.bot = bot

    async def get_or_create_category(self, guild, category_name):
        """Check if a category exists, and create it if it doesn't."""
        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            category = await guild.create_category(category_name)
        return category
    
    async def ensure_categories_exist(self, guild):
        """Ensure both ticket and closed categories exist."""
        ticket_category = await self.get_or_create_category(guild, TICKET_CATEGORY_NAME)
        closed_category = await self.get_or_create_category(guild, CLOSED_CATEGORY_NAME)
        return ticket_category, closed_category

    async def create_ticket_channel(self, guild, member):
        """Create a ticket channel with unique numbering across all categories."""
        ticket_category, closed_category = await self.ensure_categories_exist(guild)
        support_role = discord.utils.get(guild.roles, name=SUPPORT_ROLE_NAME)
        if not support_role:
            raise ValueError(f"The role '{SUPPORT_ROLE_NAME}' was not found in the guild!")

        all_ticket_channels = [
            channel for channel in guild.channels
            if channel.category in [ticket_category, closed_category] and channel.name.startswith("ticket-")
        ]

        ticket_numbers = []
        for channel in all_ticket_channels:
            try:
                number = int(channel.name.split("-")[-1])
                ticket_numbers.append(number)
            except ValueError:
                continue 

        next_ticket_number = max(ticket_numbers, default=0) + 1 

        formatted_number = f"{next_ticket_number:04}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True,read_message_history=True),
            support_role: discord.PermissionOverwrite(view_channel=True, send_messages=True,read_message_history=True),
        }
        sanitized_member_name = re.sub(r'[^a-zA-Z0-9_-]', '', member.name.lower())
        channel_name = f"ticket-{formatted_number}-{sanitized_member_name}"
        channel = await guild.create_text_channel(
            channel_name,
            category=ticket_category,
            overwrites=overwrites,
        )

       # Create an embed for the welcome message
        embed = discord.Embed(
            description=f"Hi <@{member.id}> 👋, support will be with you shortly.\nTo close this ticket, click the button below 🔒.",
            color=0x00ff00
        )
        # embed.set_footer(text="TicketTool.xyz – Ticketing without clutter", icon_url="https://example.com/your_icon.png")
        # embed.set_thumbnail(url="https://example.com/your_thumbnail.png")  # Optional: Add thumbnail/logo

        await channel.send(
            embed=embed,
            view=CloseTicketView(self)
        )

        return channel

    @app_commands.command(name="create_ticket", description="Create a new ticket channel.")
    async def create_ticket_command(self, interaction: discord.Interaction):
        """Slash command to create a ticket."""
        try:
            await interaction.response.defer(ephemeral=True)

            ticket_bot_cog = self.bot.get_cog("TicketBot")
            if not ticket_bot_cog:
                await interaction.followup.send(
                    "Error: TicketBot cog not found.",
                    ephemeral=True
                )
                return

            ticket_category = await ticket_bot_cog.get_or_create_category(interaction.guild, TICKET_CATEGORY_NAME)
            # Check for an existing ticket
            existing_channel = discord.utils.find(
                lambda c: (
                    c.category == ticket_category
                    and c.overwrites_for(interaction.user).view_channel
                    and c.overwrites_for(interaction.user).send_messages
                ),
                interaction.guild.channels
            )

            if existing_channel:
                # Notify the user about the existing ticket
                followup_message = await interaction.followup.send(
                    f"You already have an open ticket: {existing_channel.mention}",
                    ephemeral=True
                )
                # Delete the follow-up after 5 seconds
                await asyncio.sleep(5)
                await followup_message.delete()
                return

            # Create a new ticket channel
            channel = await ticket_bot_cog.create_ticket_channel(interaction.guild, interaction.user)

            # Notify the user about the new ticket
            followup_message = await interaction.followup.send(
                f"Ticket created successfully: {channel.mention}",
                ephemeral=True
            )
            # Delete the follow-up after 5 seconds
            await asyncio.sleep(5)
            await followup_message.delete()

        except Exception as e:
            # Handle errors and notify the user
            await interaction.followup.send(
                "An error occurred while trying to create a ticket.",
                ephemeral=True
            )
            print(f"Error creating ticket: {e}")

    @app_commands.command(name="close_ticket", description="Close the current ticket channel.")
    async def close_ticket_command(self, interaction: discord.Interaction):
        """Slash command to close a ticket."""
        try:
            await interaction.response.defer(ephemeral=True)

            channel = interaction.channel

            ticket_bot_cog = self.bot.get_cog("TicketBot")
            if not ticket_bot_cog:
                await interaction.followup.send(
                    "Error: TicketBot cog not found.",
                    ephemeral=True
                )
                return

            if channel.category and channel.category.name == TICKET_CATEGORY_NAME:
                view = ConfirmCloseTicketView(ticket_bot_cog, channel)
                await interaction.followup.send(
                    "Are you sure you would like to close this ticket?",
                    view=view,
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "This action is not allowed in this channel.",
                    ephemeral=True
                )

        except Exception as e:
            # Handle any errors
            await interaction.followup.send(
                "An error occurred while trying to close the ticket.",
                ephemeral=True
            )
            print(f"Error closing ticket: {e}")



    async def close_ticket_channel(self, channel, guild, closed_by_user):
        """Move the ticket channel to the closed category and disable sending messages."""
        closed_category = await self.get_or_create_category(guild, CLOSED_CATEGORY_NAME)
        
        await channel.edit(category=closed_category)

        overwrites = channel.overwrites
        for target, perms in overwrites.items():
            if isinstance(target, discord.Member) or isinstance(target, discord.Role):
                perms.send_messages = False
                overwrites[target] = perms

        await channel.edit(overwrites=overwrites)

        embed = discord.Embed(
            title="Ticket Closed",
            description=f"Ticket closed by {closed_by_user.mention}.",
                        # f"The ticket has been moved to the **Closed Tickets** category.",
            color=0xFF4500  # Orange-red color
        )
        # embed.set_footer(text="Support System • Ticket Management")
        # embed.set_thumbnail(url="https://example.com/your_logo.png")  # Optional thumbnail/logo

        await channel.send(embed=embed)

        await self.send_ticket_controls(channel, self)


    async def send_ticket_controls(self,channel, bot):
        """Send the ticket controls to the channel."""
        embed = discord.Embed(
            title="```Support Team Ticket Controls```",
            # description="Manage this ticket using the controls below.",
        )
        view = TicketControlView(bot, channel)
        await channel.send(embed=embed, view=view)

    def is_admin_or_support(self,user):
        """Check if the user has the Admin or Support Team role."""
        required_roles = ["Admin", SUPPORT_ROLE_NAME]
        user_roles = [role.name for role in user.roles]
        return any(role in user_roles for role in required_roles)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Handle a member joining and ensure 'Open Tickets' is set up under the 'Tickets' category."""
        guild = member.guild

        # Check if the category exists by name
        ticket_category = discord.utils.get(guild.categories, name=TEXT_CATEGORY_NAME)

        # If the category doesn't exist, create it
        if not ticket_category:
            ticket_category = await guild.create_category(TEXT_CATEGORY_NAME)
            print(f"Created '{TEXT_CATEGORY_NAME}' category.")

        open_tickets_channel = discord.utils.get(ticket_category.channels, name=OPEN_TICKET_CHANNEL_NAME)
        if not open_tickets_channel:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(
                    view_channel=True, 
                    send_messages=False,
                    read_message_history=False
                )
            }
            open_tickets_channel = await ticket_category.create_text_channel(
                name=OPEN_TICKET_CHANNEL_NAME,
                topic="This channel allows users to create support tickets.",
                overwrites=overwrites
            )
            print(f"Created '{OPEN_TICKET_CHANNEL_NAME}' channel under '{TEXT_CATEGORY_NAME}' category.")

        await open_tickets_channel.set_permissions(
            member,
            view_channel=True, 
            send_messages=False, 
            read_message_history=False
        )

        embed = discord.Embed(
            title="Support Ticket",
            description="To create a ticket react with 📩",
            color=0x00ff00  # Green color
        )
        embed.set_thumbnail(url="https://www.clipartmax.com/png/middle/303-3035057_customer-service-executive-team-placeholder.png")  
        # embed.set_footer(text="TicketTool.xyz - Ticketing without clutter")

        view = discord.ui.View()
        view.add_item(
        discord.ui.Button(
            label="📩 Create Ticket",
            style=discord.ButtonStyle.secondary,  # Gray color
            custom_id=f"create_ticket_{member.id}"  # Unique ID for the user
        )
    )

        await open_tickets_channel.send(
            content=f"Welcome <@{member.id}>! Please use the button below to create a ticket.",
            embed=embed,
            view=view,
        )

        await open_tickets_channel.set_permissions(
            member,
            read_message_history=True
        )

        # Log the event
        print(f"Sent a personalized message to {member.name} in '{OPEN_TICKET_CHANNEL_NAME}' channel.")

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        """Handle button interactions."""
        guild = interaction.guild
        member = interaction.user
        try:
            # Extract custom_id
            custom_id = interaction.data["custom_id"]

            if not custom_id:
                return
            
            if custom_id in ["transcript", "open_ticket", "delete_ticket","confirm_delete","cancel_delete"]:
                if not self.is_admin_or_support(interaction.user):
                    await interaction.response.send_message(
                        "You do not have permission to use this control.", ephemeral=True
                    )
                    return
            
            if custom_id == "transcript":
                try:
                    await interaction.response.send_message(
                        "Generating the ticket transcript...", ephemeral=True
                    )

                    transcript = []
                    async for message in interaction.channel.history(limit=None, oldest_first=True):
                        # Ignore bot messages
                        # if message.author.bot:
                        #     continue

                        # Format the timestamp, author, and content
                        timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                        roles = [role.name for role in message.author.roles if role.name != "@everyone"]
                        roles_str = f" ({', '.join(roles)})" if roles else ""
                        author = f"{message.author.name}#{message.author.discriminator}{roles_str}"
                        
                        content = message.clean_content or "[No Text Content]"

                        # Append the base message to the transcript
                        transcript.append(f"[{timestamp}] **{author}**: {content}")

                        # Handle attachments
                        for attachment in message.attachments:
                            transcript.append(f"[{timestamp}] **{author}**: [Attachment] {attachment.url}")

                        # # Handle embeds
                        # for embed in message.embeds:
                        #     embed_data = embed.to_dict()
                        #     embed_title = embed_data.get("title", "[No Title]")
                        #     embed_description = embed_data.get("description", "[No Description]")
                        #     embed_url = embed_data.get("url", None)

                        #     embed_content = f"[Embed] **{embed_title}**: {embed_description}"
                        #     if embed_url:
                        #         embed_content += f" (URL: {embed_url})"
                        #     transcript.append(f"[{timestamp}] **{author}**: {embed_content}")

                    # Format the transcript as a readable string
                            
                    transcript_content = "\n".join(transcript)

                    # Get or create the transcript category
                    transcript_category = await self.get_or_create_category(interaction.guild, TRANSCRIPT_CATEGORY_NAME)

                    transcript_channel_name = f"{interaction.channel.name}_transcript"
                    existing_channel = discord.utils.find(
                        lambda c: c.name == transcript_channel_name and c.category == transcript_category,
                        interaction.guild.channels
                    )

                    if not existing_channel:
                        transcript_channel = await interaction.guild.create_text_channel(
                            name=transcript_channel_name,
                            category=transcript_category,
                            overwrites={
                                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=False),
                            },
                            topic=f"Transcript of {interaction.channel.name}",
                        )
                    else:
                        transcript_channel = existing_channel

                    chunks = [transcript_content[i:i+2000] for i in range(0, len(transcript_content), 2000)]

                    readme_embed = discord.Embed(
                        title="Transcript Overview",
                        description=(
                            f"This is the transcript for `{interaction.channel.name}`.\n"
                            f"**Generated by:** {interaction.user.mention}\n"
                            f"**Original Channel:** {interaction.channel.mention}\n\n"
                            "Below, you'll find the full transcript of the conversation."
                        ),
                        color=0x5865F2,
                    )
                    await transcript_channel.send(embed=readme_embed)
                    for chunk in chunks:
                        await transcript_channel.send(chunk)

                    # Notify the user
                    await interaction.followup.send(
                        f"The transcript has been generated in {transcript_channel.mention}.", ephemeral=True
                    )

                except Exception as e:
                    await interaction.followup.send(
                        "An error occurred while generating the transcript.", ephemeral=True
                    )
                    print(f"Error generating transcript: {e}")


            elif custom_id == "open_ticket":
                try:
                    await interaction.response.defer()

                    open_tickets_category = await self.get_or_create_category(interaction.guild, TICKET_CATEGORY_NAME)

                    current_category = interaction.channel.category
                    if current_category and current_category.name == CLOSED_CATEGORY_NAME:
                        await interaction.channel.edit(category=open_tickets_category)

                        overwrites = interaction.channel.overwrites
                        for target, perms in overwrites.items():
                            if isinstance(target, discord.Member) or isinstance(target, discord.Role):
                                perms.send_messages = True
                                overwrites[target] = perms

                        await interaction.channel.edit(overwrites=overwrites)

                        await interaction.followup.send(
                            f"The ticket `{interaction.channel.name}` has been reopened.",
                            ephemeral=False
                        )
                    else:
                        await interaction.followup.send(
                            "This ticket is not in the Closed Tickets category and cannot be reopened.",
                            ephemeral=True
                        )

                except Exception as e:
                    await interaction.followup.send(
                        "An error occurred while trying to reopen the ticket.",
                        ephemeral=True
                    )
                    print(f"Error reopening ticket: {e}")

            elif custom_id == "delete_ticket":
                try:
                    await interaction.response.defer()

                    view = discord.ui.View(timeout=30)
                    view.add_item(discord.ui.Button(label="Confirm", style=discord.ButtonStyle.danger, custom_id="confirm_delete"))
                    view.add_item(discord.ui.Button(label="Cancel", style=discord.ButtonStyle.secondary, custom_id="cancel_delete"))

                    await interaction.followup.send(
                        "Are you sure you want to delete this ticket? This action cannot be undone.",
                        view=view,
                        ephemeral=True
                    )

                except Exception as e:
                    await interaction.followup.send(
                        "An error occurred while trying to initiate ticket deletion.",
                        ephemeral=True
                    )
                    print(f"Error initiating ticket deletion: {e}")

            elif custom_id == "confirm_delete":
                try:
                    await interaction.response.defer()

                    await interaction.channel.delete(reason=f"Ticket deleted by {interaction.user.name}#{interaction.user.discriminator}")

                except Exception as e:
                    await interaction.followup.send(
                        "An error occurred while trying to delete the ticket.",
                        ephemeral=True
                    )
                    print(f"Error deleting ticket: {e}")

            elif custom_id == "cancel_delete":
                try:
                    await interaction.response.send_message("Ticket deletion canceled.", ephemeral=True)
                except Exception as e:
                    print(f"Error canceling ticket deletion: {e}")


            elif custom_id.startswith("create_ticket"):
                if not interaction.response.is_done():
                    await interaction.response.defer(ephemeral=True)

                if "_" in custom_id:
                    target_user_id = int(custom_id.split("_")[-1])
                    if member.id != target_user_id:
                        followup_message = await interaction.followup.send(
                            "This button is not meant for you.", ephemeral=True
                        )
                        await asyncio.sleep(5)
                        await followup_message.delete()
                        return

                ticket_category = await self.get_or_create_category(guild, TICKET_CATEGORY_NAME)
                existing_channel = discord.utils.find(
                    lambda c: (
                        c.category == ticket_category
                        and c.overwrites_for(interaction.user).view_channel
                        and c.overwrites_for(interaction.user).send_messages
                    ),
                    interaction.guild.channels
                )

                if existing_channel:
                    followup_message = await interaction.followup.send(
                        f"You already have an open ticket: {existing_channel.mention}",
                        ephemeral=True
                    )
                    await asyncio.sleep(5)
                    await followup_message.delete()
                else:
                    channel = await self.create_ticket_channel(guild, member)

                    followup_message = await interaction.followup.send(
                        f"Ticket created successfully: {channel.mention}",
                        ephemeral=True
                    )
                    # Delete the follow-up after 5 seconds
                    await asyncio.sleep(5)
                    await followup_message.delete()

            elif custom_id == "close_ticket":
                if not interaction.response.is_done():
                    await interaction.response.defer(ephemeral=True)

                channel = interaction.channel

                if channel.category and channel.category.name == TICKET_CATEGORY_NAME:
                    view = ConfirmCloseTicketView(self, channel)
                    followup_message = await interaction.followup.send(
                        "Are you sure you would like to close this ticket?",
                        view=view,
                        ephemeral=True
                    )
                    await asyncio.sleep(5)
                    await followup_message.delete()
                else:
                    followup_message = await interaction.followup.send(
                        "This action is not allowed in this channel.", ephemeral=True
                    )
                    await asyncio.sleep(5)
                    await followup_message.delete()

            elif custom_id == "close_ticket_confirm":
                channel = interaction.channel
                if channel.category and channel.category.name == TICKET_CATEGORY_NAME:
                    if interaction.user in channel.members:
                        if not interaction.response.is_done():
                            await interaction.response.defer()

                        ticket_bot_cog = self.bot.get_cog("TicketBot")
                        if ticket_bot_cog:
                            await ticket_bot_cog.close_ticket_channel(channel, interaction.guild,interaction.user)
                        else:
                            print("TicketBot cog not found!")
                    else:
                        if not interaction.response.is_done():
                            await interaction.response.send_message(
                                "You do not have permission to close this ticket.", ephemeral=True
                            )

            elif custom_id == "close_ticket_cancel":
                if not interaction.response.is_done():
                    await interaction.response.defer()

                await interaction.followup.send(
                    content="Ticket closure cancelled.", ephemeral=True
                )
        except Exception as e:
            pass


    @commands.command()
    async def close(self, ctx):
        """Command to close the ticket."""
        if ctx.channel.category and ctx.channel.category.name == TICKET_CATEGORY_NAME:
            await self.close_ticket_channel(ctx.channel, ctx.guild)
            await ctx.send("This ticket has been closed")
        else:
            await ctx.send("This is not a ticket channel!")

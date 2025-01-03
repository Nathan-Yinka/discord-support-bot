import discord


class CloseTicketView(discord.ui.View):
    """A custom view for ticket closure."""

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

        self.add_item(discord.ui.Button(label="Close Ticket", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket"))

class ConfirmCloseTicketView(discord.ui.View):
    """A view for confirming ticket closure."""

    def __init__(self, bot, channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.channel = channel

        self.add_item(discord.ui.Button(label="Close", style=discord.ButtonStyle.danger, emoji="❌", custom_id="close_ticket_confirm"))
        self.add_item(discord.ui.Button(label="Cancel", style=discord.ButtonStyle.secondary, custom_id="close_ticket_cancel"))

class TicketControlView(discord.ui.View):
    """Support team ticket control view with buttons."""

    def __init__(self, bot, channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.channel = channel

        self.add_item(discord.ui.Button(label="Transcript", style=discord.ButtonStyle.secondary, emoji="📄", custom_id="transcript"))
        self.add_item(discord.ui.Button(label="Open", style=discord.ButtonStyle.success, emoji="🔓", custom_id="open_ticket"))
        self.add_item(discord.ui.Button(label="Delete", style=discord.ButtonStyle.danger, emoji="⛔", custom_id="delete_ticket"))

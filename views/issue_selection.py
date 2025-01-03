import discord
from discord.ui import Select, View


class IssueSelectionView(View):
    """A dropdown menu view for selecting an issue."""

    def __init__(self):
        super().__init__(timeout=None) 

        self.add_item(IssueSelectMenu())

class IssueSelectMenu(Select):
    """Custom Select menu for issue selection."""

    def __init__(self):
        options = [
            discord.SelectOption(label="Migration", description="Migration-related issues"),
            discord.SelectOption(label="Rectify", description="Rectify strange wallet issues"),
            discord.SelectOption(label="Claim", description="Token claiming issues"),
            discord.SelectOption(label="Swap/Exchange", description="Token swap/exchange issue"),
            discord.SelectOption(label="Slippage", description="Slippage or transaction fee issues"),
        ]

        super().__init__(
            placeholder="Select an issue",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="select_issue"
        )

    async def callback(self, interaction: discord.Interaction):
        """Handle the issue selection and link to a URL."""
        issue_links = {
            "Migration": "https://example.com/migration",
            "Rectify": "https://example.com/rectify",
            "Claim": "https://example.com/claim",
            "Swap/Exchange": "https://example.com/swap-exchange",
            "Slippage": "https://example.com/slippage"
        }

        selected_option = self.values[0]
        url = issue_links.get(selected_option, "https://example.com")

        await interaction.response.send_message(
            f"You selected: **{selected_option}**.\nClick [here]({url}) to proceed to the corresponding page.",
            ephemeral=False
        )

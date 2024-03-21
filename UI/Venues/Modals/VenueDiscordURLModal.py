from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("VenueDiscordURLModal",)

################################################################################
class VenueDiscordURLModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[str]):
        
        super().__init__(title="Edit Discord URL")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your venue's Discord URL.",
                value="Enter a new Discord URL or edit the currently existing one.",
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Discord URL",
                placeholder="eg. 'https://discord.gg/upfEWWxC'",
                value=cur_val,
                max_length=100,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        # RegEx to match a discord invite if I ever end up needing it.
        # rx = r"(?:https?\:\/\/)?discord(?:\.gg|(?:app)?\.com\/invite)\/(.+)"
        
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################

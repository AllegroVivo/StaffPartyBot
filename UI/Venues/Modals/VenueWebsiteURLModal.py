from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("VenueWebsiteURLModal",)

################################################################################
class VenueWebsiteURLModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[str]):
        
        super().__init__(title="Edit Webpage URL")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your venue's webpage URL.",
                value="Enter a new webpage URL or edit the currently existing one.",
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Webpage URL",
                placeholder="eg. 'https://carrd.co/LilypadLounge'",
                value=cur_val,
                max_length=200,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################

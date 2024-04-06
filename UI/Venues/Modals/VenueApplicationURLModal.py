from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("VenueApplicationURLModal",)

################################################################################
class VenueApplicationURLModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[str]):
        
        super().__init__(title="Edit Application URL")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your venue's Application URL.",
                value="Enter a new application form URL or edit the currently existing one.",
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Application URL",
                placeholder="eg. 'https://discord.gg/upfEWWxC'",
                value=cur_val,
                max_length=100,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):        
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################

from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("ProfileURLModal",)

################################################################################
class ProfileURLModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[str]):
        
        super().__init__(title="Edit Custom URL")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a custom URL.",
                value=(
                    "Enter a new custom URL for your profile in the box below, "
                    "or edit the currently existing one."
                ),
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Custom URL",
                placeholder="eg. 'https://twitter.com/HomeHopping'",
                value=cur_val,
                max_length=200,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################

from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("ProfileRatesModal",)

################################################################################
class ProfileRatesModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[str]):

        super().__init__(title="Profile Rates Section")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your Rates section information below.",
                value=(
                    "Enter the information for your 'Rates' section "
                    "exactly as you want it displayed on your profile.\n"
                    "This supports markdown and emojis."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Rates Section",
                placeholder="eg. '250k gil per photo shoot'",
                value=cur_val,
                max_length=500,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################

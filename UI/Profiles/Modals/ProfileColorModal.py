from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle, Colour
from discord.ui import InputText

from Utilities import InvalidColorError

from UI.Common import FroggeModal
################################################################################

__all__ = ("ProfileColorModal",)

################################################################################
class ProfileColorModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[Colour]):
        
        super().__init__(title="Edit Name")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your desired accent color.",
                value=(
                    "Enter the 6-character HEX code for your desired profile accent color.\n"
                    "Google Color Picker:\n"
                    "https://g.co/kgs/psoVFb"
                ),
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Accent Color HEX",
                placeholder="#4ABC23",
                value=str(cur_val).upper() if cur_val is not None else None,
                min_length=6,
                max_length=7,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        value = self.children[1].value.upper()
        if value.startswith("#"):
            value = value[1:]
            
        try:
            self.value = int(value, 16) if self.children[1].value else None
        except ValueError:
            error = InvalidColorError(self.children[1].value)
            await interaction.respond(embed=error, ephemeral=True)
        else:
            self.complete = True
            await interaction.edit()
        
        self.stop()

################################################################################

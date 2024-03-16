from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("VenueDescriptionModal",)

################################################################################
class VenueDescriptionModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[str]):
        
        super().__init__(title="Edit Venue Description")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a venue description.",
                value="Enter a new description or edit the currently existing one.",
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Name",
                placeholder="eg. 'The perfect place to lie back and relax with a good book.'",
                value=cur_val,
                max_length=500,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################

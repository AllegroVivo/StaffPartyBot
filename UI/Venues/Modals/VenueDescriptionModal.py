from __future__ import annotations

from typing import List

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("VenueDescriptionModal",)

################################################################################
class VenueDescriptionModal(FroggeModal):
    
    def __init__(self, cur_val: List[str]):
        
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
        
        value = "\n".join(cur_val) if cur_val else None
        if value is not None and len(value) > 499:
            value = value[:499]
            
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Name",
                placeholder="eg. 'The perfect place to lie back and relax with a good book.'",
                value=value,
                max_length=500,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = [
            i for i in self.children[1].value.split("\n") if i
        ] if self.children[1].value else []
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################

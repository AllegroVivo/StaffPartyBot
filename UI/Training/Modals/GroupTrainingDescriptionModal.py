from __future__ import annotations

from typing import List, Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("GroupTrainingDescriptionModal",)

################################################################################
class GroupTrainingDescriptionModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[str]):
        
        super().__init__(title="Edit Event Title")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter the description for your group training.",
                value="Please enter the description for your group training. ",
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Name(s)",
                value=cur_val,
                max_length=200,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################

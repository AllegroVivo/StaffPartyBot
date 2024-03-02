from __future__ import annotations

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("PositionNameModal",)

################################################################################
class PositionNameModal(FroggeModal):

    def __init__(self, cur_val: str):

        super().__init__(title="Edit Job Position Name")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a new name for this job...",
                value="Enter a new name for this job...",
                required=False
            )
        )
        
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Job Name",
                placeholder="eg. 'Bartender'",
                value=cur_val,
                max_length=30,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True
        
        await interaction.edit()
        self.stop()
        
################################################################################

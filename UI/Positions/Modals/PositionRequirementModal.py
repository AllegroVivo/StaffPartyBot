from __future__ import annotations

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("PositionRequirementModal",)

################################################################################
class PositionRequirementModal(FroggeModal):

    def __init__(self):

        super().__init__(title="Add New Position Requirement")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a new training requirement for this job...",
                value="Enter a new training requirement for this job below...",
                required=False
            )
        )
        
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Requirement Text",
                placeholder="eg. 'Able to speak fluent Frogge'",
                max_length=100,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True
        
        await interaction.edit()
        self.stop()
        
################################################################################

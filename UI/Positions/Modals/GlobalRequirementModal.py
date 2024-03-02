from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("GlobalRequirementModal",)

################################################################################
class GlobalRequirementModal(FroggeModal):

    def __init__(self):

        super().__init__(title="Add New Global Position Requirement")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a new training requirement for all jobs...",
                value="Enter a new training requirement applicable to all jobs below...",
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

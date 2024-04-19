from __future__ import annotations

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("ServiceNameModal",)

################################################################################
class ServiceNameModal(FroggeModal):

    def __init__(self, cur_val: str):

        super().__init__(title="Edit Hireable Service Name")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a new name for this service...",
                value="Enter a new name for this service...",
                required=False
            )
        )
        
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Service Name",
                placeholder="eg. 'Discord Admin'",
                value=cur_val,
                max_length=40,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True
        
        await interaction.edit()
        self.stop()
        
################################################################################

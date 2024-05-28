from __future__ import annotations

from typing import List, Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("GroupTrainingTitleModal",)

################################################################################
class GroupTrainingTitleModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[str]):
        
        super().__init__(title="Edit Event Title")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter the title for your group training.",
                value="Please enter the title for your group training. ",
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Name(s)",
                placeholder="eg. 'Allegro's Frogtacular Training'",
                value=cur_val,
                max_length=50,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################

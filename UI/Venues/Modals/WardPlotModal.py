from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("WardPlotModal",)

################################################################################
class WardPlotModal(FroggeModal):
    
    def __init__(self, cur_ward: Optional[int], cur_plot: Optional[int]):
        
        super().__init__(title="Edit Venue Description")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter the venue's ward and plot number.",
                value=(
                    "Enter the ward and plot number for the venue.\n"
                    "These should just be the raw numbers. (eg. 5, 12)"
                ),
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Ward",
                placeholder="eg. '5'",
                value=str(cur_ward) if cur_ward else None,
                max_length=2,
                required=True
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Plot",
                placeholder="eg. '12'",
                value=str(cur_plot) if cur_plot else None,
                max_length=2,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = (int(self.children[1].value), int(self.children[2].value))
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################

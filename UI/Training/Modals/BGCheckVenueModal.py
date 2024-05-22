from __future__ import annotations

from typing import List

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("BGCheckVenueModal",)

################################################################################
class BGCheckVenueModal(FroggeModal):
    
    def __init__(self):
        
        super().__init__(title="Add Venue Experience")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your character's venue experience.",
                value=(
                    "Please enter the name of a venue which you'd like "
                    "to list as a reference, as well as the position(s) in which "
                    "you were employed."
                ),
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Venue Name",
                placeholder="eg. 'Lilypad Lounge'",
                max_length=50,
                required=True
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Jobs Worked",
                placeholder="eg. 'Bartender, Bouncer'",
                max_length=200,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = (
            self.children[1].value,
            [j.strip() for j in self.children[2].value.split(",")]
        )
        self.complete = True
        
        await interaction.edit()
        self.stop()

################################################################################

from __future__ import annotations

from typing import Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
from Utilities import Race, Clan
################################################################################

__all__ = ("ProfilePersonalityModal",)

################################################################################
class ProfilePersonalityModal(FroggeModal):
    
    def __init__(self, personality: Optional[str]):
        
        super().__init__(title="Set Custom Clan Value")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your Personality value in the box below.",
                value = (
                    f"Enter your desired Personality section content here. "
                    "Note that this accepts markdown, newlines, and emojis, "
                    "so really make it your own. ♥"
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Personality",
                placeholder="eg. 'A beautiful froggy princess who loves flies.'",
                value=personality,
                max_length=300,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################

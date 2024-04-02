from __future__ import annotations

from typing import Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
from Utilities import Race, Clan
################################################################################

__all__ = ("AdditionalImageCaptionModal",)

################################################################################
class AdditionalImageCaptionModal(FroggeModal):
    
    def __init__(self, cur_caption: Optional[str] = None):
        
        super().__init__(title="Set Custom Clan Value")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter the caption for your image.",
                value=(
                    "Enter the caption for your additional image. This text will "
                    "take the place of the ugly-looking link text on your profile."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Caption",
                placeholder="eg. 'Leaping from lilypad to lilypad~'",
                value=cur_caption,
                max_length=50,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True

        await interaction.respond("** **", delete_after=0.1)
        self.stop()

################################################################################

from __future__ import annotations

from typing import Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
from Utilities import Race, Clan
################################################################################

__all__ = ("CustomClanModal",)

################################################################################
class CustomClanModal(FroggeModal):
    
    def __init__(self, cur_clan: Optional[Union[Clan, str]]):
        
        super().__init__(title="Set Custom Clan Value")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your custom Clan value in the blow below.",
                value=(
                    "Enter your custom Clan value below. This isn't required, and if \n"
                    "you don't want to enter one, simply submit a blank dialog."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Clan",
                placeholder="eg. 'Pad Leaper'",
                value=cur_clan if not isinstance(cur_clan, Clan) else None,
                max_length=25,
                required=False
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################

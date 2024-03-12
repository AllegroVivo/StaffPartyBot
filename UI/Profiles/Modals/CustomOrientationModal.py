from __future__ import annotations

from typing import Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
from Utilities import Orientation
################################################################################

__all__ = ("CustomOrientationModal",)

################################################################################
class CustomOrientationModal(FroggeModal):

    def __init__(self, cur_value: Optional[Union[Orientation, str]]):
        super().__init__(title="Set Your Custom Orientation Value")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your custom sexual orientation.",
                value="Enter the text you want to display as your sexual orientation.",
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Sexual Orientation",
                placeholder="eg. 'Frogge'",
                value=cur_value if not isinstance(cur_value, Orientation) else None,
                required=False,
                max_length=40
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################

from __future__ import annotations

from typing import Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
from Utilities import Gender
################################################################################

__all__ = ("CustomGenderModal",)

################################################################################
class CustomGenderModal(FroggeModal):

    def __init__(self, cur_val: Optional[Union[Gender, str]]):

        super().__init__(title="Set Custom Gender Value")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your custom gender identity below.",
                value=(
                    "Enter your custom gender identity in the box below.\n"
                    "You can choose your preferred pronouns after this."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Custom Gender",
                placeholder="eg. 'Amphibian'",
                value=cur_val if not isinstance(cur_val, Gender) else None,
                max_length=30,
                required=True
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################

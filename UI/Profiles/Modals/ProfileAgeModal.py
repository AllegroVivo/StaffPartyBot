from __future__ import annotations

from typing import Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("ProfileAgeModal",)

################################################################################
class ProfileAgeModal(FroggeModal):

    def __init__(self, cur_val: Optional[Union[str, int]]):
        super().__init__(title="Age Value Input")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your age below.",
                value="Enter your age. It may be a numerical value or text.",
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Age",
                placeholder="eg. '32' -or- 'Older than you think...'",
                value=str(cur_val) if cur_val is not None else None,
                required=False,
                max_length=30
            )
        )

    async def callback(self, interaction: Interaction):
        if self.children[1].value:
            if self.children[1].value.isdigit():
                self.value = abs(int(self.children[1].value))
            else:
                self.value = self.children[1].value

        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################

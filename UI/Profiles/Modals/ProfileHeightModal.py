from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("ProfileHeightModal",)

################################################################################
class ProfileHeightModal(FroggeModal):

    def __init__(self, cur_val: Optional[int]):
        super().__init__(title="Height Entry")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your height in feet and inches.",
                value="Enter your height in feet and inches, or centimeters.",
                required=False
            )
        )

        if cur_val is not None:
            inches = int(cur_val / 2.54)
            feet = int(inches / 12)
            leftover = int(inches % 12)
            cur_val = f"{feet}' {leftover}\""

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Height",
                placeholder="eg. '6ft 2in'",
                value=cur_val,
                required=False,
                max_length=20
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################

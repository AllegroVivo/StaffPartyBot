from __future__ import annotations

from typing import Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("PositionDescriptionModal",)

################################################################################
class PositionDescriptionModal(FroggeModal):

    def __init__(self, cur_val: Optional[str]):
        super().__init__(title="Position Description Entry")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a description below.",
                value="Enter a more detailed description for the job position.",
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Description",
                value=str(cur_val) if cur_val is not None else None,
                required=False,
                max_length=500
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################

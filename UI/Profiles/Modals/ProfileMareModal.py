from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("ProfileMareModal",)

################################################################################
class ProfileMareModal(FroggeModal):

    def __init__(self, cur_val: Optional[str]):
        super().__init__(title="Friend ID Code Entry")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter your Mare ID/pairing code.",
                value="Enter your alphanumeric Mare Pairing ID below.",
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Mare ID",
                placeholder="eg. 'A1B2C3D4E5'",
                value=cur_val,
                required=False,
                max_length=30
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value if self.children[1].value else None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################

from __future__ import annotations

from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("PositionTrainerPayModal",)

################################################################################
class PositionTrainerPayModal(FroggeModal):

    def __init__(self, cur_val: Optional[int]):

        super().__init__(title="Edit Job Pay Rate")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter this job's trainer pay amount.",
                value="Enter the trainer pay rate for this job...",
                required=False
            )
        )
        
        pay_val = f"{cur_val:,}" if cur_val else None
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Trainer Pay",
                placeholder="eg. '100,000' or '200k'",
                value=pay_val,
                max_length=12,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True
        
        await interaction.edit()
        self.stop()
        
################################################################################

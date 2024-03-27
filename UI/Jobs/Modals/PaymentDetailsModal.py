from __future__ import annotations

from typing import Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText, Modal

from UI.Common import FroggeModal
################################################################################

__all__ = ("PaymentDetailsModal",)

################################################################################
class PaymentDetailsModal(FroggeModal):

    def __init__(self, cur_val: Optional[str]):
        super().__init__(title="Payment Details Entry")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter additional details below.",
                value=(
                    "Enter any additional details about this job posting. If "
                    "there are none, you can leave this blank."
                ),
                required=False
            )
        )

        # self.add_item(
        #     InputText(
        #         style=InputTextStyle.multiline,
        #         label="Job Details",
        #         value=str(cur_val) if cur_val is not None else None,
        #         required=False,
        #         max_length=500
        #     )
        # )

    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value or None
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################

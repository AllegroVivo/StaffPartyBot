from __future__ import annotations

from typing import Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("JobReportRangeModal",)

################################################################################
class JobReportRangeModal(FroggeModal):

    def __init__(self):
        super().__init__(title="Job Posting Date Range")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter the start and end dates for the job posting report.",
                value=(
                    "Enter the start and end dates for the job posting report. "
                    "You may leave either field blank to indicate today's date."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Start Date",
                placeholder="MM/DD/YYYY",
                required=False,
                max_length=20
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="End Date",
                placeholder="MM/DD/YYYY",
                required=False,
                max_length=20
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = (
            self.children[1].value if self.children[1].value else None, 
            self.children[2].value if self.children[2].value else None
        )
        self.complete = True

        await interaction.response.edit_message()
        self.stop()

################################################################################

from __future__ import annotations

from typing import Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText, Modal
from Utilities import Utilities as U, InvalidSalaryError

from UI.Common import FroggeModal
################################################################################

__all__ = ("SalaryModal",)

################################################################################
class SalaryModal(FroggeModal):

    def __init__(self, cur_sal: Optional[int], cur_details: Optional[str]):
        super().__init__(title="Job Salary Entry")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a salary below.",
                value="Enter the salary for this job posting.",
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Salary",
                value=str(cur_sal) if cur_sal is not None else None,
                required=True,
                max_length=15
            )
        )
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Other Details",
                placeholder="Enter any other payment details here.",
                value=str(cur_details) if cur_details is not None else None,
                required=False,
                max_length=200
            )
        )

    async def callback(self, interaction: Interaction):
        if not (salary := U.parse_salary(self.children[1].value)):
            error = InvalidSalaryError(self.children[1].value)
            await interaction.respond(embed=error, ephemeral=True)
            return

        self.value = salary, (self.children[2].value or None), interaction
        self.complete = True

        self.stop()

################################################################################

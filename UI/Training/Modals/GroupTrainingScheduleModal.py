from __future__ import annotations

from datetime import datetime
from typing import Optional, Union

from discord import Interaction, InputTextStyle
from discord.ui import InputText, Modal

from UI.Common import FroggeModal
################################################################################

__all__ = ("GroupTrainingScheduleModal",)

################################################################################
class GroupTrainingScheduleModal(FroggeModal):

    def __init__(self, cur_start: Optional[datetime], cur_end: Optional[datetime]):
        super().__init__(title="Edit Group Training Times")

        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter the start and stop times below.",
                value=(
                    "Enter the start and stop times for the group training "
                    "in the format MM/DD/YYYY HH:MM AM/PM."
                ),
                required=False
            )
        )

        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Start Time",
                placeholder="MM/DD/YYYY HH:MM AM/PM",
                value=(
                    f"{cur_start.strftime('%m/%d/%Y %I:%M %p')}"
                    if cur_start is not None 
                    else None
                ),
                required=True,
                max_length=20
            )
        )
        
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Stop Time",
                placeholder="MM/DD/YYYY HH:MM AM/PM",
                value=(
                    f"{cur_end.strftime('%m/%d/%Y %I:%M %p')}"
                    if cur_end is not None 
                    else None
                ),
                required=True,
                max_length=20
            )
        )

    async def callback(self, interaction: Interaction):
        self.value = (self.children[1].value, self.children[2].value)
        self.complete = True

        await interaction.respond("** **", delete_after=0.1)
        self.stop()

################################################################################

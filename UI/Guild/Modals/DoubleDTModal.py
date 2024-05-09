from __future__ import annotations

from datetime import datetime
from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("DoubleDTModal",)

################################################################################
class DoubleDTModal(FroggeModal):
    
    def __init__(
        self, 
        cur_val_a: Optional[datetime], 
        cur_val_b: Optional[datetime], 
        title: Optional[str] = None
    ):
        
        super().__init__(title=title or "Enter Start/End DateTimes")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a date and time.",
                value=(
                    "Enter start and end dates and times in the format: "
                    "MM/DD/YY HH:MM AM/PM.\n"
                ),
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Start Datetime",
                placeholder="eg. '12/31/24 11:59 PM'",
                value=(
                    cur_val_a.strftime("%m/%d/%y %I:%M %p")
                    if cur_val_a else None
                ),
                max_length=20,
                required=True
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="End Datetime",
                placeholder="eg. '12/31/24 11:59 PM'",
                value=(
                    cur_val_b.strftime("%m/%d/%y %I:%M %p")
                    if cur_val_b else None
                ),
                max_length=20,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value, self.children[2].value
        self.complete = True
        
        await self.dummy_response(interaction)
        self.stop()

################################################################################

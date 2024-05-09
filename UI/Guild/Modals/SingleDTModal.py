from __future__ import annotations

from datetime import datetime
from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("SingleDTModal",)

################################################################################
class SingleDTModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[datetime], title: Optional[str] = None):
        
        super().__init__(title=title or "Enter a Date and Time")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a date and time.",
                value=(
                    "Enter a date and time in the format MM/DD/YY HH:MM AM/PM.\n"
                    "Example: 12/31/24 11:59 PM"
                ),
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Datetime",
                placeholder="eg. '12/31/24 11:59 PM'",
                value=(
                    cur_val.strftime("%m/%d/%y %I:%M %p")
                    if cur_val else None
                ),
                max_length=20,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True

        await self.dummy_response(interaction)
        self.stop()

################################################################################

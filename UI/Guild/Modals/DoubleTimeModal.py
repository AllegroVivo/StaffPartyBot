from __future__ import annotations

from datetime import time
from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("DoubleTimeModal",)

################################################################################
class DoubleTimeModal(FroggeModal):
    
    def __init__(
        self, 
        cur_val_a: Optional[time], 
        cur_val_b: Optional[time], 
        title: Optional[str] = None
    ):
        
        super().__init__(title=title or "Enter Start/End Times")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter times.",
                value=(
                    "Enter start and end times in the format: HH:MM AM/PM.\n"
                ),
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Start Time",
                placeholder="eg. '11:59 PM'",
                value=(
                    cur_val_a.strftime("%I:%M %p")
                    if cur_val_a else None
                ),
                max_length=10,
                required=True
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="End Datetime",
                placeholder="eg. '11:59 PM'",
                value=(
                    cur_val_b.strftime("%I:%M %p")
                    if cur_val_b else None
                ),
                max_length=10,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value, self.children[2].value
        self.complete = True
        
        await self.dummy_response(interaction)
        self.stop()

################################################################################

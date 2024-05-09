from __future__ import annotations

from datetime import time
from typing import Optional

from discord import Interaction, InputTextStyle
from discord.ui import InputText

from UI.Common import FroggeModal
################################################################################

__all__ = ("SingleTimeModal",)

################################################################################
class SingleTimeModal(FroggeModal):
    
    def __init__(self, cur_val: Optional[time], title: Optional[str] = None):
        
        super().__init__(title=title or "Enter a Time")
        
        self.add_item(
            InputText(
                style=InputTextStyle.multiline,
                label="Instructions",
                placeholder="Enter a time.",
                value=(
                    "Enter a time in the format HH:MM AM/PM.\n"
                    "Example: 11:59 PM"
                ),
                required=False
            )
        )
        self.add_item(
            InputText(
                style=InputTextStyle.singleline,
                label="Time",
                placeholder="eg. '11:59 PM'",
                value=(
                    cur_val.strftime("%I:%M %p")
                    if cur_val else None
                ),
                max_length=10,
                required=True
            )
        )
        
    async def callback(self, interaction: Interaction):
        self.value = self.children[1].value
        self.complete = True

        await self.dummy_response(interaction)
        self.stop()

################################################################################

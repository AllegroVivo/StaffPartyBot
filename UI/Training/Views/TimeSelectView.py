from __future__ import annotations

import os
from datetime import time

from discord import Interaction, User
from discord.ui import Select
from dotenv import load_dotenv

from UI.Common import FroggeView, CloseMessageButton
from Utilities import Hours, Minutes
################################################################################

__all__ = ("TimeSelectView",)

################################################################################
class TimeSelectView(FroggeView):

    def __init__(self,  user: User):
        
        super().__init__(user, close_on_complete=True)

        self.add_item(HourSelect())
        self.add_item(CloseMessageButton())
    
################################################################################
class HourSelect(Select):
    
    def __init__(self):
        
        super().__init__(
            placeholder="Select the hour...",
            options=Hours.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        value = int(self.values[0])
        # Adjust for null initial value
        value -= 1
        
        if value == -1:  # Unavailable
            self.view.value = value
            self.view.complete = True
            await interaction.edit()
            await self.view.stop()  # type: ignore
            return

        self.placeholder = [
            option for option in self.options if option.value == self.values[0]
        ][0].label
        self.disabled = True
        
        load_dotenv()
        if os.getenv("DEBUG") == "False":
            # Adjust for EST timezone if in production
            value += 4
            if value > 23:
                value -= 24
            
        self.view.add_item(MinuteSelect(value))
        await interaction.edit(view=self.view)
    
################################################################################
class MinuteSelect(Select):

    def __init__(self, hour: int):

        super().__init__(
            placeholder="Select the minutes...",
            options=Minutes.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )
        
        self.hour = hour

    async def callback(self, interaction: Interaction):
        minutes = int(Minutes(int(self.values[0])).proper_name[3:])
        self.view.value = time(
            hour=self.hour, 
            minute=minutes
        )
        self.view.complete = True

        await interaction.edit()
        await self.view.stop()  # type: ignore

################################################################################

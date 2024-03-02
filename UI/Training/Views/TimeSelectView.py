from __future__ import annotations

from datetime import time

from discord import Interaction, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import Utilities as U, Hours, Minutes, Timezone
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
        self.view.value = value
        
        if value == 0:  # Unavailable
            self.view.value = -1
            self.view.complete = True
            await interaction.edit()
            await self.view.stop()  # type: ignore
            return

        self.placeholder = [
            option for option in self.options if option.value == self.values[0]
        ][0].label
        self.disabled = True

        self.view.add_item(MinuteSelect())
        await interaction.edit(view=self.view)
    
################################################################################
class MinuteSelect(Select):

    def __init__(self):

        super().__init__(
            placeholder="Select the minutes...",
            options=Minutes.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction):
        minutes = int(Minutes(int(self.values[0])).proper_name[3:])
        self.view.value = time(self.view.value - 1, minutes)  # type: ignore

        self.placeholder = [
            option for option in self.options if option.value == self.values[0]
        ][0].label
        self.disabled = True
        
        self.view.add_item(TimezoneSelect())
        await interaction.edit(view=self.view)

################################################################################
class TimezoneSelect(Select):

    def __init__(self):

        super().__init__(
            placeholder="Select your timezone...",
            options=Timezone.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=2
        )

    async def callback(self, interaction: Interaction):
        tz_info = U.TIMEZONE_OFFSETS[Timezone(int(self.values[0]))]
        self.view.value = time(self.view.value.hour, self.view.value.minute, tzinfo=tz_info) 
        self.view.complete = True

        await interaction.edit()
        await self.view.stop()  # type: ignore

################################################################################

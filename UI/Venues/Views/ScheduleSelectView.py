from __future__ import annotations
from datetime import time
from discord import Interaction, User
from discord.ui import Select
import pytz

from UI.Common import FroggeView, CloseMessageButton
from Utilities import (
    Utilities as U,
    Weekday,
    edit_message_helper,
    Timezone, 
    Hours,
    Minutes
)
################################################################################

__all__ = ("ScheduleOpenSelectView",)

################################################################################
class ScheduleOpenSelectView(FroggeView):

    def __init__(self,  user: User):
        
        super().__init__(user, close_on_complete=True)
        
        self.add_item(WeekdaySelect())
        self.add_item(CloseMessageButton())
        
        self.weekday = None
        self.timezone = None
        self.hour = None
        
################################################################################
class WeekdaySelect(Select):
    
    def __init__(self):
                                   
        super().__init__(
            placeholder="Select a day to set the schedule for...",
            options=Weekday.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.weekday = Weekday(int(self.values[0]))
        self.view.add_item(TimezoneSelect())
        
        self.placeholder = self.view.weekday.proper_name
        self.disabled = True
        
        await edit_message_helper(interaction, view=self.view)
    
################################################################################
class TimezoneSelect(Select):
    
    def __init__(self):
        
        super().__init__(
            placeholder="Select a timezone...",
            options=Timezone.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )
        
    async def callback(self, interaction: Interaction):
        self.view.timezone = Timezone(int(self.values[0]))
        self.view.add_item(HourSelect())

        self.placeholder = self.view.timezone.proper_name
        self.disabled = True

        await edit_message_helper(interaction, view=self.view)
        
################################################################################
class HourSelect(Select):
    
    def __init__(self):
        
        super().__init__(
            placeholder="Select an hour...",
            options=Hours.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=2
        )
        
    async def callback(self, interaction: Interaction):
        self.view.hour = Hours(int(self.values[0]))
        self.view.add_item(MinuteSelect())
        
        self.placeholder = self.view.hour.proper_name
        self.disabled = True
        
        await edit_message_helper(interaction, view=self.view)
        
################################################################################
class MinuteSelect(Select):
    
    def __init__(self):
        
        super().__init__(
            placeholder="Select a minute...",
            options=Minutes.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=3
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = time(
            hour=self.view.hour.value - 1, 
            minute=int(Minutes(int(self.values[0])).proper_name.split(":")[1]),
            tzinfo=U.TIMEZONE_OFFSETS[self.view.timezone]
        )
        self.view.complete = True
        
        await edit_message_helper(interaction)
        await self.view.stop()  # type: ignore
        
################################################################################

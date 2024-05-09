from __future__ import annotations

from discord import Interaction, User
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
from Utilities import Weekday, Timezone
################################################################################

__all__ = ("TZWeekdaySelectView",)

################################################################################
class TZWeekdaySelectView(FroggeView):

    def __init__(self,  user: User):
        
        super().__init__(user, close_on_complete=True)
        
        self.tz = None
        
        self.add_item(TimezoneSelect())
        self.add_item(CloseMessageButton())
        
################################################################################
class TimezoneSelect(Select):
    
    def __init__(self):
        
        super().__init__(
            placeholder="Select a timezone...",
            options=Timezone.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=0
        )
        
    async def callback(self, interaction: Interaction):
        self.view.tz = Timezone(int(self.values[0]))
        self.view.add_item(WeekdaySelect())

        self.placeholder = self.view.tz.proper_name
        self.disabled = True

        # await interaction.respond("** **", delete_after=0.1)
        await interaction.edit(view=self.view)
        
################################################################################
class WeekdaySelect(Select):

    def __init__(self):

        super().__init__(
            placeholder="Select a day of the week...",
            options=Weekday.select_options(),
            min_values=1,
            max_values=1,
            disabled=False,
            row=1
        )

    async def callback(self, interaction: Interaction):
        self.view.value = self.view.tz, Weekday(int(self.values[0]))
        self.view.complete = True

        await interaction.respond("** **", delete_after=0.1)
        await self.view.stop()  # type: ignore

################################################################################
        
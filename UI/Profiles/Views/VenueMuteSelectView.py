from __future__ import annotations

from typing import List

from discord import Interaction, User, SelectOption
from discord.ui import Select

from UI.Common import FroggeView, CloseMessageButton
################################################################################

__all__ = ("VenueMuteSelectView",)

################################################################################        
class VenueMuteSelectView(FroggeView):

    def __init__(self, user: User, options: List[SelectOption]):

        super().__init__(user, close_on_complete=True)

        item_list = [
            VenueSelect(options),
            CloseMessageButton()
        ]
        for item in item_list:
            self.add_item(item)

################################################################################        
class VenueSelect(Select):

    def __init__(self, options: List[SelectOption]):
        super().__init__(
            placeholder="Select a Venue(s)...",
            options=options,
            disabled=False,
            row=0,
            min_values=1,
            max_values=len(options)
        )

    async def callback(self, interaction: Interaction):
        self.view.value = self.values
        self.view.complete = True
        
        await interaction.edit()
        await self.view.stop()  # type: ignore

################################################################################

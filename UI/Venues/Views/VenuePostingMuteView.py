from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button, View

from Assets import BotEmojis
from UI.Common import FroggeView, CloseMessageButton
from Utilities import DataCenter, edit_message_helper

if TYPE_CHECKING:
    from Classes import Venue
################################################################################

__all__ = ("VenuePostingMuteView",)

################################################################################
class VenuePostingMuteView(View):

    def __init__(self,  venue: Venue):
        
        super().__init__(timeout=None)
        
        self.venue: Venue = venue
        self.add_item(VenueMuteButton(self.venue.id))
        
################################################################################
class VenueMuteButton(Button):
    
    def __init__(self, venue_id: str):
                                   
        super().__init__(
            style=ButtonStyle.secondary,
            label="Mute Venue Pings (For Staff)",
            disabled=False,
            row=0,
            emoji=BotEmojis.Mute,
            custom_id=f"venue_mute_{venue_id}"
        )
        
    async def callback(self, interaction: Interaction):
        self.view.value = DataCenter(int(self.values[0]))
        self.view.complete = True
        
        await edit_message_helper(interaction)
        await self.view.stop()  # type: ignore
    
################################################################################

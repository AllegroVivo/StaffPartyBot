from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, ButtonStyle
from discord.ui import Button, View

from Assets import BotEmojis

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
        venue: Venue = self.view.venue
        tuser = venue.guild.training_manager[interaction.user.id]
        if tuser is None:
            await interaction.edit()
            return
        
        await tuser.mute_venue(interaction, venue)
    
################################################################################

from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView

if TYPE_CHECKING:
    from Classes import Venue
################################################################################

__all__ = ("VenueMatchView",)

################################################################################
class VenueMatchView(FroggeView):

    def __init__(self, user: User, venues: List[Venue]) -> None:

        super().__init__(user)

        for i, venue in enumerate(venues):
            row = 0 if i < 3 else 1
            self.add_item(VenueInterestButton(venue, row))

################################################################################
class VenueInterestButton(Button):

    def __init__(self, venue: Venue, row: int) -> None:

        super().__init__(
            style=ButtonStyle.primary,
            label=f"Notify {venue.name}",
            disabled=False,
            row=row
        )
        
        self.venue: Venue = venue

    async def callback(self, interaction: Interaction) -> None:
        await self.venue.notify_of_interest(interaction)

################################################################################
        